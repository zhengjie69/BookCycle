from flask import jsonify, request, current_app
from ..models.super_admin_model import SuperAdmin
from datetime import datetime

superadminModel = SuperAdmin()

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


def create_admin_account():
    if request.method == "POST":
        superAdminEmail = request.form.get("superAdminEmail")
        username = request.form.get("Username")
        adminEmail = request.form.get("AdminEmail")
        password = request.form.get("Password")
        contactNumber = request.form.get("ContactNumber")
        
        # if logged in user is a superadmin, create admin
        if superadminModel.validate_super_admin(superAdminEmail):
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Creating admin account", "create_admin_account", superadminModel.create_admin_account(username, adminEmail, password, contactNumber)))
        
        else:
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Creating admin account", "create_admin_account", "Error User does not have permission"))

def delete_admin_account():
        if request.method == "POST":
        
            superAdminEmail = request.form.get("superAdminEmail")
            adminEmail = request.form.get("AdminEmail")

            # if logged in user is a superadmin, create admin
            if superadminModel.validate_super_admin(superAdminEmail):
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Deleting admin account", "delete_admin_account", superadminModel.delete_admin_account(adminEmail)))
        
            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Deleting admin account", "delete_admin_account", "Error User does not have permission"))

def disable_admin_account():
    if request.method == "POST":
        superAdminEmail = request.form.get("superAdminEmail")
        admninEmail = request.form.get("AdminEmail")

        # if logged in user is a superadmin, disable admin account
        if superadminModel.validate_super_admin(superAdminEmail):
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Disabling admin account", "disable_admin_account", superadminModel.disable_admin_account(admninEmail)))
        else:
            return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Disabling admin account", "disable_admin_account", "Error User does not have permission"))