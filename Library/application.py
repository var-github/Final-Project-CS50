from cs50 import SQL
from datetime import date, timedelta
import urllib.parse
import requests
from tempfile import mkdtemp
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///info.db")


# default route - shows basic info
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # if book is due then returning the book
    due = db.execute("SELECT Due FROM users WHERE id = ?", session["user_id"])[0]["Due"]
    if due:
        if date(int(due[:4]), int(due[5:7]), int(due[8:])) < date.today():
            return redirect("/overdue")
    # showing info
    book_id = db.execute("SELECT reading FROM users WHERE id = ?", session["user_id"])[0]["reading"]
    if book_id:
        book_id = book_id.replace("[", "").replace("]", "").replace("'", "").split(", ")
        response = {}
        response.update(get_info(book_id))
        cover = response["cover_link"]
        response.pop("cover_link")
        response.pop("author_link")
        return render_template("index.html", message=response, cover=cover)
    else:
        return render_template("index.html", message=None)


# login route - displays login page
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("display.html", message="Please enter your username")
        elif not request.form.get("password"):
            return render_template("display.html", message="Please enter your password")
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("display.html", message="Invalid username or password")
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# register route - shows and handles registrations
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # error checking
        if not request.form.get("username"):
            return render_template("display.html", message="Please enter a username")
        elif not request.form.get("password"):
            return render_template("display.html", message="A password is necessary to protect your account")
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("display.html", message="The two passwords din't match")
        elif {"username": request.form.get("username")} in (db.execute("SELECT username FROM users")):
            return render_template("display.html", message="The username has already been used")
        else:
            # inserting their username and password into database
            username = request.form.get("username")
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(request.form.get("password")))
            # remebering someone logged in
            session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
            # creating a history table for each person
            return redirect("/")
    elif request.method == "GET":
        return render_template("register.html")



# this page is where you can search for a book
@app.route("/search", methods=["GET", "POST"])
@login_required
def book():
    # getting info based on catagory
    if request.method == "GET":
        return render_template("search.html", catagory="all", message=None, query=None)
    elif request.method == "POST":
        response = ""
        if request.form.get("catagory") == "all":
            url = "http://openlibrary.org/search.json?q=" + request.form.get("name").lower()
        elif request.form.get("catagory") == "title":
            url = "https://openlibrary.org/search.json?title=" + request.form.get("name").lower()
        elif request.form.get("catagory") == "author":
            url = "https://openlibrary.org/search.json?author=" + request.form.get("name").lower()
        elif request.form.get("catagory") == "ISBN":
            # not enough info if the search is by isbn number - gather more info on book
            if not request.form.get("name").lower().isnumeric():
                return render_template("search.html", catagory="all", query=None, message="Isbn numbers cannot contain letters or symbols", error="1")
            if len(request.form.get("name")) != 10 and len(request.form.get("name")) != 13:
                return render_template("search.html", catagory="all", query=None, message="Only isbn 10 and isbn 13 are supported", error="1")
            else:
                # info is catagory is isbn
                isbn = request.form.get("name")
                url = "https://openlibrary.org/isbn/" + isbn + ".json"
                response = requests.get(url)
                if response.status_code != 200:
                    return render_template("search.html", catagory="all", query=None, message="Invalid Isbn number", error="1")
                response = response.json()
                book_id = response["key"][7:]
                languages = {}
                for a in db.execute("SELECT * FROM languages"):
                    languages[a["abbvr"]] = a["name"]
                url = "https://openlibrary.org/books/" + book_id + ".json"
                data = requests.get(url)
                data = data.json()
                if "languages" in data.keys():
                    data["languages"] = [languages[data["languages"][0]["key"][11:]]]
                    if "languages" in response.keys() and data["languages"][0] not in response["languages"]:
                        response["languages"].append(data["languages"][0])
                        data.pop("languages")
                for y in response.keys():
                    if y in data.keys():
                        if (y == "isbn_13" or y == "publishers") and data[y][0] not in response[y]:
                            response[y].append(data[y][0])
                            data.pop(y)
                        else:
                            data.pop(y)
                response.update(data)
                url = "https://openlibrary.org" + response["works"][0]["key"] + ".json"
                data = requests.get(url)
                data = data.json()
                if "covers" in data.keys():
                    cover = "https://covers.openlibrary.org/b/id/" + str(data["covers"][0]) + "-L.jpg"
                if "authors" in data.keys():
                    author = "https://covers.openlibrary.org/a/olid" + str(data["authors"][0]["author"]["key"][8:]) + "-L.jpg"
                response["work"] = data
                return render_template("info.html", message=response, cover=cover, author=author, book_id=book_id)
        response = requests.get(url)
        response = response.json()["docs"]
        if not response:
            return render_template("search.html", catagory="all", query=None, message="No results found, please use different keywords or navigate to the specific catagory and search", error="1")
        data = []
        languages = {}
        # formatting response
        for a in db.execute("SELECT * FROM languages"):
            languages[a["abbvr"]] = a["name"]
        for x in range(len(response)):
            if "author_name" in response[x].keys() and "edition_key" in response[x].keys():
                data.append({"title": response[x]["title"], "author": response[x]["author_name"], "book_id": response[x]["edition_key"]})
                if "subject" in response[x].keys():
                    data[len(data) - 1]["subject"] = response[x]["subject"]
                if "first_publish_year" in response[x].keys():
                    data[len(data) - 1]["published"] = response[x]["first_publish_year"]
                if "publisher" in response[x].keys():
                    data[len(data) - 1]["publisher"] = response[x]["publisher"]
                if "language" in response[x].keys():
                    data[len(data) - 1]["language"] = []
                    for y in response[x]["language"]:
                        if y not in languages.keys():
                            url = "https://openlibrary.org/languages/" + y + ".json"
                            answer = requests.get(url)
                            answer = answer.json()
                            languages[y] = answer["name"]
                            db.execute("INSERT INTO languages (abbvr, name) VALUES (?, ?)", y, answer["name"])
                            data[len(data) - 1]["language"].append(answer["name"])
                        else:
                            data[len(data) - 1]["language"].append(languages[y])
        # displaying it
        return render_template("search.html", message=data, query=request.form.get("name"), catagory=request.form.get("catagory"))


