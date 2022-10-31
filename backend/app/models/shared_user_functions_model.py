import sqlite3
from flask import current_app, url_for
import bcrypt
import jwt
import time

class Shared_User_Functions:

    def __init__(self):
            self.dbname = "database"
            self.tablename = "User"
            self.roleTableName = "Role"
            self.accountStatusTableName = "AccountStatus"

    def login(self, email, password):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()
                cur.execute("SELECT * FROM {} WHERE Email = \"{}\"".format(self.tablename, email))
                rows = cur.fetchall()
                print(rows)
                # if only 1 record is found (as each email should only have 1 account) 
                if len(rows) == 1:
                    hashedPassword = rows[0][2]
                    if bcrypt.checkpw(password.encode(), hashedPassword):
                        print("Password matched")
                        return True
                    else:
                        print("Password wrong")
                        return False
                else:
                    print("Password wrong")
                    return False

        except:
            con.rollback()
            return("Error in Logging in, Please try again")
      
        finally:
            con.close()
            print("Successfully closed connection")
    

    def update_password(self, email, oldPassword, newPassword):
        try:
            
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                # checks if the old password and new password is null or none, if not, check the old password to stored password
                if oldPassword != "" and oldPassword is not None and newPassword != "" and newPassword is not None:
                    
                    cur = con.cursor()
                    cur.execute("SELECT Password FROM {} WHERE Email = ?".format(self.tablename), (email,))
                    result = cur.fetchall()

                    fetchedPassword = result[0][0]
                    
                    # checks if the old password matches the stored password
                    # if matches proceed to replace password with the new one
                    if bcrypt.checkpw(oldPassword.encode(), fetchedPassword):
                        
                        newHashPassword = bcrypt.hashpw(newPassword.encode(), bcrypt.gensalt())
                        con.execute("UPDATE {} SET Password = ? WHERE Email = ?".format(self.tablename),(newHashPassword, email))
                        con.commit()
                        returnMessage = "Password Successfully Changed"

                    else:
                        returnMessage = "Invalid old password"
                
                else:
                    returnMessage =    "Invalid Input"

                
                return returnMessage
        except sqlite3.Error as er:
            print(er)
            con.rollback()
            return("Error in Updating Password")
      
        finally:
            con.close()
            print("Successfully closed connection")


    def reset_password(self,email,password):
        try:

            with sqlite3.connect(self.dbname + ".db") as con:
                print("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")



                cur = con.cursor()

                newHashPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                con.execute("UPDATE {} SET Password = ? WHERE Email = ?".format(self.tablename),
                                    (newHashPassword, email))
                con.commit()
                returnMessage = "Password Successfully Changed"




                return returnMessage
        except sqlite3.Error as er:
            print(er)
            con.rollback()
            return ("Error in Updating Password")

        finally:
            con.close()
            print("Successfully closed connection")

    def get_role(self,email):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()

                # fetches all users from User table
                cur.execute("SELECT b.RoleName FROM {} AS a INNER JOIN {} AS b ON a.RoleID = b.RoleID WHERE a.Email = ?".format(self.tablename, self.roleTableName), (email,))
                rows = cur.fetchall()
                   
                # gets the role if a role is found
                if len(rows) == 1:
                    return(rows[0][0])
                else:
                    return(None) 

        except:
            con.rollback()
            return(None)
      
        finally:
            con.close()
            print(None)

    def get_user_profile(self, email):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()

                # fetches all users from User table
                cur.execute("SELECT Username, Email, ContactNumber FROM {} WHERE Email = ?".format(self.tablename), (email,))
                rows = cur.fetchall()
                   
                # goes through the list to create a list with dict inside
                if len(rows) > 0:
                    print("rows of records:")
                    returnData = []
                    for records in rows:

                        returnData.append({'Username': records[0], 'Email': records[1], 'ContactNumber': records[2]})

                        print(records)
                    return(returnData)
                else:
                    return("No matching user in database") 

        except:
            con.rollback()
            return("Error in fetching selected user")
      
        finally:
            con.close()
            print("Successfully closed connection")

    def verifyEmailExists(self, email):
        try:

            with sqlite3.connect(self.dbname + ".db") as con:
                print("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()

                # fetches all users from User table
                cur.execute("SELECT Email FROM {} WHERE Email = ?".format(self.tablename),
                            (email,))
                rows = cur.fetchall()
                # goes through the list to create a list with dict inside
                if len(rows) > 0:
                    print("Email Valid")
                    return True
                else:
                    return ("No matching email in database")

        except:
            con.rollback()
            return ("Error in fetching selected email")

        finally:
            con.close()
            print("Successfully closed connection")

    def get_reset_token(self,email, expires=30):
        times = time.time()
        return jwt.encode({'reset_password': email, 'exp': times + expires}, key=("TESTINGKEY"))

    def verify_reset_token(self,token):
        try:
            username = jwt.decode(token, key=("TESTINGKEY"),algorithms=['HS256']),['reset_password']
        except Exception as e:
            print(e)
            return "Invalid"



        return username[0]['reset_password']