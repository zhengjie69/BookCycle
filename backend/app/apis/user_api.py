from flask import jsonify, request
from ..models.user_model import User
from ..models.book_model import Book
from ..models.shared_user_functions_model import Shared_User_Functions
from ..models.data_cleaning import *
from .api_logger import *


userModel = User()
bookModel = Book()
sharedUserFunctionModel = Shared_User_Functions()

def create_User():
    if request.method == "POST":

        try:
            username = request.form.get("Username")
            email = request.form.get("Email")
            password = request.form.get("Password")
            contactNumber = request.form.get("ContactNumber")

            # checks if the data is empty or not and are strings
            if username is not None and email is not None and password is not None and contactNumber is not None and isstring(username) and isstring(email) and isstring(password) and isstring(contactNumber):

                # checks if the email is valid and contact Number is all numbers and length of contact number is 8 and if the email length exceeds SMTP limit (RFC 2821)
                if len(str(username)) <= 12 and isemail(email) and len(email) < 254 and len(str(password)) >= 8 and len(str(password)) <= 25 and isvalidpassword(password) and isint(contactNumber) and len(str(contactNumber)) == 8:


                    result = userModel.create_user(data_cleaning_without_space(username), email, password, contactNumber)
                    if "Error" in result:
                        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to create user account", "create_user", result)
                    else:

                        role = sharedUserFunctionModel.get_role(email)
                        return(jsonify(authentication=True, Email=email, Role=role), 201)
                
                else:
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to create user account", "create_user", "Error invalid input found")
            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to create user account", "create_user", "Error fields cannot be left blank")
        
        except Exception as ex:
            
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when creating user", "create_user", logMessage)
            return jsonify("Error Something went wrong, please try again later"), 401
def login():
    if request.method == "POST":

        try:
            email = request.form.get("Email")
            password = request.form.get("Password")

            # checks if the input is null or empty and is valid
            if email is not None and password is not None and isemail(email):

                if(sharedUserFunctionModel.login(email, password) == True): 

                    role = sharedUserFunctionModel.get_role(email)
                    if role is not None: 
                        return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting role for user during login", "get_role", "Successfully logged in")         
                        return(jsonify(authentication=True, Email=email, Role= role), 201)
                    else:
                        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting role for user during login", "get_role", "Error login failed")
                else:
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to login user", "login", "Error email or password is wrong")
            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to login user", "login", "Error fields cannot be left blank and must be valid inputs")
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when logging in", "login", logMessage)
            return jsonify("Something went wrong, please try again later"), 401

def get_user_profile():
    if request.method == "GET":

        try:
            email = request.args.get("Email")

            # checks if the input is null or empty and is valid
            if email is not None and isemail(email):
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting user profile", "get_user_profile", sharedUserFunctionModel.get_user_profile(email))
            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to get user profile", "get_user_profile", "Error fields cannot be left blank and must be valid inputs")
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when getting user profile", "get_user_profile", logMessage)
            return jsonify("Something went wrong, please try again later"), 401

def update_password():
    if request.method == "POST":

        try:
            userEmail = request.form.get("Email")
            oldPassword = request.form.get("OldPassword")
            newPassword = request.form.get("NewPassword")

            # checks if the input is null or empty and is valid
            if userEmail is not None and isemail(userEmail) and oldPassword is not None and newPassword is not None:

                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Updating user password", "update_password", sharedUserFunctionModel.update_password(userEmail, oldPassword, newPassword))
            
            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to update user password", "update_password", "Error fields cannot be left blank and must be valid inputs")
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when updating user password", "update_password", logMessage)
            return jsonify("Something went wrong, please try again later"), 401

def reset_password():
    pass

def update_profile():
     if request.method == "POST":

        try:
            email = request.form.get("Email")
            username = request.form.get("Username")
            contactNumber = request.form.get("ContactNumber")

            # checks if the input is null or empty and is valid
            if email is not None and isemail(email) and username is not None and contactNumber is not None:
                #return(jsonify(userModel.update_profile(email, username, contactNumber)), 200)
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Updating profile", "update_profile", userModel.update_profile(email, username, contactNumber))
            
            else:

                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to update profile", "update_profile", "Error fields cannot be left blank and must be valid inputs")
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when updating profile", "update_profile", logMessage)
            return jsonify("Something went wrong, please try again later"), 401


def send_book_offer():
    if request.method == "POST":
        try:         
            bookID = request.form.get("BookID")
            offererEmail = request.form.get("Email")
            offer = request.form.get("Offer")

            # checks if the input is null or empty and is valid
            if bookID is not None and isint(bookID) and offererEmail is not None and isemail(offererEmail) and offer is not None and isfloat(offer):
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Sending book offer", "send_book_offer", bookModel.send_book_offer(bookID, offer, offererEmail))

            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to send book offer", "send_book_offer", "Error fields cannot be left blank and must be valid inputs")
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when sending book offer", "send_book_offer", logMessage)
            return jsonify("Something went wrong, please try again later"), 401

