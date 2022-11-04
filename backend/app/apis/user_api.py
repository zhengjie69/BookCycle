from flask import jsonify, request,render_template, session
from flask_mail import Message
from ..models.user_model import User
from ..models.book_model import Book
from ..models.shared_user_functions_model import Shared_User_Functions
from ..models.data_cleaning import *
from .api_logger import *
import requests
import json
from flask import current_app


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
                if len(str(username)) <= 12 and isemail(email) and len(email) < 254 and \
                        len(str(password)) >= 8 and len(str(password)) <= 25 and \
                        isvalidpassword(password) and isint(contactNumber) and len(str(contactNumber)) == 8:


                    result = userModel.create_user(data_cleaning_without_space(username), email, password, contactNumber)
                    if "Error" in result:
                        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to create user account", "create_user", result)
                    else:

                        role = sharedUserFunctionModel.get_role(email)
                        if role is not None:
                            

                            session["email"] = email
                            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                                         "User account successfully created with the username "+email, "create_user",
                                         "Successful User Creation")
                            return(jsonify(authentication=True, Email=email, Role=role), 201)
                        
                        else:
                            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to get row after create user account", "create_user", "Error invalid role found")
                
                else:
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to create user account with the username"+email, "create_user", "Error invalid input found")
            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to create user account with the username"+email, "create_user", "Error fields cannot be left blank")
        
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

                result = sharedUserFunctionModel.login(email, password)
                if "Success" in result: 

                    role = sharedUserFunctionModel.get_role(email)
                    if role is not None: 
                        return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Sucessful Login by "+email, "get_role", "Successfully logged in")
                        session["email"] = email
                        return(jsonify(authentication=True, Email=email, Role= role), 201)
                    else:
                        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting role for user during login", "get_role", "Error login failed")
                else:
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to login user. Username used by login is"+email, "login", result)
            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to login user. Username used by login is"+email, "login", "Error fields cannot be left blank and must be valid inputs")
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when logging in", "login", logMessage)
            return jsonify("Something went wrong, please try again later"), 401

