# BookCycle

People often buy books to read, but after finishing them, they are frequently abandoned on the bookshelf. Therefore, the team has decided to create a platform for book recycling that allows users to donate or sell their books to another user. This not only frees up space for sellers to acquire new books, but also gives the book a new lease on life. 

By creating an account, the user can begin giving and selling books by listing the book's title, genre, price (if selling), description, condition, and location for collection. After listing a book, the user has the option to edit their listing information, change the book listing status, and delete the book listing. 

Users who are interested in looking for a book may search for the book on the website. Books that are available as listings will be displayed as search results, and the user can click the search results to view more details about the listings. All book listings will be tagged with a preferred MRT station which is available for the user to collect if they wish to acquire the book. 

To facilitate issues such as removing fraudulent book listings or disabling accounts, an administrator account can be used to perform the removal of books and the disabling of accounts. There will also be a super administrator who will oversee the creation and disabling of these administrator accounts. 

<h1>FrontEnd</h1>

Requirements:
Node.js v16.13.0

Visual Studio Code

Steps to run codes:
1. Open the BookCycle foler in VS Code
2. Open a terminal in VS Code
3. In the VS Code terminal, navigate to the frontend folder (cd .\frontend\)
4. Run the command: npm start

<h1>BackEnd</h1>

Requirements:
Python 3.10

Visual Studio Code

Steps to run project(windows):

1.On VS Code, open the BookCycle folder
2.Open a terminal in VS Code
3.In the VS Code terminal, navigate to the backend folder
4.In the VS Code terminal, run the command : py -m venv venv
5.In VS Code, click on the Python version on the bottom right corener of the IDE
6.Click on "Enter interpreter path" under "Select Interpreter"
7.Locate the "python.exe" file in BookCycle\backend\venv\scripts and select it
8.Click on "Select Interpreter"
9.In the VS Code terminal, run the command : venv\scripts\activate.bat
10.Ensure that the (venv) text is shown in front of the folder location in the terminal
11.In the VS Code terminal, run the command : pip install -r requirements.txt
12.In the VS Code terminal, run the command : flask run

Steps to use apis:

1.Refer to the paths in the files in routes folder (e.g. user_routes.py) to call the apis in the web browser
2.For commands that requires form data input, use postman for testing(with the postman desktop plugin)
3.For what data is required and it's key, refer to the files in the apis folder (e.g. user_api.py) to pass with the api
