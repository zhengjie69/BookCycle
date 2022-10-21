from operator import contains
import os
from flask import jsonify, request, current_app
from ..models.book_model import Book
from werkzeug.utils import secure_filename
from datetime import datetime


bookmodel = Book()

# helper function to check for allowed files for upload
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# function to log and return result
# note that all result that is an error should be a string containing the word "Error" at the start
# for ipAddress, if ngix is used for production, request.environ.get('HTTP_X_REAL_IP', request.remote_addr) should be used to get ip
# actionDescription will be used for logging purposes

def return_result(ipAddress, actionDescription, functionCalled, result):
    
    print("----Log Test----")

    # who
    print("Who: {}".format(ipAddress))

    #what
    print("What: {}".format(actionDescription))

    #where
    print("Where: {}".format(functionCalled))

    #when
    now = datetime.now()
    print("When: {}".format(now))

    #result
    print("Result: {}".format(result))
    print("----------------")
    # checks if the result is an error result
    if type(result) == str and "Error" in result:
        return(jsonify(result), 401)
    else:
        return(jsonify(result), 201)



def get_all_genres():
    if request.method == "GET":
        #return (jsonify(bookmodel.get_all_genres()), 200)
        return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all genres", "get_all_genres", bookmodel.get_all_genres()))

        

def get_all_locations():
    if request.method == "GET":
        #return (jsonify(bookmodel.get_all_locations()), 200)
        return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all locations", "get_all_locations", bookmodel.get_all_locations()))
def get_all_book_conditions():
    if request.method == "GET":
        return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all book condition", "get_all_book_condition", bookmodel.get_all_book_conditions()))


def create_book():
    if request.method == "POST":
        title = request.form.get("Title")
        price = request.form.get("Price")
        description = request.form.get("Description")
        genreID = request.form.get("GenreID")
        email = request.form.get("Email")
        image = request.files['Image']
        locationID = request.form.get("LocationID")
        bookConditionID = request.form.get("BookConditionID")

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if image.filename == '':
            return (jsonify("No selected image"), 200)

        # if there is a image uploaded and the uploaded image format is accepted 
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            print(filename)
            if bookmodel.create_book(title, price, description, genreID, email, filename, locationID, bookConditionID):
                current_dir = str(os.getcwd() + '\\app\\' + current_app.config['UPLOAD_FOLDER'])
                # image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                image.save(os.path.join(current_dir, filename))
                
                #return(jsonify("Successfully Created Book"), 201)
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Creating a book", "create_book", "Successfully Created Book"))
            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Creating a book", "create_book", "Error failed to create Book"))
        else:
            #return(jsonify("Invalid File Type, Please only upload files with .jpg, .png"), 401)
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Error creating a book", "create_book", "Error , invalid File Type, Please only upload files with .jpg, .png"))

def search_book():
    if request.method == "GET":

        bookTitle = request.args.get("BookTitle")
        userEmail = request.args.get("Email")
        genreFilter = request.args.get("GenreFilter")
        locationFilter = request.args.get("LocationFilter")
        bookConditionFilter = request.args.get("BookConditionFilter")
        minPriceFilter = request.args.get("MinPriceFilter")
        maxPriceFilter = request.args.get("MaxPriceFilter")

        if bookTitle is not None and bookTitle == "null":
            bookTitle = None

        if userEmail is not None and userEmail == "null":
            userEmail = None
        
        if genreFilter is not None and genreFilter == "null":
            genreFilter = None

        if locationFilter is not None and locationFilter == "null":
            locationFilter = None
        
        if bookConditionFilter is not None and bookConditionFilter == "null":
            bookConditionFilter = None
        
        if minPriceFilter is not None and minPriceFilter == "null":
            minPriceFilter = None

        if maxPriceFilter is not None and maxPriceFilter == "null":
            maxPriceFilter = None    
        # checks if the result is an error result
        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Fetching books with or without filter", "search_books", bookmodel.search_book(bookTitle, userEmail, genreFilter, locationFilter, bookConditionFilter, minPriceFilter, maxPriceFilter))

def get_all_available_books():
    if request.method == "GET":

        userEmail = request.args.get("Email")
        genreFilter = request.args.get("GenreFilter")
        locationFilter = request.args.get("LocationFilter")
        bookConditionFilter = request.args.get("BookConditionFilter")
        minPriceFilter = request.args.get("MinPriceFilter")
        maxPriceFilter = request.args.get("MaxPriceFilter")

        # checks if the result is an error result
        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Fetching all avaliable books", "get_all_available_books", bookmodel.get_all_available_books(userEmail, genreFilter, locationFilter, bookConditionFilter, minPriceFilter, maxPriceFilter))

def get_all_user_books():
    if request.method == "GET":
        email = request.args.get("Email")
        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Fetching all user books", "get_all_user_books", bookmodel.get_all_user_books(email))

def search_book_by_title():
    if request.method == "GET":

        userEmail = request.args.get("Email")
        bookTitle = request.args.get("Title")

        #result = bookmodel.search_book_by_title(userEmail, bookTitle)

        # checks if the result is an error result
        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Searching book by title", "search_book_by_title", bookmodel.search_book_by_title(userEmail, bookTitle))


def update_book_details():
    if request.method == "POST":
        bookID = request.form.get("BookID")
        title = request.form.get("Title")
        price = request.form.get("Price")
        description = request.form.get("Description")
        genreID = request.form.get("GenreID")
        image = request.form.get("Image")
        locationID = request.form.get("LocationID")

        if image is not None and image == "null":
            image = None
        #return(jsonify(bookmodel.update_book_details(bookID, title, price, description, genreID, image, locationID)), 200)

        if bookID is not None and title is not None and price is not None and description is not None and genreID is not None and locationID is not None:
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Updating book details", "update_book_details", bookmodel.update_book_details(bookID, title, price, description, genreID, image, locationID))
        else:
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Updating book details", "update_book_details", "Error required values are empty")
def delete_book():
    if request.method == "POST":
        bookID = request.form.get("BookID")
        ownerEmail = request.form.get("Email")
        #return(jsonify(bookmodel.delete_book(bookID, ownerEmail)), 200)
        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Deleting book", "delete_book", bookmodel.delete_book(bookID, ownerEmail))


