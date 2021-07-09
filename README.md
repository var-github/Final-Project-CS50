# Final-Project
#### The project entails a library management system designed to be used by the people who are enrolled in the library. All new users of the library are prompted to register into the application by providing a username and password.
#### After registering/logging in users can search, borrow and return books. The process is independent of the librarian and hence is convienient and snappy.
*The application is not only meant for borrowing and returning books, but also for browsing through the books in the library.*

### The app has three main parts:
- [Searching books](https://github.com/var-github/Final-Project/blob/main/README.md#search-books)
- [Borrowing books](https://github.com/var-github/Final-Project/blob/main/README.md#borrow-books)
- [Returning books](https://github.com/var-github/Final-Project/blob/main/README.md#return-books)

&nbsp;
## *Search Books*
Searching books is one of the main tasks the application handles and to do so the application uses an [API](https://openlibrary.org/developers/api). The API provides a list of books and some basic information on them.
The search.html page acts as the user interface to search books. In search.html the category in which you want to search and the keyword to search are taken as input. This is then formatted and submited to the API. The API returns json file with necessary information related to the query. This file is processed and important information are displayed. <br />
Books can be searched in the ***general category*** or by its:-
- Name
- Author
- ISBN

The info.html page is displayed when one of the books from the search results is selected. This page shows more detailed information on the book along with cover page and author picture if available. Books can be borrowed from this page.

The entire process of searching and displaying books happen in ***/search*** route.

## *Borrow Books*
The user can borrow a new book by logging in to their account, searching and selecting the borrow option on the Info page. All borrow requests are handled by the ***/borrow*** route. Books already borrowed by someone else cannot be borrowed until they return it. The application also dosent allow multiple books to be borrowed and will ask the user if he wants to return the previous book before borrowing another. All books have a due date of two weeks and must be returned within that time. Currently the application only extends the due date when it is returned late, fines and other punishments can be implemented by the library.<br />
The borrow page is characterised by the borrow.html file that displays important information on the borrowed book along with the return option and due date.

## *Return Books*
To return a book the user has to navigate to the borrow page after signing in to their account. The borrow page displays the book you are currently reading and has the return option. Upon clicking the return option you will be redirected to a ***/return*** route - which returns the book and takes you to the home page.<br />
From here new book scan be borrowed by navigating to the search column.<br />
It must be noted that if the book is already due the system will return it and ask for confirmation if you want to borrow it for another two week.

&nbsp;
## *Helper files*
#### **1. Layout.html**
It houses the basic structure for all other html files. Contains the navigation bar, byline and other visual details, and is a template for the other files.
#### **2. Base.html**
The search page is a host for a lot of program, due to its many functionalities and hence has its own template - base.html. This file is very similar to the layout file, but has few tweaks to accomplish its tasks.
#### **3. Login.html**
This file operates in the /login route and displays the interface to login to an existing account
#### **4. Register.html**
This file displays the register page and submits the information to the /register route
#### **5. Display.html**
This page acts like a notification page and displays any error that occur during the login or register process. Wrong password and wrong username errors are also shown here
#### **6. Index.html**
The home page is characterised by this file. It displays relevent information on the borrowed book and puts up a medium to perform other functions

## *Application.py*
This file is the crux of the entire web application and contains all the back end programming and logic. The app has nine routes:
- Main route (/)
- Login route (/login)
- Logout route (/logout)
- Register route (/register)
- Search route (/search)
- Info route (/info)
- Borrow route (/borrow)
- Return route (/return)
- Due route (/overdue)

Along with these routes there is an info function which looks up the api and returns a dictionary with the formatted information. The formatted information is then processed by the concerning route. This framework extends to helpers.py that is reponsible for checking if a person is logged in. The libraries that are used in this file are mentioned in the ***requirements.txt*** file.

&nbsp;
## *General process*
1. Login to your account
2. Return the previous book (if borrowed) from the borrow page
3. Then locate the book by searching it via the search page
4. After selecting the book from the search results click on the borrow option on the info page
5. Happy reading - logout

### *Things to remember*
- Due date is set to two weeks, so return it before that<br />
- Logout after use or someone else can use your account

&nbsp;
## Video description

