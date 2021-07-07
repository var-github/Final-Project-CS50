# Final-Project
#### The project entails a library management system designed to be used by the people who are enrolled in a library. All new users of the library are prompted to register into the application by providing a username and password.
#### After registering/logging in users can search, borrow and return books. The process is independent of the librarian and hence is convienient and snappy.
*The application is not only ment for borrowing and returning books, but also for browsing through the books in the library.*

&nbsp;
### The app has three main parts:
- [Searching books](https://github.com/var-github/Final-Project/blob/main/README.md#search-books)
- Borrowing books
- Returning books

### *Search Books*
Searching books is one of the main tasks the application handles and to do so the application uses an [API](https://openlibrary.org/developers/api). The API provides a list of books and some basic information on them.
The search.html page acts as the user interface to search books. In search.html the category in which you want to search and the keyword to search are taken as input. This is then formatted and submited to the API. The API returns json file with necessary information related to the query. This file is processed and important information are displayed. <br />
The entire process of searching and displaying happens in ***/search*** route.

The info.html page is displayed when one of the books from the search results is selected. This page shows more detailed information on the book along with cover page and author picture if available. Books can be borrowed from this page. <br />
Incase a book is searched by its isbn number the book is directly displayed on the info page.

***On the inside each book is identified by its book id provided by the API.***

