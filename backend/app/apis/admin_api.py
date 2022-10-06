from ..models.admin_model import Admin
from flask import jsonify, request
from datetime import datetime

adminModel = Admin()

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

def search_user():
    if request.method == "POST":
        adminEmail = request.form.get("AdminEmail")
        userEmail = request.form.get("UserEmail")

        # checks if the email calling the api is a Admin email, if it is, call the required functions
        if adminModel.validate_admin(adminEmail):
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin searching user", "search_user", adminModel.search_user(userEmail)))
        else:
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin searching user", "search_user", "Error User does not have permission"))

def delete_user_book():
    if request.method == "POST":
        ownerEmail = request.form.get("OwnerEmail")
        email = request.form.get("Email")
        bookID = request.form.get("BookID")

        # checks if the email calling the api is a Admin email, if it is, call the required functions
        if adminModel.validate_admin(email):
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin searching user", "search_user", adminModel.delete_user_book(bookID, ownerEmail)))
        else:
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin deleting user book", "delete_user_book", "Error User does not have permission"))


def enable_user_account():
    if request.method == "POST":
        userEmail = request.form.get("UserEmail")
        email = request.form.get("Email")

        # checks if the email calling the api is a Admin email, if it is, call the required functions
        if adminModel.validate_admin(email):
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin enable user account", "enable_user_account", adminModel.enable_user_account(userEmail)))
        else:
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin enable user account", "enable_user_account", "Error User does not have permission"))

def disable_user_account():
    if request.method == "POST":
        userEmail = request.form.get("UserEmail")
        email = request.form.get("Email")

        # checks if the email calling the api is a Admin email, if it is, call the required functions
        if adminModel.validate_admin(email):
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin disable user account", "disable", adminModel.disable_user_account(userEmail)))
        else:
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Admin enable user account", "enable_user_account", "Error User does not have permission"))


