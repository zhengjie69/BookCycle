from flask import request, session
from ..models.data_cleaning import *
from ..models.super_admin_model import SuperAdmin
from .api_logger import *

superadminModel = SuperAdmin()

def create_admin_account():
    if request.method == "POST":

        try:
            #superAdminEmail = request.form.get("superAdminEmail")
            superAdminEmail = session.get("email")
            username = request.form.get("Username")
            adminEmail = request.form.get("AdminEmail")
            password = request.form.get("Password")
            contactNumber = request.form.get("ContactNumber")
            
            # checks if the values are not none
            if superAdminEmail is not None and username is not None and adminEmail is not None and password is not None and contactNumber is not None:

                # checks if values are valid, if it is, proceed to create admin
                if isemail(superAdminEmail) and isemail(superAdminEmail) and isstring(username) and isvalidpassword(password) and isvalidcontactnumber(contactNumber):
            
                    # if logged in user is a superadmin, create admin
                    if superadminModel.validate_super_admin(superAdminEmail):
                        return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Creating admin account", "create_admin_account", superadminModel.create_admin_account(username, adminEmail, password, contactNumber)))
                    
                    else:
                        return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to Create admin account with superadmin", "create_admin_account", "Error User does not have permission"))
                
                else:
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to Create admin account with superadmin", "create_admin_account", "Error invalid input found"))               

            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to Create admin account with superadmin", "create_admin_account", "Error required values are empty"))
                
        except Exception as ex:
            # logs the error log and returns a error message
                logMessage = "Exception Error " + str(ex)
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when superadmin is creating admin account", "create_admin_account", logMessage)
                return jsonify("Something went wrong, please try again later"), 401            

def search_admin():
    if request.method == "POST":

        try:
            adminEmail = request.form.get("AdminEmail")
            #superAdminEmail = request.form.get("SuperAdminEmail")
            superAdminEmail = session.get("email")

            # checks if the values are valid and not none, if valid and not none check if the user has right role
            if adminEmail is not None and isemail(adminEmail) and superAdminEmail is not None and isemail(superAdminEmail):
                # checks if the email calling the api is a Admin email, if it is, call the required functions
                if superadminModel.validate_super_admin(superAdminEmail):
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "SuperAdmin searching admin", "search_admin", superadminModel.search_admin(adminEmail)))
                else:
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to search admin with superAdmin", "search_admin", "Error User does not have permission"))
            
            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to search admin with superAdmin", "search_admin", "Error invalid input found"))

        except Exception as ex:
            # logs the error log and returns a error message
                logMessage = "Exception Error " + str(ex)
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when superadmin is searching admin account", "search_admin", logMessage)
                return jsonify("Something went wrong, please try again later"), 401

def delete_admin_account():
        if request.method == "POST":

            try:
        
                #superAdminEmail = request.form.get("superAdminEmail")
                superAdminEmail = session.get("email")
                adminEmail = request.form.get("AdminEmail")

                # checks if the values are valid and not none, if valid and not none check if the user has right role
                if adminEmail is not None and isemail(adminEmail) and superAdminEmail is not None and isemail(superAdminEmail):
                    # if logged in user is a superadmin, create admin
                    if superadminModel.validate_super_admin(superAdminEmail):
                        return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Deleting admin account", "delete_admin_account", superadminModel.delete_admin_account(adminEmail)))
                
                    else:
                        return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to delete admin account", "delete_admin_account", "Error User does not have permission"))
                else:
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to delete admin account", "delete_admin_account", "Error invalid input found"))
            
            except Exception as ex:
            # logs the error log and returns a error message
                logMessage = "Exception Error " + str(ex)
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when superadmin is deleting admin account", "delete_admin_account", logMessage)
                return jsonify("Something went wrong, please try again later"), 401
                    

def disable_admin_account():
    if request.method == "POST":

        try:
            #superAdminEmail = request.form.get("superAdminEmail")
            superAdminEmail = session.get("email")
            adminEmail = request.form.get("AdminEmail")


            # checks if the values are valid and not none, if valid and not none check if the user has right role
            if adminEmail is not None and isemail(adminEmail) and superAdminEmail is not None and isemail(superAdminEmail):
                # if logged in user is a superadmin, disable admin account
                if superadminModel.validate_super_admin(superAdminEmail):
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Disabling admin account", "disable_admin_account", superadminModel.disable_admin_account(adminEmail)))
                else:
                    return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to disable admin account", "disable_admin_account", "Error User does not have permission"))

            else:
                return(return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Failed to disable admin account", "disable_admin_account", "Error invalid input found"))

        except Exception as ex:
            # logs the error log and returns a error message
                logMessage = "Exception Error " + str(ex)
                return_result(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), "Exception when superadmin is deleting admin account", "disable_admin_account", logMessage)
                return jsonify("Something went wrong, please try again later"), 401        