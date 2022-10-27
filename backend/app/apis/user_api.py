from flask import jsonify, request
from ..models.user_model import User
from ..models.book_model import Book
from ..models.shared_user_functions_model import Shared_User_Functions
from ..models.data_cleaning import *
from datetime import datetime


userModel = User()
bookModel = Book()
sharedUserFunctionModel = Shared_User_Functions()

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

    logMessage = "{} -- {} -- {} -- {} -- {}".format(ipAddress, actionDescription, functionCalled, now, result)
    

    # checks if the result is an error result
    if type(result) == str and "Error" in result:
        return(jsonify(result), 401)
    else:
        return(jsonify(result), 201)




def create_User():
    if request.method == "POST":
        username = request.form.get("Username")
        email = request.form.get("Email")
        password = request.form.get("Password")
        contactNumber = request.form.get("ContactNumber")

        # checks if the data is empty or not
        if username is not None and email is not None and password is not None and contactNumber is not None:

            # checks if the email is valid and contact Number is all numbers and length of contact number is 8 and if the email length exceeds SMTP limit (RFC 2821)
            if len(str(username)) <= 12 and isemail(email) and len(email) < 254 and len(str(password)) >= 8 and len(str(password)) <= 25 and isint(contactNumber) and len(str(contactNumber)) == 8:


                result = userModel.create_user(username, email, password, contactNumber)
                if "Error" in result:
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Creating user account", "create_user", result)
                else:

                    role = sharedUserFunctionModel.get_role(email)
                    return(jsonify(authentication=True, Email=email, Role=role), 201)
            
            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Creating user account", "create_user", "Error invalid input found")
        else:
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Creating user account", "create_user", "Error fields cannot be left blank")

def login():
    if request.method == "POST":
        email = request.form.get("Email")
        password = request.form.get("Password")

        # checks if the input is null or empty and is valid
        if email is not None and password is not None and isemail(email):

            if(sharedUserFunctionModel.login(email, password) == True): 

                role = sharedUserFunctionModel.get_role(email)
                if role is not None:          
                    return(jsonify(authentication=True, Email=email, Role= role), 201)
                else:
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting role for user during login", "get_role", "Error login failed")
            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting role for user during login", "get_role", "Error email or password is wrong")
        else:
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting role for user during login", "get_role", "Error fields cannot be left blank and must be valid inputs")

def get_user_profile():
    if request.method == "GET":
        email = request.args.get("Email")

        # checks if the input is null or empty and is valid
        if email is not None and isemail(email):
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting user profile", "get_user_profile", sharedUserFunctionModel.get_user_profile(email))
        else:
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting user profile", "get_user_profile", "Error fields cannot be left blank and must be valid inputs")

def update_password():
    if request.method == "POST":
        userEmail = request.form.get("Email")
        oldPassword = request.form.get("OldPassword")
        newPassword = request.form.get("NewPassword")

        # checks if the input is null or empty and is valid
        if userEmail is not None and isemail(userEmail) and oldPassword is not None and newPassword is not None:

            #return(jsonify(sharedUserFunctionModel.update_password(userEmail, oldPassword, newPassword)), 200)
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Updating user password", "update_password", sharedUserFunctionModel.update_password(userEmail, oldPassword, newPassword))
        
        else:
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Updating user password", "update_password", "Error fields cannot be left blank and must be valid inputs")

def reset_password():
    pass

def update_profile():
     if request.method == "POST":
        email = request.form.get("Email")
        username = request.form.get("Username")
        contactNumber = request.form.get("ContactNumber")

        # checks if the input is null or empty and is valid
        if email is not None and isemail(email) and username is not None and contactNumber is not None:
            #return(jsonify(userModel.update_profile(email, username, contactNumber)), 200)
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Updating profile", "update_profile", userModel.update_profile(email, username, contactNumber))
        
        else:

            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Updating profile", "update_profile", "Error fields cannot be left blank and must be valid inputs")


