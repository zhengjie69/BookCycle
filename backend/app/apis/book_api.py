import os
from flask import jsonify, request, current_app
import random
import string

from app.models.data_cleaning import *
from ..models.book_model import Book
from .api_logger import *

bookmodel = Book()

# helper function to check for allowed files for upload
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_filename(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# helper function to check for the image file in storage
def find_image(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None

def validate_filter(filterID):
    # validate the filter id
        if filterID is not None and filterID == "null":
            filterID = None
        
        # if Filter id is not a integer, set to none, else convert value to int and set to variable
        elif filterID is not None and filterID != "null" and isint(filterID):
            filterID = int(filterID)
        
        else:
            filterID = None
        
        return filterID

def get_all_genres():
    if request.method == "GET":

        try:
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all genres", "get_all_genres", bookmodel.get_all_genres()))
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when getting all genres", "get_all_genres", logMessage)
            return jsonify("Something went wrong, please try again later"), 401     
        

def get_all_locations():
    if request.method == "GET":

        try:
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all locations", "get_all_locations", bookmodel.get_all_locations()))
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when getting all locations", "get_all_locations", logMessage)
            return jsonify("Something went wrong, please try again later"), 401

def get_all_book_conditions():
    if request.method == "GET":

        try:
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all book condition", "get_all_book_condition", bookmodel.get_all_book_conditions()))
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when getting all book condition", "get_all_book_condition", logMessage)
            return jsonify("Something went wrong, please try again later"), 401

def create_book():
    if request.method == "POST":

        try:
            title = request.form.get("Title")
            price = request.form.get("Price")
            description = request.form.get("Description")
            genreID = request.form.get("GenreID")
            email = request.form.get("Email")
            image = request.files['Image']
            locationID = request.form.get("LocationID")
            bookConditionID = request.form.get("BookConditionID")

            # checks if the input is null or empty
            if title is not None and price is not None and description is not None and genreID is not None and email is not None and image is not None and locationID is not None and bookConditionID is not None:
                
                # validates if the data is in the right type
                if isstring(title) and isfloat(price) and isstring(description) and isint(genreID) and isemail(email) and isint(locationID) and isint(bookConditionID):

                    # If the user does not select a file, the browser submits an
                    # empty file without a filename.
                    if image.filename == '':
                        return (jsonify("No selected image"), 200)

                    # if there is a image uploaded and the uploaded image format is accepted 
                    if image and allowed_file(image.filename):

                        # retrieves the file extension
                        imageExtension = image.filename.split(".")[1]
                        filename = generate_filename(8) + "." + imageExtension

                        print(filename)
                        result = bookmodel.create_book(title, price, description, genreID, email, filename, locationID, bookConditionID)
                        
                        # if the book listing is successfully created, insert uploaded image into storage
                        if "Error" not in result:
                            current_dir = str(os.getcwd() + '\\app\\' + current_app.config['UPLOAD_FOLDER'])
                            # image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                            image.save(os.path.join(current_dir, filename))
                            
                            #return(jsonify("Successfully Created Book"), 201)
                            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Creating a book", "create_book", "Successfully Created Book"))
                        else:
                            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to create a book", "create_book", "Error failed to create Book, please try again"))
                    else:
                        #return(jsonify("Invalid File Type, Please only upload files with .jpg, .png"), 401)
                        return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to create a book", "create_book", "Error , invalid File Type, Please only upload files with .jpg, .png"))
                
                else:
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to create a book", "create_book", "Error invalid input found"))        
            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to create a book", "create_book", "Error fields cannot be left blank"))
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when creating a book", "create_book", logMessage)
            return jsonify("Something went wrong, please try again later"), 401
        
def search_book():
    if request.method == "GET":
        try:
            bookTitle = request.args.get("BookTitle")
            userEmail = request.args.get("Email")
            genreFilter = request.args.get("GenreFilter")
            locationFilter = request.args.get("LocationFilter")
            bookConditionFilter = request.args.get("BookConditionFilter")
            minPriceFilter = request.args.get("MinPriceFilter")
            maxPriceFilter = request.args.get("MaxPriceFilter")

            # validate the booktitle
            if bookTitle is not None and bookTitle == "null":
                bookTitle = None
            
            elif bookTitle is not None and bookTitle != "null":
                bookTitle = data_cleaning_with_space(bookTitle)
            
            else:
                bookTitle = None

            # validate the user email
            if userEmail is not None and userEmail == "null":
                userEmail = None

            elif userEmail is not None and userEmail != "null" and isemail(userEmail):
                userEmail = userEmail
            
            else:
                userEmail = None
            
            # sets the values if it is a valid filter id
            genreFilter = validate_filter(genreFilter)
            locationFilter = validate_filter(locationFilter)
            bookConditionFilter = validate_filter(bookConditionFilter)

            

            # validate the minPriceFilter 
            if minPriceFilter is not None and minPriceFilter == "null":
                minPriceFilter = None
            
            # if minPriceFilter is not a integer, set to none, else convert value to int and set to variable
            elif minPriceFilter is not None and minPriceFilter != "null" and isfloat(minPriceFilter):
                minPriceFilter = int(minPriceFilter)
            
            else:
                minPriceFilter = None

            # validate the maxPriceFilter 
            if maxPriceFilter is not None and maxPriceFilter == "null":
                maxPriceFilter = None

            # if maxPriceFilter is not a integer, set to none, else convert value to int and set to variable
            elif maxPriceFilter is not None and maxPriceFilter != "null" and isfloat(maxPriceFilter):
                maxPriceFilter = int(maxPriceFilter)
            
            else:
                maxPriceFilter = None


            # checks if the result is an error result
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Fetching books with or without filter", "search_books", bookmodel.search_book(bookTitle, userEmail, genreFilter, locationFilter, bookConditionFilter, minPriceFilter, maxPriceFilter))
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when fetching books with or without a filter", "search_books", logMessage)
            return jsonify("Something went wrong, please try again later"), 401    


def get_all_user_books():
    if request.method == "GET":

        try:
            email = request.args.get("Email")

            if email is not None and isemail(email):
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Fetching all user books", "get_all_user_books", bookmodel.get_all_user_books(email))
            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to fetch all user books", "get_all_user_books", "Error invalid input found")

        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when fetching all user books", "get_all_user_books", logMessage)
            return jsonify("Something went wrong, please try again later"), 401        


def update_book_details():
    if request.method == "POST":

        try:
            bookID = request.form.get("BookID")
            title = request.form.get("Title")
            price = request.form.get("Price")
            description = request.form.get("Description")
            genreID = request.form.get("GenreID")
            image = request.files['Image']
            locationID = request.form.get("LocationID")
            bookConditionID = request.form.get("BookConditionID")

            if image is not None and image == "null":
                image = None
            

            # checks if the input is null or empty
            if bookID is not None and title is not None and price is not None and description is not None and genreID is not None and locationID is not None and bookConditionID is not None:

                if isint(bookID) and isstring(title) and isfloat(price) and isstring(description) and isint(genreID) and isint(locationID) and isint(bookConditionID):
                    
                    # generates the new image name and gets the old image name for deletion below
                    newImageName = generate_filename(8)
                    oldImageName = bookmodel.get_book_image_name(bookID)
                    result = bookmodel.update_book_details(bookID, title, price, description, genreID, newImageName, locationID, bookConditionID)

                    # uploads the image into storage if update is successful and the file upload is not none
                    if "Error" not in result and image is not None:

                        # if there is a image uploaded and the uploaded image format is accepted 
                        if image and allowed_file(image.filename):
                            
                            # if a new image is uploaded, old image is deleted before adding new image
                            current_dir = str(os.getcwd() + '\\app\\' + current_app.config['UPLOAD_FOLDER'])
                            

                            # searches for the old image in the file system
                            # if no old image, upload the new image
                            if find_image(oldImageName, current_dir):

                                os.remove(os.path.join(current_dir, oldImageName))
                                image.save(os.path.join(current_dir, newImageName))

                            else:
                                image.save(os.path.join(current_dir, newImageName))

                            # current_dir = str(os.getcwd() + '\\app\\' + current_app.config['UPLOAD_FOLDER'])
                            # image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    
                    else:
                        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Updating book details", "update_book_details", result)
                
                else:
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to update book details", "update_book_details", "Error invalid input found")

            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to update book details", "update_book_details", "Error required values are empty")
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when updating book details", "update_book_details", logMessage)
            return jsonify("Something went wrong, please try again later"), 401

def delete_book():
    if request.method == "POST":

        try:
            bookID = request.form.get("BookID")
            ownerEmail = request.form.get("Email")

            if bookID is not None and ownerEmail is not None:

                if isint(bookID) and isemail(ownerEmail):

                    # gets the image name before deletion
                    imagename = bookmodel.get_book_image_name(bookID)

                    result = bookmodel.delete_book(bookID, ownerEmail)

                    # prepares to delete the image from storage if record is successfully deleted
                    if "Error" not in result:

                        print("image name is")
                        print(imagename)
                        current_dir = str(os.getcwd() + '\\app\\' + current_app.config['UPLOAD_FOLDER'])
                        # searches for the image in the file system
                        # if found, delete the image
                        if find_image(imagename, current_dir):
                            os.remove(os.path.join(current_dir, imagename))

                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Deleting book", "delete_book", result)
                
                else:
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to delete book", "delete_book", "Error invalid input found")
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when deleting book", "delete_book", logMessage)
            return jsonify("Something went wrong, please try again later"), 401 