# shows detatiled info on book, when clicked
@app.route("/info", methods=["POST"])
@login_required
def info():
    book_id = request.form.get("book_id")
    book_id = book_id.replace("[", "").replace("]", "").replace("'", "").split(", ")
    if len(book_id) > 10:
        del book_id[10:]
    response = {}
    response.update(get_info(book_id))
    reading = db.execute("SELECT reading FROM users WHERE id = ?", session["user_id"])[0]["reading"]
    reading = reading.replace("[", "").replace("]", "").replace("'", "").split(", ") if reading else []
    cover = response["cover_link"]
    author = response["author_link"]
    response.pop("cover_link")
    response.pop("author_link")
    if not overlap(reading, book_id):
        return render_template("info.html", message=response, cover=cover, author=author, book_id=book_id)
    else:
        return render_template("info.html", message=response, cover=cover, author=author, book_id=None)


# this page is where you borrow a book and return it
@app.route("/borrow", methods=["GET", "POST"])
@login_required
def borrow():
    if request.method == "POST":
        due = ""
        unavailable = False
        book_id = request.form.get("book_id")
        book_id = book_id.replace("[", "").replace("]", "").replace("'", "").split(", ")
        if len(book_id) > 10:
            del book_id[10:]
        reading = db.execute("SELECT reading, Due FROM users")
        del reading[session["user_id"] - 1]
        for x in reading:
            if x["reading"]:
                x["reading"] = x["reading"].replace("[", "").replace("]", "").replace("'", "").split(", ")
            else:
                continue
            if overlap(x["reading"], book_id):
                unavailable = True
                due = x["Due"]
                break
        if unavailable:
            return render_template("borrow.html", book=None, message="2", due=due)
        if not db.execute("SELECT reading FROM users WHERE id = ?", session["user_id"])[0]["reading"]:
            db.execute("UPDATE users SET reading = ? WHERE id = ?", str(book_id), session["user_id"])
            db.execute("UPDATE users SET Due = ? WHERE id = ?", date.today() + timedelta(weeks=2), session["user_id"])
            response = {}
            response.update(get_info(book_id))
            cover = response["cover_link"]
            author = response["author_link"]
            response.pop("cover_link")
            response.pop("author_link")
            return render_template("borrow.html", message=response, cover=cover, author=author, due=date.today() + timedelta(weeks=2))
        else:
            return render_template("borrow.html", book=None, message="1", book_id=book_id)
    elif request.method == "GET":
        book_id = db.execute("SELECT reading FROM users WHERE id = ?", session["user_id"])[0]["reading"]
        if book_id:
            book_id = book_id.replace("[", "").replace("]", "").replace("'", "").split(", ")
            response = {}
            response.update(get_info(book_id))
            due = db.execute("SELECT Due FROM users WHERE id = ?", session["user_id"])[0]["Due"]
            cover = response["cover_link"]
            author = response["author_link"]
            response.pop("cover_link")
            response.pop("author_link")
            return render_template("borrow.html", message=response, cover=cover, author=author, due=due)
        else:
            return render_template("borrow.html", book=None)