def send_book_offer():
    if request.method == "POST":         
            bookID = request.form.get("BookID")
            offererEmail = request.form.get("Email")
            offer = request.form.get("Offer")

            # checks if the input is null or empty and is valid
            if bookID is not None and isint(bookID) and offererEmail is not None and isemail(offererEmail) and offer is not None and isfloat(offer):
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Sending book offer", "send_book_offer", bookModel.send_book_offer(bookID, offer, offererEmail))

            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Sending book offer", "send_book_offer", "Error fields cannot be left blank and must be valid inputs")

def get_book_offers():
    if request.method == "GET":         
            bookID = request.args.get("BookID")
            ownerEmail = request.args.get("Email")
            userTableName = userModel.get_tablename()

            # checks if the input is null or empty and is valid
            if bookID is not None and isint(bookID) and ownerEmail is not None and isemail(ownerEmail) and userTableName is not None:
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting book offer", "get_book_offers", bookModel.get_book_offers(bookID, ownerEmail, userTableName))
            
            else:
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting book offer", "get_book_offers", "Error fields cannot be left blank and must be valid inputs")

def get_all_user_book_offers():
    if request.method == "GET": 
            email = request.args.get("Email")
            userTableName = userModel.get_tablename()
            transactionsTableName = userModel.get_transactionsTableName()

            # checks if the input is null or empty and is valid
            if email is not None and isemail(email) and userTableName is not None and transactionsTableName is not None:
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all book offers made by selected user email", "get_all_user_book_offers", bookModel.get_all_user_book_offers(email, userTableName, transactionsTableName))
            
            else:
           
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all book offers made by selected user email", "get_all_user_book_offers", "Error fields cannot be left blank and must be valid inputs")

def accept_book_offer():
    if request.method == "POST":
        bookOfferID = request.form.get("BookOfferID")
        ownerEmail = request.form.get("Email")

        # checks if the input is null or empty and is valid
        if bookOfferID is not None and isint(bookOfferID) and ownerEmail is not None and isemail(ownerEmail):
            result = bookModel.accept_book_offer(bookOfferID, ownerEmail)

            if type(result) == str and "Error" in result:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Accepting book offer", "accept_book_offer", result)
            
            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Accepting book offer", "accept_book_offer", userModel.create_transaction(result))

        else:
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Accepting book offer", "accept_book_offer", "Error fields cannot be left blank and must be valid inputs")    
            
def edit_book_offer():
    if request.method == "POST":
        bookOfferID = request.form.get("BookOfferID")
        offererEmail = request.form.get("Email")
        newOffer = request.form.get("Offer")

        # checks if the input is null or empty and is valid
        if bookOfferID is not None and isint(bookOfferID) and offererEmail is not None and isemail(offererEmail) and newOffer is not None and isfloat(newOffer):
            
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Editing book offer", "edit_book_offer", bookModel.edit_book_offer(bookOfferID, offererEmail, newOffer))
        
        else:

            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Editing book offer", "edit_book_offer", "Error fields cannot be left blank and must be valid inputs")

def delete_book_offer():
    if request.method == "POST":
        bookOfferID = request.form.get("BookOfferID")
        offererEmail = request.form.get("Email")

        # checks if the input is null or empty and is valid
        if bookOfferID is not None and isint(bookOfferID) and offererEmail is not None and isemail(offererEmail):
            
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Deleting book offer", "delete_book_offer", bookModel.delete_book_offer(bookOfferID, offererEmail))
        
        else:
            
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Deleting book offer", "delete_book_offer", "Error fields cannot be left blank and must be valid inputs")

def get_transaction_details():
        if request.method == "GET": 
            transactionID = request.args.get("TransactionID")

            # checks if the input is null or empty and is valid
            if transactionID is not None and isint(transactionID):

                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting transcation detail of a specific transcation", "get_transaction_details", userModel.get_transaction_details(transactionID))

            else:

                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting transcation detail of a specific transcation", "get_transaction_details", "Error fields cannot be left blank and must be valid inputs")

def get_all_user_transactions():
     if request.method == "GET": 
            email = request.args.get("Email")

            # checks if the input is null or empty and is valid
            if email is not None and isemail(email):
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all user transcations made by selected user email", "get_all_user_transcations", userModel.get_all_user_transactions(email))
            
            else:
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all user transcations made by selected user email", "get_all_user_transcations", "Error fields cannot be left blank and must be valid inputs")