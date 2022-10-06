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
        return(jsonify(authentication=True, Email=email), 201)

def login():
    if request.method == "POST":
        email = request.form.get("Email")
        password = request.form.get("Password")
        if(sharedUserFunctionModel.login(email, password) == True):            
            return(jsonify(authentication=True, Email=email), 201)
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
            
            if bookModel.Send_book_offer(bookID, offer, offererEmail):
                return(jsonify("Successfully Sent Offer"), 201)
            else:
                return(jsonify("Error sending offer for Book"), 401)

def get_book_offers():
    if request.method == "POST":         
            bookID = request.form.get("BookID")
            ownerEmail = request.form.get("Email")
            userTableName = userModel.get_tablename()

            result = bookModel.get_book_offers(bookID, ownerEmail, userTableName)

            if type(result) == str and "Error" in result:

                return(jsonify(result), 401)

            else:

                return(jsonify(result), 201)

def accept_book_offer():
    if request.method == "POST":
        bookOfferID = request.form.get("BookOfferID")
        ownerEmail = request.form.get("Email")

        # checks if there are data input for the required fields 
        if bookOfferID is not None and ownerEmail is not None:
            if bookModel.accept_book_offer(bookOfferID, ownerEmail):
                return(jsonify("Successfully Accepted Offer"), 201)
            else:
                return(jsonify("Error Accepting offer for Book"), 401)
        
        else:
            return(jsonify("Error Accepting offer for Book"), 401)

            


