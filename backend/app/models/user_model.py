import sqlite3
import bcrypt


class User:

    def __init__(self):
        self.dbname = "database"
        self.tablename = "User"
        self.transactionsTableName = "Transactions"
        self.roleTableName = "Role"
        self.accountStatusTableName = "AccountStatus"

    def get_tablename(self):
        return self._tablename

    def create_user(self, username, email, password, contactNumber):
        try:
            
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()
                cur.execute("SELECT RoleID FROM {} WHERE RoleName = ?".format(self.roleTableName), ("User",))
                result = cur.fetchall()

                roleID = result[0][0]

                cur.execute("SELECT AccountStatusID FROM {} WHERE AccountStatusName = ?".format(self.accountStatusTableName), ("Active",))
                result2 = cur.fetchall()

                accountStatusID = result2[0][0]

                # if the role id and account status id is retrieved successfully
                if roleID is not None and roleID > 0 and accountStatusID is not None and accountStatusID > 0:

                    if password != "" and password is not None:
                        
                        hashpassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                        con.execute("INSERT INTO {} (Username, Email, Password, ContactNumber, RoleID, AccountStatusID) VALUES (?,?,?,?,?,?)".format(self.tablename),(username,email, hashpassword, contactNumber, roleID, accountStatusID))
                con.commit()
                return("Successfully created user account")

        except sqlite3.Error as er:
            print(er)
            con.rollback()
            return("Error in Inserting User")
      
        finally:
            con.close()
            print("Successfully closed connection")

    # def get_user_profile(self, email):
    #     try:
        
    #         with sqlite3.connect(self.dbname + ".db") as con:
    #             print ("Opened database successfully")

    #             # this command forces sqlite to enforce the foreign key rules set  for the tables
    #             con.execute("PRAGMA foreign_keys = 1")

    #             cur = con.cursor()

    #             # fetches all users from User table
    #             cur.execute("SELECT Email, ContactNumber FROM {} WHERE Email = \"{}\"".format(self.tablename, email))
    #             rows = cur.fetchall()
                   
    #             # test print db records
    #             if len(rows) > 0:
    #                 print("rows of records:")
    #                 for records in rows:
    #                     print(records)
    #                 return(rows)
    #             else:
    #                 return("No matching user in database") 

    #     except:
    #         con.rollback()
    #         return("Error in fetching selected user")
      
    #     finally:
    #         con.close()
    #         print("Successfully closed connection")

    # def update_password(self, email, oldPassword, newPassword):
    #     try:
            
    #         with sqlite3.connect(self.dbname + ".db") as con:
    #             print ("Opened database successfully")

    #             cur = con.cursor()
    #             cur.execute("SELECT Password FROM {} WHERE Email = \"{}\"".format(self.dbname, email))
    #             result = cur.fetchall()

    #             fetchedPassword = result[0][0]


    #             if oldPassword != "" and oldPassword is not None and newPassword != "" and newPassword is not None:
                    

                    
    #                 # checks if the old password matches the stored password
    #                 # if matches proceed to replace password with the new one
    #                 if bcrypt.checkpw(oldPassword.encode(), fetchedPassword):
                        
    #                     newHashPassword = bcrypt.hashpw(newPassword.encode(), bcrypt.gensalt())
    #                     con.execute("UPDATE {} SET Password = \"{}\" ON Email = \"{}\"",(self.dbname, newHashPassword, email))
    #                     returnMessage = "Password Successfully Changed"

    #                 else:
    #                     returnMessage = "Invalid old password"
                
    #             else:
    #                 returnMessage =    "Invalid Input"

    #             con.commit()
    #             return returnMessage
    #     except sqlite3.Error as er:
    #         print(er)
    #         con.rollback()
    #         return("Error in Inserting User")
      
    #     finally:
    #         con.close()
    #         print("Successfully closed connection")


    # def reset_password():
    #     pass


    def update_profile(self, email, username, contactnumber):
        try:
            
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                con.execute("UPDATE {} SET Username = ?, ContactNumber = ? WHERE Email = ?".format(self.tablename), ( username, contactnumber, email) )
                con.commit()
                return("Successfully Updated User Profile")


        except sqlite3.Error as er:
            print(er)
            con.rollback()
            return("Error in Updating User Profile")
      
        finally:
            con.close()
            print("Successfully closed connection")

    


    def create_Transaction(self, bookDetails, PurchaserEmail):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                bookTitle = bookDetails[0][0]
                bookPrice = bookDetails[0][1]
                ownerEmail = bookDetails[0][2]

                cur = con.cursor()
                cur.execute("INSERT INTO {} (BookTitle, Price, Email, PurchaserEmail) VALUES(?,?,?,?)".format(self.transactionsTableName), (bookTitle, bookPrice, ownerEmail, PurchaserEmail))
                con.commit()

        except:
            con.rollback()
            return("Error in Logging in, Please try again")
      
        finally:
            con.close()
            print("Successfully closed connection")

    # def validate_user(self, email):
    #     try:
        
    #         with sqlite3.connect(self.dbname + ".db") as con:
    #             print ("Opened database successfully")
                
    #             cur = con.cursor()
    #             cur.execute("SELECT Email FROM {} WHERE Email = \"{}\"".format(self.tablename, email))
    #             rows = cur.fetchall()
    #             # if only 1 record is found (as each email should only have 1 account) 
    #             if len(rows) == 1:
    #                 return(True)
    #             else:
    #                 return(False) 

    #     except:
    #         con.rollback()
    #         print("User not found")
    #         return(False) 
      
    #     finally:
    #         con.close()
    #         print("Successfully closed connection")




        
        
        