# this route returns the book
@app.route("/return", methods=["POST"])
@login_required
def return_book():
    if request.form.get("book_id") == "None":
        db.execute("UPDATE users SET reading = ? WHERE id = ?", "", session["user_id"])
        db.execute("UPDATE users SET Due = ? WHERE id = ?", "", session["user_id"])
        return redirect("/borrow")
    else:
        book_id = request.form.get("book_id").replace("[", "").replace("]", "").replace("'", "").split(", ")
        db.execute("UPDATE users SET reading = ? WHERE id = ?", str(book_id), session["user_id"])
        db.execute("UPDATE users SET Due = ? WHERE id = ?", date.today() + timedelta(weeks=2), session["user_id"])
        return redirect("/borrow")


# common function to gett info - called frequently
def get_info(book_id):
    languages = {}
    for a in db.execute("SELECT * FROM languages"):
        languages[a["abbvr"]] = a["name"]
    response = {}
    for x in book_id:
        url = "https://openlibrary.org/books/" + x + ".json"
        data = requests.get(url)
        if data.status_code != 200:
            continue
        data = data.json()
        if "languages" in data.keys():
            data["languages"] = [languages[data["languages"][0]["key"][11:]]]
            if "languages" in response.keys() and data["languages"][0] not in response["languages"]:
                response["languages"].append(data["languages"][0])
                data.pop("languages")
        for y in response.keys():
            if y in data.keys():
                if y == "publishers" and data[y][0] not in response[y]:
                    response[y].append(data[y][0])
                    data.pop(y)
                else:
                    data.pop(y)
        response.update(data)
    response["names"] = []
    for x in response["authors"]:
        url = "https://openlibrary.org" + x["key"] + ".json"
        data = requests.get(url)
        if data.status_code != 200:
            continue
        data = data.json()
        response["names"].append(data["name"])
    url = "https://openlibrary.org" + response["works"][0]["key"] + ".json"
    data = requests.get(url)
    data = data.json()
    if "covers" in data.keys():
        response["cover_link"] = "https://covers.openlibrary.org/b/id/" + str(data["covers"][0]) + "-L.jpg"
    else:
        response["cover_link"] = ""
    if "authors" in data.keys():
        response["author_link"] = "https://covers.openlibrary.org/a/olid" + str(data["authors"][0]["author"]["key"][8:]) + "-L.jpg"
    else:
        response["author_link"] = ""
    response["work"] = data
    y = ["publishers", "title", "publish_date", "series", "description", "languages",  "number_of_pages", "genres", "first_sentence", "cover_link", "author_link", "work", "names"]
    data = response.copy()
    for x in data.keys():
        if x not in y:
            response.pop(x)
    z = ["subjects"] + list(set(y) - set(response.keys()))
    data = response["work"].copy()
    for x in data.keys():
        if x not in z:
            response["work"].pop(x)
    return response


def overlap(a, b):
    return len(set(a).intersection(set(b))) > 0


# checking if book is already due
@app.route("/overdue", methods=["GET"])
def overdue():
    book_id = db.execute("SELECT reading FROM users WHERE id = ?", session["user_id"])[0]["reading"]
    book = book_id.replace("[", "").replace("]", "").replace("'", "").split(", ")
    db.execute("UPDATE users SET reading = ? WHERE id = ?", "", session["user_id"])
    db.execute("UPDATE users SET Due = ? WHERE id = ?", "", session["user_id"])
    return render_template("borrow.html", book=None, message="3", book_id=book)


"""
Some information
The program uses a unique book id to identify each book
One book may have many ids but they to unique to it
In realtime a lot more data is collected on each book, but isnt displayed

A database is used to store username, encrypted passwords and common languages for the program to use

The API used is - openlibrary
https://openlibrary.org/
"""
