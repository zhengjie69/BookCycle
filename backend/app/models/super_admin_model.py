import sqlite3
import bcrypt

class SuperAdmin:

    def __init__(self):
        self.dbname  = "database"
        self.userTablename = "User"
        self.transactionsTableName = "Transactions"
        self.roleTableName = "Role"
        self.accountStatusTableName = "AccountStatus"
        self.bookTableName = "Book"

    def validate_super_admin(self, loginEmail):
       try:
        
           with sqlite3.connect(self.dbname + ".db") as con:
               print ("Opened database successfully")
                
               cur = con.cursor()
               cur.execute("SELECT COUNT(*) FROM {} AS a INNER JOIN {} AS b ON a.RoleID = b.RoleID WHERE a.Email = ? AND b.RoleName = ?".format(self.userTablename, self.roleTableName), (loginEmail,"SuperAdmin"))
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


    def create_admin_account(self, username, email, password, contactNumber):
        try:
            
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                # fetches the admin role ID
                cur = con.cursor()
                cur.execute("SELECT RoleID FROM {} WHERE RoleName = ?".format(self.roleTableName), ("Admin",))
                result = cur.fetchall()

                roleID = result[0][0]

                # fetches the active account status ID
                cur.execute("SELECT AccountStatusID FROM {} WHERE AccountStatusName = ?".format(self.accountStatusTableName), ("Active",))
                result2 = cur.fetchall()

                accountStatusID = result2[0][0]
                if roleID is not None and roleID > 0 and accountStatusID is not None and accountStatusID > 0:

                    if password != "" and password is not None:
                        hashpassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                        

                        con.execute("INSERT INTO {} (Username, Email, Password, ContactNumber, RoleID, AccountStatusID) VALUES (?,?,?,?,?,?)".format(self.userTablename),(username,email, hashpassword, contactNumber, roleID, accountStatusID))
                con.commit()
                return("Successfully created user")

        except sqlite3.Error as er:
            print(er)
            con.rollback()
            return("Error in Creating Admin")
      
        finally:
            con.close()
            print("Successfully closed connection")

    def search_admin(self, adminEmail):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()

                # fetches the matching admin role account from User table, query is exact, not LIKE
                cur.execute("SELECT a.Username, a.Email, a.ContactNumber, C.AccountStatusName FROM {} AS a INNER JOIN {} AS b ON a.RoleID = b.RoleID INNER JOIN {} AS c ON a.AccountStatusID = c.AccountStatusID WHERE b.RoleName = ? AND a.Email = ?".format(self.userTablename, self.roleTableName, self.accountStatusTableName),("Admin", adminEmail))
                rows = cur.fetchall()
                   
                # if the user is found:
                if len(rows) == 1:
                    
                    dataList = []
                    tempdict = {'Username': rows[0][0], 'Email': rows[0][1], 'ContactNumber': rows[0][2], 'AccountStatus': rows[0][3]}
                    dataList.append(tempdict)
                    return(dataList)
                else:
                    return("Error no matching account found") 

        except:
            con.rollback()
            return("Error in searching account")
      
        finally:
            con.close()
            print("Successfully closed connection")

    def delete_admin_account(self, adminEmail):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")
                
                # fetches the admin role ID
                cur = con.cursor()
                cur.execute("SELECT RoleID FROM {} WHERE RoleName = ?".format(self.roleTableName), ("Admin",))
                result = cur.fetchall()

                roleID = result[0][0]
                
                cur.execute("DELETE FROM {} WHERE Email = ? AND RoleID = ?".format(self.userTablename), (adminEmail, roleID))
                con.commit()
                
                return("Successfully deleted")

        except sqlite3.Error as er:
            con.rollback()
            print(er)
            return("Error in deleting book")

        finally:
            con.close()
            print("Successfully closed connection")

    def disable_admin_account(self, adminEmail):
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

                    cur.execute("UPDATE {} SET AccountStatusID = ? WHERE Email = ? ".format(self.userTablename),(accountStatusID, adminEmail))
                    con.commit()
                    return("Successfully disabled admin account")

                else:
                    return("Error in getting Account")
                
        except sqlite3.Error as er:
            con.rollback()
            return("Error in disabling account")

        finally:
            con.close()
            print("Successfully closed connection")