def get_book_offers():
    if request.method == "GET":

        try:         
            bookID = request.args.get("BookID")
            ownerEmail = request.args.get("Email")
            userTableName = userModel.get_tablename()

            # checks if the input is null or empty and is valid
            if bookID is not None and isint(bookID) and ownerEmail is not None and isemail(ownerEmail) and userTableName is not None:
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting book offers", "get_book_offers", bookModel.get_book_offers(bookID, ownerEmail, userTableName))
            
            else:
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to get book offers", "get_book_offers", "Error fields cannot be left blank and must be valid inputs")
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when getting book offers", "get_book_offers", logMessage)
            return jsonify("Something went wrong, please try again later"), 401

def get_all_user_book_offers():
    if request.method == "GET":

        try: 
            email = request.args.get("Email")
            userTableName = userModel.get_tablename()
            transactionsTableName = userModel.get_transactionsTableName()

            # checks if the input is null or empty and is valid
            if email is not None and isemail(email) and userTableName is not None and transactionsTableName is not None:
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all book offers made by selected user email", "get_all_user_book_offers", bookModel.get_all_user_book_offers(email, userTableName, transactionsTableName))
            
            else:
           
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to get all book offers made by selected user email", "get_all_user_book_offers", "Error fields cannot be left blank and must be valid inputs")
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when getting all book offers made by selected user email", "get_all_user_book_offers", logMessage)
            return jsonify("Something went wrong, please try again later"), 401

def accept_book_offer():
    if request.method == "POST":

        try:
            bookOfferID = request.form.get("BookOfferID")
            ownerEmail = request.form.get("Email")

            # checks if the input is null or empty and is valid
            if bookOfferID is not None and isint(bookOfferID) and ownerEmail is not None and isemail(ownerEmail):
                result = bookModel.accept_book_offer(bookOfferID, ownerEmail)

                # checks if the book offer is successfully accepted, if successful, create transaction record
                if type(result) == str and "Error" in result:
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to accept book offer", "accept_book_offer", result)
                
                else:
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Creating trasaction after successfully accepting book offer", "accept_book_offer", userModel.create_transaction(result))

            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to accept book offer", "accept_book_offer", "Error fields cannot be left blank and must be valid inputs")    
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when accepting book offer", "accept_book_offer", logMessage)
            return jsonify("Something went wrong, please try again later"), 401        
            
def edit_book_offer():
    if request.method == "POST":

        try:
            bookOfferID = request.form.get("BookOfferID")
            offererEmail = request.form.get("Email")
            newOffer = request.form.get("Offer")

            # checks if the input is null or empty and is valid
            if bookOfferID is not None and isint(bookOfferID) and offererEmail is not None and isemail(offererEmail) and newOffer is not None and isfloat(newOffer):
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Editing book offer", "edit_book_offer", bookModel.edit_book_offer(bookOfferID, offererEmail, newOffer))
            
            else:

                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to Edit book offer", "edit_book_offer", "Error fields cannot be left blank and must be valid inputs")

        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when editing book offer", "edit_book_offer", logMessage)
            return jsonify("Something went wrong, please try again later"), 401         

def delete_book_offer():
    if request.method == "POST":

        try:
            bookOfferID = request.form.get("BookOfferID")
            offererEmail = request.form.get("Email")

            # checks if the input is null or empty and is valid
            if bookOfferID is not None and isint(bookOfferID) and offererEmail is not None and isemail(offererEmail):
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Deleting book offer", "delete_book_offer", bookModel.delete_book_offer(bookOfferID, offererEmail))
            
            else:
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to book offer", "delete_book_offer", "Error fields cannot be left blank and must be valid inputs")
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception deleting book offer", "delete_book_offer", logMessage)
            return jsonify("Something went wrong, please try again later"), 401    

def get_transaction_details():
        if request.method == "GET": 

            try:
                transactionID = request.args.get("TransactionID")

                # checks if the input is null or empty and is valid
                if transactionID is not None and isint(transactionID):

                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting transcation details of a specific transcation", "get_transaction_details", userModel.get_transaction_details(transactionID))

                else:

                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to get transcation details of a specific transcation", "get_transaction_details", "Error fields cannot be left blank and must be valid inputs")
            
            except Exception as ex:
                # logs the error log and returns a error message
                logMessage = "Exception Error " + str(ex)
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when getting transcation details of a specific transcation", "get_transaction_details", logMessage)
                return jsonify("Something went wrong, please try again later"), 401    

def get_all_user_transactions():
     if request.method == "GET":

        try:
            email = request.args.get("Email")

            # checks if the input is null or empty and is valid
            if email is not None and isemail(email):
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all user transcations made by selected user email", "get_all_user_transcations", userModel.get_all_user_transactions(email))
            
            else:
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to get all user transcations made by selected user email", "get_all_user_transcations", "Error fields cannot be left blank and must be valid inputs")

        except Exception as ex:
                # logs the error log and returns a error message
                logMessage = "Exception Error " + str(ex)
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when getting all user transcations made by selected user email", "get_all_user_transcations", logMessage)
                return jsonify("Something went wrong, please try again later"), 401                    