def logout():
    if request.method == "POST":

        try:
            email = request.form.get("Email")
            if session.get("email") is not None:
                session.clear()
                return jsonify(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Successful Logging out by"+email, "logout", "Successfully logged out"))
            
            else:
                return jsonify(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to log out", "logout", "Error Not logged in"))

        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when logging out", "logout", logMessage)
            return jsonify("Something went wrong, please try again later"), 401
        

def get_user_profile():
    if request.method == "GET":
        
        try:
            #email = request.args.get("Email")
            email = session.get("email")

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
                sharedUserFunctionModel.update_password(userEmail, oldPassword, newPassword)
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Successful updating user password by"+userEmail, "update_password", "Successful password update")
            
            else:
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to update user password by"+userEmail, "update_password", "Error fields cannot be left blank and must be valid inputs")
        
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
            #email = request.form.get("Email")
            email = session.get("email")
            username = request.form.get("Username")
            contactNumber = request.form.get("ContactNumber")

            # checks if the input is null or empty and is valid
            if email is not None and isemail(email) and username is not None and contactNumber is not None:
                #return(jsonify(userModel.update_profile(email, username, contactNumber)), 200)
                userModel.update_profile(email, username, contactNumber)
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Successful Update profile", "update_profile", "Success")
            
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
            #offererEmail = request.form.get("Email")
            offererEmail = session.get("email")
            offer = request.form.get("Offer")

            # checks if the input is null or empty and is valid
            if bookID is not None and isint(bookID) and offererEmail is not None and isemail(offererEmail) and offer is not None and isfloat(offer):
                
                # verifies if the role is User, as only users can send_book_offer
                if sharedUserFunctionModel.get_role(offererEmail) == "User":
                    bookModel.send_book_offer(bookID, offer, offererEmail)
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Sending book offer", "send_book_offer", "Success Book Offer")

                else:
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to send book offer", "send_book_offer", "Error user not authroized")
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
            #ownerEmail = request.args.get("Email")
            ownerEmail = session.get("email")
            userTableName = userModel.get_tablename()

            # checks if the input is null or empty and is valid
            if bookID is not None and isint(bookID) and ownerEmail is not None and isemail(ownerEmail) and userTableName is not None:

                bookModel.get_book_offers(bookID, ownerEmail, userTableName)
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting book offers", "get_book_offers", "Success")



            
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
            #email = request.args.get("Email")
            email = session.get("email")
            userTableName = userModel.get_tablename()
            transactionsTableName = userModel.get_transactionsTableName()

            # checks if the input is null or empty and is valid
            if email is not None and isemail(email) and userTableName is not None and transactionsTableName is not None:
                bookModel.get_all_user_book_offers(email, userTableName, transactionsTableName)
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all book offers made by selected user email", "get_all_user_book_offers", "Success")
            
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
            #ownerEmail = request.args.get("Email")
            ownerEmail = session.get("email")

            # checks if the input is null or empty and is valid
            if bookOfferID is not None and isint(bookOfferID) and ownerEmail is not None and isemail(ownerEmail):

                # verifies if the role is User, as only users can accept_book_offer
                if sharedUserFunctionModel.get_role(ownerEmail) == "User":
                    result = bookModel.accept_book_offer(bookOfferID, ownerEmail)
                
                else:
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to accept book offer", "accept_book_offer", "Error user not authroized")

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
            #offererEmail = request.form.get("Email")
            offererEmail = session.get("email")
            newOffer = request.form.get("Offer")

            # checks if the input is null or empty and is valid
            if bookOfferID is not None and isint(bookOfferID) and offererEmail is not None and isemail(offererEmail) and newOffer is not None and isfloat(newOffer):

                bookModel.edit_book_offer(bookOfferID, offererEmail, newOffer)
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Editing book offer", "edit_book_offer", "Success")
            
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
            offererEmail = session.get("email")
            #offererEmail = request.form.get("Email")

            # checks if the input is null or empty and is valid
            if bookOfferID is not None and isint(bookOfferID) and offererEmail is not None and isemail(offererEmail):

                if sharedUserFunctionModel.get_role(offererEmail) == "User":
                    bookModel.delete_book_offer(bookOfferID, offererEmail)
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Deleting book offer", "delete_book_offer", "Success")
                
                else:
                    return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to delete book offer", "delete_book_offer", "Error user not authroized")
                    
            else:
                
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to delete book offer", "delete_book_offer", "Error fields cannot be left blank and must be valid inputs")
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception deleting book offer", "delete_book_offer", logMessage)
            return jsonify("Something went wrong, please try again later"), 401    

def get_transaction_details():
        if request.method == "GET": 

            try:
                transactionID = request.args.get("TransactionID")
                email = session.get("email")

                # checks if the input is null or empty and is valid and a session is active
                if transactionID is not None and isint(transactionID) and email is not None and isemail(email):
                    
                    if sharedUserFunctionModel.get_role(email) == "User":
                        userModel.get_transaction_details(transactionID)
                        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting transcation details of a specific transcation", "get_transaction_details", "Success")

                    else:
                        return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to get transcation details of a specific transcation", "get_transaction_details", "Error user not authroized")

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
            #email = request.args.get("Email")
            email = session.get("email")

            # checks if the input is null or empty and is valid
            if email is not None and isemail(email):
                userModel.get_all_user_transactions(email)
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Getting all user transcations made by selected user email", "get_all_user_transcations", "Success")
            
            else:

                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to get all user transcations made by selected user email", "get_all_user_transcations", "Error user not authroized")

        except Exception as ex:
                # logs the error log and returns a error message
                logMessage = "Exception Error " + str(ex)
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when getting all user transcations made by selected user email", "get_all_user_transcations", logMessage)
                return jsonify("Something went wrong, please try again later"), 401                    





def forget_password_reset():
    if request.method == "POST":
        try:
            email = request.form.get("Email")
            if (sharedUserFunctionModel.verifyEmailExists(email) == True):
                token = sharedUserFunctionModel.get_reset_token(email)

                send_email(email,token)
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Password reset was requested by"+email, "forget_password_reset", "Success")
                return (jsonify(message='OKK'), 201)
            else:
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Password reset was requested by"+email, "forget_password_reset", "Fail. Invalid Email")
                return (jsonify(message='An email will be sent to the email provided for password reset if it exists'), 201)
        
        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when sending email for password reset", "forget_password_reset", logMessage)
            return jsonify("Something went wrong, please try again later"), 401



def send_email(email,generatedtoken):

    from app import mail

    sender = current_app.config.get('MAIL_USERNAME')
    recipients = [email]
    msg = Message()
    msg.subject = "Password Recovery"
    msg.recipients = recipients
    msg.sender = sender
    msg.body = "You have requested for a password change, click on the link to reset your password now. "+"http://localhost:3000/ForgetResetPassword/"+generatedtoken

    mail.send(msg)

def verify_reset_password(token):

    try:
        args = request.view_args['token']
        username = sharedUserFunctionModel.verify_reset_token(args)
        if request.method == "GET":
            if username == "Invalid":
                return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                                     "Accesssing URL of password reset",
                                     "verify_reset_password",
                                     "Error! Invalid or expired token")
                return (jsonify(message='Token Expired'), 404)

            return (jsonify(message='OKK'), 201)

        if request.method == "POST":

            newpassword = request.form.get("Password")
            sharedUserFunctionModel.reset_password(username, newpassword)
            return return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Updating user password",
                                "verify_reset_password",
                                "Success")

    except Exception as ex:
        # logs the error log and returns a error message
        logMessage = "Exception Error " + str(ex)
        return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when validating email for password reset", "verify_reset_password", logMessage)
        return jsonify("Something went wrong, please try again later"), 401


def verify_captcha():
    if request.method == "POST":

        try:
            captchattoken = request.form.get("Token")  # retrieve token from ForgetPassword.js
            secretkey = current_app.config.get('RECAPTCHA_SECRET_KEY')  # captcha secret key to validate
            captchapayload = {'response': captchattoken,
                              'secret': secretkey}  # create the payload to sent request for captcha validation

            response = requests.post("https://www.google.com/recaptcha/api/siteverify",
                                     captchapayload)  # captcha validation
            captcharesponse_text = json.loads(response.text)

            if (captcharesponse_text['success'] == True):
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                              "Verifying Captcha", "verify_reset_password", "Success")

                return {'message': ['true']}

            else:
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                              "Verifying Captcha", "verify_reset_password", "Fail! Invalid key")
                return {jsonify({'message': ['false']})}

        except Exception as ex:
            # logs the error log and returns a error message
            logMessage = "Exception Error " + str(ex)
            return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                          "Exception when validating capcha", "verify_captcha", logMessage)
            return jsonify("Something went wrong, please try again later"), 401