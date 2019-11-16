# Project 1

Check the [video clip](https://v.youku.com/v_show/id_XNDQzMzA5MzQ4OA==.html?spm=a2hzp.8244740.0.0).

All the requirements are met. The backend codes are in "application.py". And the pages are in /templates folder.

- [x] Registration: Users should be able to register for your website, providing (at minimum) a username and password.
    - Open the main page, if you have not registered, you can click <kbd>Sign up now</kbd> to sign up. Username and password are required.
- [x] Login: Users, once registered, should be able to log in to your website with their username and password.
    - Once you have an accout, you can log in using the username and password on /login page. 
- [x] Logout: Logged in users should be able to log out of the site.
    - There is a <kbd>Logout</kbd> button on top of the page. You can click it to log out any time.
- [x] Import: Provided for you in this project is a file called books.csv, which is a spreadsheet in CSV format of 5000 different books. 
    - The books.csv have already been uploaded to the database. I used `pandas` to do the trick.
- [x] Search: Once a user has logged in, they should be taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!
    - After login, you are redirected to /index page, where you can search for specific books. You can apply multiple conditions before clicking the <kbd>Search</kbd> button.
- [x] Book Page: When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
    - All the required information will be shown on the /book/<int:book_id> page, including the given info and the information retrieved from Goodreads. The reviews by users are shown below the book info.
- [x] Review Submission: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
    - You can submit a rating as well as your comments for a book. But if you have submitted it, the <kdb>Submit</kbd> button will be disabled.
- [x] Goodreads Review Data: On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.
    - Yes, it is shown along with the book info.
- [x] API Access: If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. If the requested ISBN number isn’t in your database, your website should return a 404 error.
    - You can access to the book info json by /api/book?isbn=isbn.
