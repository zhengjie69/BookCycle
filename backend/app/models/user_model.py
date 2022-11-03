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
        return self.tablename

    def get_transactionsTableName(self):
        return self.transactionsTableName

    def get_role(self, email):
        try:
            if email is not None:
                with sqlite3.connect(self.dbname + ".db") as con:
                    print ("Opened database successfully")
                    
                    # this command forces sqlite to enforce the foreign key rules set  for the tables
                    con.execute("PRAGMA foreign_keys = 1")

                    
                    cur = con.cursor()

                    # checks if the username is already used in the db
                    cur.execute("SELECT b.RoleName FROM {} AS a INNER JOIN {} AS b ON a.RoleID = b.RoleID WHERE a.Email = ?".format(self.tablename, self.roleTableName), (email,))
                    result = cur.fetchall()

                    if len(result) == 1:
                        usernamecount = result[0][0]
                        return usernamecount
                    
                    else:
                        return "Error fetching role"
            
            else:
                return "Error fetching role"

            
        except Exception as ex:
            return("Error fetching role")
        finally:
            con.close()
            print("Successfully closed connection")

    def create_user(self, username, email, password, contactNumber):
        try:
            
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                
                cur = con.cursor()

                # checks if the username is already used in the db
                cur.execute("SELECT COUNT(Username) FROM {} WHERE Username = ?".format(self.tablename), (username,))
                result = cur.fetchall()
                usernamecount = result[0][0]

                # checks if the email is already used in the db
                cur.execute("SELECT COUNT(Email) FROM {} WHERE Email = ?".format(self.tablename), (email,))
                result2 = cur.fetchall()
                emailcount = result2[0][0]

                # if no same username and email is in the db, create user, else return error message
                if usernamecount == 0 and emailcount == 0:

                    cur.execute("SELECT RoleID FROM {} WHERE RoleName = ?".format(self.roleTableName), ("User",))
                    result3 = cur.fetchall()

                    roleID = result3[0][0]

                    cur.execute("SELECT AccountStatusID FROM {} WHERE AccountStatusName = ?".format(self.accountStatusTableName), ("Active",))
                    result4 = cur.fetchall()

                    accountStatusID = result4[0][0]

                    # if the role id and account status id is retrieved successfully
                    if roleID is not None and roleID > 0 and accountStatusID is not None and accountStatusID > 0:

                        if password != "" and password is not None:
                            
                            hashpassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                            con.execute("INSERT INTO {} (Username, Email, Password, ContactNumber, RoleID, AccountStatusID, LoginAttemptCount, LastLoginAttemptTime) VALUES (?,?,?,?,?,?,?,?)".format(self.tablename),(username,email, hashpassword, contactNumber, roleID, accountStatusID, 0, 0))
                            con.commit()
                            return("Successfully created user account")
                        else:
                            return("Error password cannot be empty")
                    else:
                        return("Error in Inserting User")
                
                else:
                    return("Error username or email is already in use")

        except sqlite3.Error as er:
            con.rollback()
            return("Error in Inserting User")
      
        finally:
            con.close()
            print("Successfully closed connection")


    def update_profile(self, email, username, contactnumber):
        try:
            
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()

                # checks if the username is already used in the db
                cur.execute("SELECT COUNT(Username) FROM {} WHERE Username = ?".format(self.tablename), (username,))
                result = cur.fetchall()
                usernamecount = result[0][0]

                # if no same username is in the db, create user, else return error message
                if usernamecount == 0:
                    con.execute("UPDATE {} SET Username = ?, ContactNumber = ? WHERE Email = ?".format(self.tablename), ( username, contactnumber, email) )
                    con.commit()
                    return("Successfully Updated User Profile")
                
                else:
                    return("Error username is already in use")


        except sqlite3.Error as er:
            print(er)
            con.rollback()
            return("Error in Updating User Profile")
      
        finally:
            con.close()
            print("Successfully closed connection")

    


    def create_transaction(self, transactionDetails):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                bookTitle = transactionDetails[0]
                bookPrice = transactionDetails[1]
                ownerEmail = transactionDetails[2]
                purchaserEmail = transactionDetails[3]

                cur = con.cursor()
                cur.execute("INSERT INTO {} (BookTitle, Price, Email, PurchaserEmail) VALUES(?,?,?,?)".format(self.transactionsTableName), (bookTitle, bookPrice, ownerEmail, purchaserEmail))
                con.commit()
                return("Successfully Created Transaction")

        except sqlite3.Error as er:
            con.rollback()
            return("Error failed to create transaction")

        except Exception as e:
            return("Error in fetching books")
            
        finally:
            con.close()
            print("Successfully closed connection")

    def get_transaction_details(self, transactionID):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()
                cur.execute("SELECT * FROM {} WHERE TransactionID = ?".format(self.transactionsTableName), (transactionID,))
                transactionInfo = cur.fetchall()[0]

                cur.execute("SELECT ContactNumber FROM {} WHERE Email = ?".format(self.tablename), (transactionInfo[3],))
                contactNumber = cur.fetchall()[0][0]
                return({'TransactionID': transactionInfo[0], 'BookTitle': transactionInfo[1], 'Price': transactionInfo[2], 'Owner': transactionInfo[3], 'OwnerPhoneNumber': contactNumber, 'PurchaserEmail': transactionInfo[4]})

        except sqlite3.Error as er:
            con.rollback()
            return("Error failed to get transaction")
      
        finally:
            con.close()
            print("Successfully closed connection")


    def get_all_user_transactions(self, email):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()
                cur.execute("SELECT * FROM {} WHERE PurchaserEmail = ? OR Email = ?".format(self.transactionsTableName), (email, email))
                transactionRows = cur.fetchall()

                if len(transactionRows) > 0:
                    returnList = []
                    for transaction in transactionRows:
                        cur.execute("SELECT ContactNumber FROM {} WHERE Email = ?".format(self.tablename), (transaction[3],))
                        contactNumber = cur.fetchall()[0][0]

                        returnList.append({'TransactionID': transaction[0], 'BookTitle': transaction[1], 'Price': transaction[2], 'Owner': transaction[3], 'OwnerPhoneNumber': contactNumber, 'PurchaserEmail': transaction[4]})
                    return (returnList)
                else:
                    return("No transactions found")

        except sqlite3.Error as er:
            con.rollback()
            return("Error failed to get transaction")
        
        except Exception as e:
            return("Error in fetching books")
      
        finally:
            con.close()
            print("Successfully closed connection")

    def get_key(self):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()
                cur.execute("SELECT Password FROM {} WHERE Email = ?".format(self.tablename), ("superadmin@gmail.com",))
                resultRows = cur.fetchall()

                if resultRows is not None and len(resultRows) == 1:
                    
                    return (resultRows[0][0])
                else:
                    return(None)

        except sqlite3.Error as er:
            con.rollback()
            return(None)
        
        except Exception as ex:
            return(None)
      
        finally:
            con.close()
            print("Successfully closed connection")


        