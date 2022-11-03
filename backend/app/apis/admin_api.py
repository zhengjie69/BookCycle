from ..models.data_cleaning import *
from ..models.admin_model import Admin
from flask import request, session
from .api_logger import *

adminModel = Admin()

def search_user():
    if request.method == "POST":

        try:
            #adminEmail = request.form.get("AdminEmail")
            adminEmail = session.get("email")
            userEmail = request.form.get("UserEmail")

            # checks if the values are valid and not none, if valid and not none check if the user has right role
            if adminEmail is not None and userEmail is not None and isemail(adminEmail) and isemail(userEmail):

                # checks if the email calling the api is a Admin email, if it is, call the required functions
                if adminModel.validate_admin(adminEmail):
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin searching user", "search_user", adminModel.search_user(userEmail)))
                else:
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to search user by admin", "search_user", "Error User does not have permission"))
            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to search user by admin", "search_user", "Error invalid input found"))

        except Exception as ex:
            # logs the error log and returns a error message
                logMessage = "Exception Error " + str(ex)
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when admin is searching for user", "search_user", logMessage)
                return jsonify("Something went wrong, please try again later"), 401        

def delete_user_book():
    if request.method == "POST":

        try:
            ownerEmail = request.form.get("OwnerEmail")
            #email = request.form.get("Email")
            email = session.get("email")
            bookID = request.form.get("BookID")

            # checks if the values are valid and not none, if valid and not none check if the user has right role
            if ownerEmail is not None and email is not None and bookID is not None and isemail(ownerEmail) and isemail(email) and isint(bookID):
                
                # checks if the email calling the api is a Admin email, if it is, call the required functions
                if adminModel.validate_admin(email):
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin deleting user book", "delete_user_book", adminModel.delete_user_book(bookID, ownerEmail)))
                else:
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to delete user book by admin", "delete_user_book", "Error User does not have permission"))
        
            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to delete user book by admin", "delete_user_book", "Error invalid input found"))
        
        except Exception as ex:
            # logs the error log and returns a error message
                logMessage = "Exception Error " + str(ex)
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when admin is deleting user book", "delete_user_book", logMessage)
                return jsonify("Something went wrong, please try again later"), 401

def enable_user_account():
    if request.method == "POST":

        try:
            userEmail = request.form.get("UserEmail")
            #email = request.form.get("Email")
            email = session.get("email")
            
            # checks if the values are valid and not none, if valid and not none check if the user has right role
            if userEmail is not None and email is not None and isemail(userEmail) and isemail(email):

                # checks if the email calling the api is a Admin email, if it is, call the required functions
                if adminModel.validate_admin(email):
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin enable user account", "enable_user_account", adminModel.enable_user_account(userEmail)))
                else:
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to enable user account by admin", "enable_user_account", "Error User does not have permission"))
            
            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to enable user account by admin", "enable_user_account", "Error invalid input found"))

        except Exception as ex:
            # logs the error log and returns a error message
                logMessage = "Exception Error " + str(ex)
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when admin is enabling user account", "enable_user_account", logMessage)
                return jsonify("Something went wrong, please try again later"), 401

def disable_user_account():
    if request.method == "POST":

        try:
            userEmail = request.form.get("UserEmail")
            #email = request.form.get("Email")
            email = session.get("email")

            # checks if the values are valid and not none, if valid and not none check if the user has right role
            if userEmail is not None and email is not None and isemail(userEmail) and isemail(email):

                # checks if the email calling the api is a Admin email, if it is, call the required functions
                if adminModel.validate_admin(email):
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin disable user account", "disable_user_account", adminModel.disable_user_account(userEmail)))
                else:
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to disable user account by admin", "disable_user_account", "Error User does not have permission"))
                
            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to disable user account by admin", "disable_user_account", "Error invalid input found"))
        
        except Exception as ex:
            # logs the error log and returns a error message
                logMessage = "Exception Error " + str(ex)
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when admin diables user account", "disable_user_account", logMessage)
                return jsonify("Something went wrong, please try again later"), 401

