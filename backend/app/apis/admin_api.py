from ..models.data_cleaning import *
from ..models.admin_model import Admin
from flask import request
from .api_logger import *

adminModel = Admin()

def search_user():
    if request.method == "POST":
        adminEmail = request.form.get("AdminEmail")
        userEmail = request.form.get("UserEmail")

        # checks if the values are valid and not none, if valid and not none check if the user has right role
        if adminEmail is not None and userEmail is not None and isemail(adminEmail) and isemail(userEmail):

            # checks if the email calling the api is a Admin email, if it is, call the required functions
            if adminModel.validate_admin(adminEmail):
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin searching user", "search_user", adminModel.search_user(userEmail)))
            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin searching user", "search_user", "Error User does not have permission"))
        else:
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin searching user", "search_user", "Error invalid input found"))

def delete_user_book():
    if request.method == "POST":
        ownerEmail = request.form.get("OwnerEmail")
        email = request.form.get("Email")
        bookID = request.form.get("BookID")

        # checks if the values are valid and not none, if valid and not none check if the user has right role
        if ownerEmail is not None and email is not None and bookID is not None and isemail(ownerEmail) and isemail(email) and isint(bookID):
            
            # checks if the email calling the api is a Admin email, if it is, call the required functions
            if adminModel.validate_admin(email):
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin searching user", "search_user", adminModel.delete_user_book(bookID, ownerEmail)))
            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin deleting user book", "delete_user_book", "Error User does not have permission"))
       
        else:
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin deleting user book", "delete_user_book", "Error invalid input found"))

def enable_user_account():
    if request.method == "POST":
        userEmail = request.form.get("UserEmail")
        email = request.form.get("Email")
        
        # checks if the values are valid and not none, if valid and not none check if the user has right role
        if userEmail is not None and email is not None and isemail(userEmail) and isemail(email):

            # checks if the email calling the api is a Admin email, if it is, call the required functions
            if adminModel.validate_admin(email):
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin enable user account", "enable_user_account", adminModel.enable_user_account(userEmail)))
            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin enable user account", "enable_user_account", "Error User does not have permission"))
        
        else:
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin enable user account", "enable_user_account", "Error invalid input found"))

def disable_user_account():
    if request.method == "POST":
        userEmail = request.form.get("UserEmail")
        email = request.form.get("Email")

        # checks if the values are valid and not none, if valid and not none check if the user has right role
        if userEmail is not None and email is not None and isemail(userEmail) and isemail(email):

            # checks if the email calling the api is a Admin email, if it is, call the required functions
            if adminModel.validate_admin(email):
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin disable user account", "disable", adminModel.disable_user_account(userEmail)))
            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin enable user account", "enable_user_account", "Error User does not have permission"))
            
        else:
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin enable user account", "enable_user_account", "Error invalid input found"))


