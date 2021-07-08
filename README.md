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
## *Other files*
#### **1.layout.html**
It houses the basic structure for all other html files. Contains the navigation bar, byline and other visual details, and is a template for the other files.
#### **2.base.html**
The search page is a host for a lot of program, due to its many functionalities and hence has its own template - base.html. This file is very similar to the layout file, but has few tweaks to accomplish its tasks.
#### **3.login.html**

#### **4.register.html**

#### **5.display.html**

#### **6.register.html**

#### **7.index.html**

#### **8.helpers.py**

#### **9.info.db**

#### **10.styles.css**
