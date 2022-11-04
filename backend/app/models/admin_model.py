import sqlite3


class Admin:

    def __init__(self):
        self.dbname = "database"
        self.userTablename = "User"
        self.transactionsTableName = "Transactions"
        self.roleTableName = "Role"
        self.accountStatusTableName = "AccountStatus"
        self.bookTableName = "Book"

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

       except Exception as ex:
           con.rollback()
           raise ex
      
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

                # fetches the matching user role account from User table, query is exact, not LIKE
                cur.execute("SELECT a.Username, a.Email, a.ContactNumber, C.AccountStatusName FROM {} AS a INNER JOIN {} AS b ON a.RoleID = b.RoleID INNER JOIN {} AS c ON a.AccountStatusID = c.AccountStatusID WHERE b.RoleName = ? AND a.Email = ?".format(self.userTablename, self.roleTableName, self.accountStatusTableName),("User", userEmail))
                rows = cur.fetchall()
                   
                # if the user is found:
                if len(rows) == 1:
                    
                    dataList = []
                    tempdict = {'Username': rows[0][0], 'Email': rows[0][1], 'ContactNumber': rows[0][2], 'AccountStatus': rows[0][3]}
                    dataList.append(tempdict)
                    return(dataList)
                else:
                    return("Error no matching user found") 

        except Exception as ex:
            con.rollback()
            raise ex
      
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

        except Exception as ex:
            con.rollback()
            raise ex

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

                    cur.execute("UPDATE {} SET AccountStatusID = ?, LoginAttemptCount = ? WHERE Email = ? ".format(self.userTablename),(accountStatusID, 0, userEmail))
                    con.commit()
                    return("successfully enabled account")

                else:
                    return("Error in getting Account Status ID")
                
        except Exception as ex:
            con.rollback()
            raise ex

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
                
        except Exception as ex:
            con.rollback()
            raise ex

        finally:
            con.close()
            print("Successfully closed connection")

        
        
        