# Final-Project
#### The project entails a library management system designed to be used by the people who are enrolled in a library. All new users of the library are prompted to register into the application by providing a username and password.
#### After registering/logging in users can search, borrow and return books. The process is independent of the librarian and hence is convienient and snappy.
*The application is not only ment for borrowing and returning books, but also for browsing through the books in the library.*

### The app has three main parts:
- [Searching books](https://github.com/var-github/Final-Project/blob/main/README.md#search-books)
- [Borrowing books](https://github.com/var-github/Final-Project/blob/main/README.md#borrow-books)
- Returning books

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
The user can borrow a new book by logging in to their account, searching and selecting the borrow option on the Info page. All borrow requests are handled by the ***/borrow*** route. Books already borrowed by someone else cannot be borrowed until they return it and multiple books cannot be borrowed at the same time. All books have a due date of two weeks and must be returned within that time. Currently the application only extends the due date when it is returned late, fines and other punishments can be implemented by the library.<br />
Important information on the borrowed book will be displayed on the home and borrow page. The return option and due date are also present in the borrow page. The borrow page is characterised by the borrow.html file.........
