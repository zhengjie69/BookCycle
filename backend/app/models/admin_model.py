import sqlite3


class Admin:

    def __init__(self):
        self.dbname = "database"
        self.userTablename = "User"
        self.transactionsTableName = "Transactions"
        self.roleTableName = "Role"
        self.accountStatusTableName = "AccountStatus"
        self.bookTableName = "Book"


    # fetches all users with the role "User"
    # def get_all_users(self):
    #     try:
        
    #         with sqlite3.connect(self.dbName + ".db") as con:
    #             print ("Opened database successfully")

    #             # this command forces sqlite to enforce the foreign key rules set  for the tables
    #             con.execute("PRAGMA foreign_keys = 1")

    #             cur = con.cursor()

    #             # fetches all users role account from User table
    #             cur.execute("SELECT a.Email FROM {} AS a INNER JOIN {} AS b ON a.AccountStatusID = b.AccountStatusID AND b.AccountStatusName = \"User\"".format(self.userTablename, self.accountStatusTableName))
    #             rows = cur.fetchall()
                   
    #             # test print db records
    #             if len(rows) > 0:
    #                 print("rows of records:")
    #                 for records in rows:
    #                     print(records)
    #                 return(rows)
    #             else:
    #                 return("No records in database") 

    #     except:
    #         con.rollback()
    #         return("Error in fetching users")
      
    #     finally:
    #         con.close()
    #         print("Successfully closed connection")

    # checks if the account logged in is aa Admin
    def validate_admin(self, loginEmail):
       try:
        
           with sqlite3.connect(self.dbname + ".db") as con:
               print ("Opened database successfully")
                
               cur = con.cursor()
               cur.execute("SELECT COUNT(*) FROM {} AS a INNER JOIN {} AS b ON a.RoleID = b.RoleID WHERE a.Email = ? AND b.RoleName = ?".format(self.userTablename, self.roleTableName), (loginEmail,"Admin"))
               rows = cur.fetchall()
               # if only 1 record is found which verifies that the account is a Admin
               if rows[0][0] == 1:
                   return(True)
               else:
                   return(False) 

       except:
           con.rollback()
           print("Error unable to validate user")
           return(False) 
      
       finally:
           con.close()
           print("Successfully closed connection")

    def search_user(self, userEmail):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()

                # fetches all users role account from User table, query is exact, not LIKE
                cur.execute("SELECT a.Username, a.Email, a.ContactNumber, b.AccountStatusName FROM {} AS a INNER JOIN {} AS b ON a.AccountStatusID = b.AccountStatusID WHERE b.AccountStatusName = ? AND a.Email = ?".format(self.userTablename, self.accountStatusTableName),("User", userEmail))
                rows = cur.fetchall()
                   
                # if the user is found:
                if len(rows) == 1:
                    
                    dataList = []
                    tempdict = {'Username': rows[0][0], 'Email': rows[0][1], 'ContactNumber': rows[0][2], 'AccountStatus': rows[0][3]}
                    dataList.append(tempdict)
                    return(dataList)
                else:
                    return("Error no matching user found") 

        except:
            con.rollback()
            return("Error in searching user")
      
        finally:
            con.close()
            print("Successfully closed connection")

    
    def delete_user_book(self, bookID, ownerEmail):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")
                
                cur = con.cursor()
                cur.execute("DELETE FROM {} WHERE BookID = ? AND Email = ?".format(self.bookTableName), (bookID,ownerEmail))
                con.commit()
                return("successfully deleted")

        except sqlite3.Error as er:
            con.rollback()
            print(er)
            return("Error in deleting book")

        finally:
            con.close()
            print("Successfully closed connection")


    def enable_user_account(self, userEmail):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()


                # gets the account status id of "Activate" from the db for update
                cur.execute("SELECT AccountStatusID FROM {} WHERE AccountStatusName = ?".format(self.accountStatusTableName), ("Active",))
                result = cur.fetchall()
                
                # when exactly 1 of the account status ID for "Activate" is found
                # updates the account status id to "Activate"'s id
                if len(result) == 1:
                    accountStatusID = result[0][0]

                    cur.execute("UPDATE {} SET AccountStatusID = ? WHERE Email = ? ".format(self.userTablename),(accountStatusID, userEmail))
                    con.commit()
                    return("successfully enabled account")

                else:
                    return("Error in getting Account Status ID")
                
        except sqlite3.Error as er:
            con.rollback()
            print(er)
            return("Error in enabling account")

        finally:
            con.close()
            print("Successfully closed connection")

    def disable_user_account(self, userEmail):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()


                # gets the account status id of "Disabled" from the db for update
                cur.execute("SELECT AccountStatusID FROM {} WHERE AccountStatusName = ?".format(self.accountStatusTableName), ("Disabled",))
                result = cur.fetchall()
                
                # when exactly 1 of the account status ID for "Disabled" is found
                # updates the account status id to "Disabled"'s id
                if len(result) == 1:
                    accountStatusID = result[0][0]

                    cur.execute("UPDATE {} SET AccountStatusID = ? WHERE Email = ? ".format(self.userTablename),(accountStatusID, userEmail))
                    con.commit()
                    return("successfully disabled account")

                else:
                    return("Error in getting Account Status ID")
                
        except sqlite3.Error as er:
            con.rollback()
            print(er)
            return("Error in disabling account")

        finally:
            con.close()
            print("Successfully closed connection")

        
        
        