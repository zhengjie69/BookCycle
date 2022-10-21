from flask import jsonify, request
from ..models.user_model import User
from ..models.book_model import Book
from ..models.shared_user_functions_model import Shared_User_Functions
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

  
        print("username: {}".format(username))
        print("email: {}".format(email))
        print("password: {}".format(password))
        print("contactNumber: {}".format(contactNumber))

        result = userModel.create_user(username, email, password, contactNumber)
        if "Error" in result:
             return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Creating user account", "create_user", result)
        else:

            role = sharedUserFunctionModel.get_role(email)
            return(jsonify(authentication=True, Email=email, Role=role), 201)

def login():
    if request.method == "POST":
        email = request.form.get("Email")
        password = request.form.get("Password")
        if(sharedUserFunctionModel.login(email, password) == True): 

            role = sharedUserFunctionModel.get_role(email)
            if role is not None:          
                return(jsonify(authentication=True, Email=email, Role= role), 201)
            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting role for user during login", "get_role", "Error loggin failed")
        else:
            return(jsonify(message='Invalid Email or Password'), 401)

def get_user_profile():
    if request.method == "GET":
        email = request.args.get("Email")
        #return(jsonify(userModel.get_user_profile(email)), 200)
        return(jsonify(sharedUserFunctionModel.get_user_profile(email)), 200)

def update_password():
    if request.method == "POST":
        userEmail = request.form.get("Email")
        oldPassword = request.form.get("OldPassword")
        newPassword = request.form.get("NewPassword")
        #return(jsonify(userModel.update_password(oldPassword, newPassword)), 200)
        return(jsonify(sharedUserFunctionModel.update_password(userEmail, oldPassword, newPassword)), 200)

def reset_password():
    pass

def update_profile():
     if request.method == "POST":
        email = request.form.get("Email")
        username = request.form.get("Username")
        contactNumber = request.form.get("ContactNumber")
        return(jsonify(userModel.update_profile(email, username, contactNumber)), 200)

def send_book_offer():
    if request.method == "POST":         
            bookID = request.form.get("BookID")
            offererEmail = request.form.get("Email")
            offer = request.form.get("Offer")
            
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Sending book offer", "send_book_offer", bookModel.send_book_offer(bookID, offer, offererEmail))

def get_book_offers():
    if request.method == "GET":         
            bookID = request.args.get("BookID")
            ownerEmail = request.args.get("Email")
            userTableName = userModel.get_tablename()

            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting book offer", "get_book_offers", bookModel.get_book_offers(bookID, ownerEmail, userTableName))

def get_all_user_book_offers():
    if request.method == "GET": 
            email = request.args.get("Email")
            userTableName = userModel.get_tablename()
            transactionsTableName = userModel.get_transactionsTableName()
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all book offers made by selected user email", "get_all_user_book_offers", bookModel.get_all_user_book_offers(email, userTableName, transactionsTableName))

def accept_book_offer():
    if request.method == "POST":
        bookOfferID = request.form.get("BookOfferID")
        ownerEmail = request.form.get("Email")

        result = bookModel.accept_book_offer(bookOfferID, ownerEmail)

        if type(result) == str and "Error" in result:
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Accepting book offer", "accept_book_offer", result)
        
        else:
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Accepting book offer", "accept_book_offer", userModel.create_transaction(result))
            
            
def edit_book_offer():
    if request.method == "POST":
        bookOfferID = request.form.get("BookOfferID")
        offererEmail = request.form.get("Email")
        newOffer = request.form.get("Offer")

        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Editing book offer", "edit_book_offer", bookModel.edit_book_offer(bookOfferID, offererEmail, newOffer))

def delete_book_offer():
    if request.method == "POST":
        bookOfferID = request.form.get("BookOfferID")
        offererEmail = request.form.get("Email")

        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Deleting book offer", "delete_book_offer", bookModel.delete_book_offer(bookOfferID, offererEmail))

def get_transaction_details():
        if request.method == "GET": 
            transactionID = request.args.get("TransactionID")
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting transcation detail of a specific transcation", "get_transaction_details", userModel.get_transaction_details(transactionID))

def get_all_user_transactions():
     if request.method == "GET": 
            email = request.args.get("Email")
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all user transcations made by selected user email", "get_all_user_transcations", userModel.get_all_user_transactions(email))