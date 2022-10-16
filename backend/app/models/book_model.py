import sqlite3
from tokenize import Double
from flask import current_app, url_for
from .data_cleaning import *

class Book:

    def __init__(self):
        self.dbname = "database"
        self.tablename = "Book"
        self.bookstatustablename = "BookStatus"
        self.genretablename = "Genre"
        self.locationtablename = "Location"
        self.bookconditiontablename = "BookCondition"
        self.bookofferstatustablename = "BookOfferStatus"
        self.bookoffertablename = "BookOffers"
    
    def get_all_genres(self):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                cur = con.cursor()
                cur.execute("SELECT * FROM {}".format(self.genretablename))
                rows = cur.fetchall()
                   
                # test print db records
                if len(rows) > 0:

                    # creates a return list for key value pair
                    dataList = []
                    for row in rows:

                        dataList.append({'GenreID': row[0], 'GenreName': row[1]})

                    return (dataList)
                else:
                    return("Error no Genres in database") 
        except sqlite3.Error as er:
            con.rollback()
            return("Error in fetching genres")

        finally:
            con.close()
            print("Successfully closed connection")
    
    def get_all_locations(self):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                cur = con.cursor()
                cur.execute("SELECT * FROM {}".format(self.locationtablename))
                rows = cur.fetchall()
                   
                # test print db records
                if len(rows) > 0:
                    # creates a return list for key value pair
                    dataList = []
                    for row in rows:

                        dataList.append({"LocationID": row[0], "LocationName": row[1]})
                    return (dataList)
                else:
                    return("Error no locations in database") 
        except sqlite3.Error as er:
            con.rollback()
            return("Error in fetching locations")

        finally:
            con.close()
            print("Successfully closed connection")

    def get_all_book_conditions(self):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                cur = con.cursor()
                cur.execute("SELECT * FROM {}".format(self.bookconditiontablename))
                rows = cur.fetchall()
                   
                # test print db records
                if len(rows) > 0:
                    # creates a return list for key value pair
                    dataList = []
                    for row in rows:

                        dataList.append({"BookConditionID": row[0], "BookConditionName": row[1]})
                    return (dataList)
                else:
                    return("Error no Book Conditions in database") 
        except sqlite3.Error as er:
            con.rollback()
            return("Error in fetching Book Conditions")

        finally:
            con.close()
            print("Successfully closed connection")


    def create_book(self, title, price, description, genreID, email, image, locationID, bookConditionID):
        try:

            # checks if the values are none or "", if all are not, start insertion
            if title is not None and price is not None and description is not None and genreID is not None and email is not None and image is not None and locationID is not None:
                if title != "" and price != "" and description != "" and genreID != "" and email != "" and image != "" and locationID != "":
                    with sqlite3.connect(self.dbname + ".db") as con:
                        print ("Opened database successfully")
                        
                        # this command forces sqlite to enforce the foreign key rules set  for the tables
                        con.execute("PRAGMA foreign_keys = 1")

                        cur = con.cursor()

                        # fetches the bookstatus id for the status Avaliable
                        cur.execute("SELECT BookStatusID FROM {} WHERE BookStatusName = ?".format(self.bookstatustablename), ("Avaliable",))
                        result = cur.fetchall()
                        bookStatusID = result[0][0]

                        # inserts the data required for the book into the database
                        # bookstatus by default is "Avaliable" when first created
                        cur.execute("INSERT INTO {}(Title, Price, BookStatusID, Description, GenreID, Email, Image, LocationID, BookConditionID) VALUES (?,?,?,?,?,?,?,?,?)".format(self.tablename), (title, price, bookStatusID, description, genreID, email, image, locationID, bookConditionID))
                        con.commit()
                        #return("successfully created book")
                        return True
                
            return False

        except sqlite3.Error as er:
            con.rollback()
            #return("Error in creating book")
            return False

        finally:
            con.close()
            print("Successfully closed connection")
    
    def search_book(self, bookTitle = None, userEmail = None, genreFilter = None, locationFilter = None, bookConditionFilter = None, minPriceFilter = None, maxPriceFilter = None):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()
                #cur.execute("SELECT * FROM {}".format(self.tablename))

                # SELECT a.bookID, a.Title, a.Price, a.Description, a.Image, b.GenreName, c.LocationName, d.BookConditionName FROM Book AS a 
                # INNER JOIN Genre AS b ON a.GenreID = b.GenreID INNER JOIN Location AS c ON a.LocationID = c.LocationID 
                # INNER JOIN BookCondition AS d ON a.BookConditionID = d.BookConditionID
                # INNER JOIN BookStatus AS e ON a.BookStatusID = e.BookStatusID 
                # WHERE a.Email != "test4@gmail.com" 
                # AND e.BookStatusName = "Avaliable" 
                # AND a.Price >= 0
                # AND a.Price <= 5
                # AND b.GenreID in (0, 1, 2)
                # AND c.LocationID in (1) 
                # AND d.BookConditionID in (0);
                
                queryStorage = []
                filterQuery = ""

                if userEmail is not None:


                    if userEmail != "" and isemail(userEmail):
                        queryStorage.append("a.Email != \"{}\"".format(userEmail))

                # checks if title is None, if not none build the command for title filter
                if bookTitle is not None:

                    filteredBookTitle = data_cleaning(bookTitle)
                    # check if the values is not empty string
                    if filteredBookTitle != "":

                        queryStorage.append("a.Title LIKE \"{}\"".format("%" + filteredBookTitle + "%"))

                # checks if min and max price filter is None, if not none build the command for min and max price filter
                if minPriceFilter is not None and maxPriceFilter is not None:
                    
                    # check if the values is not negative
                    if float(minPriceFilter) >= 0 and float(maxPriceFilter) >= 0 and isfloat(minPriceFilter) and isfloat(maxPriceFilter):

                        queryStorage.append("a.Price >= {} AND a.Price <= {} ".format(float(minPriceFilter), float(maxPriceFilter)))
                    
                elif minPriceFilter is not None and maxPriceFilter is None and isfloat(minPriceFilter):

                    # check if the values is not negative
                    if float(minPriceFilter) >= 0:

                        queryStorage.append("a.Price >= {} ".format(float(minPriceFilter)))
                    
                elif minPriceFilter is None and maxPriceFilter is not None and isfloat(maxPriceFilter):

                    # check if the values is not negative
                    if float(maxPriceFilter) >= 0:

                        queryStorage.append("a.Price <= {} ".format(float(maxPriceFilter)))


                # checks if genre is None, if not none build the command for genre filter
                if genreFilter is not None:
                    tempData = "("
                    for idx, genre in enumerate(genreFilter):
                        tempData += str(genre)
                        if idx < len(genreFilter) - 1:
                            tempData += ","
                        else:
                            tempData += ")"

                        
                    queryStorage.append("b.GenreID in {}".format(tempData))


                # checks if location is None, if not none build the command for location filter
                if locationFilter is not None:
                    tempData2 = "("
                    for idx, location in enumerate(locationFilter):
                        tempData2 += str(location)
                        if idx < len(locationFilter) - 1:
                            tempData2 += ","
                        else:
                            tempData2 += ")"

                        
                    queryStorage.append("c.LocationID in {}".format(tempData2))

                
                # checks if book Condition Query is None, if not none build the command for book Condition Query filter
                if bookConditionFilter is not None:
                    tempData3 = "("
                    for idx, bookCondition in enumerate(bookConditionFilter):
                        tempData3 += str(bookCondition)
                        if idx < len(bookConditionFilter) - 1:
                            tempData3 += ","
                        else:
                            tempData3 += ")"

                        
                    queryStorage.append("a.BookConditionID in {}".format(tempData3))

                # if there are queries
                if len(queryStorage) > 0:
                    for idx, query in enumerate(queryStorage):
                        
                        # checks if it is not the last object in the list, as sql commands cannot have "AND" at the end with no values to compare
                        if query != "" and idx < len(queryStorage) - 1:
                            filterQuery += query + " AND "

                        elif query != "" and idx < len(queryStorage):
                            filterQuery += query
                
                print("filter query is {}".format(filterQuery))

                if filterQuery != "":
                    cur.execute("SELECT a.bookID, a.Title, a.Price, a.Description, a.Image, b.GenreName, c.LocationName, d.BookConditionName  FROM {} AS a INNER JOIN {} AS b ON a.GenreID = b.GenreID INNER JOIN {} AS c ON a.LocationID = c.LocationID INNER JOIN {} AS d ON a.BookConditionID = d.BookConditionID INNER JOIN {} AS e ON a.BookStatusID = e.BookStatusID WHERE e.BookStatusName = ? AND {}".format(self.tablename, self.genretablename, self.locationtablename, self.bookconditiontablename, self.bookstatustablename, filterQuery), ("Avaliable",))
                else:
                    cur.execute("SELECT a.bookID, a.Title, a.Price, a.Description, a.Image, b.GenreName, c.LocationName, d.BookConditionName  FROM {} AS a INNER JOIN {} AS b ON a.GenreID = b.GenreID INNER JOIN {} AS c ON a.LocationID = c.LocationID INNER JOIN {} AS d ON a.BookConditionID = d.BookConditionID INNER JOIN {} AS e ON a.BookStatusID = e.BookStatusID WHERE e.BookStatusName = ?".format(self.tablename, self.genretablename, self.locationtablename, self.bookconditiontablename, self.bookstatustablename), ("Avaliable",))
                rows = cur.fetchall()
                   
                # if there are book records found:
                if len(rows) > 0:
                    print("rows of records:")
                    returnData = []
                    for records in rows:
                        print(records)


                        # builds the image url
                        fileurl = url_for('static', filename='BookImages/{}'.format(records[4]))
                        imgurl = "http://127.0.0.1:5000" + fileurl

                        # creates a dictonary for each book record and inserts into a list for return
                        roledict = {'BookID': records[0], 'Title': records[1], 'Price': records[2], 'Description': records[3], 'Image': imgurl, 'Genre': records[5], 'Location': records[6], 'BookCondition': records[7]}
                        returnData.append(roledict)
                    return(returnData)
                else:
                    return("No results found") 

        except sqlite3.Error as er:
            con.rollback()
            return("Error in fetching books")

        except Exception as e:
            return("Error in fetching books")
        finally:
            con.close()
            print("Successfully closed connection")

    def get_all_available_books(self, userEmail, genreFilter = None, locationFilter = None, bookConditionFilter = None, minPriceFilter = None, maxPriceFilter = None):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()
                #cur.execute("SELECT * FROM {}".format(self.tablename))

                # SELECT a.bookID, a.Title, a.Price, a.Description, a.Image, b.GenreName, c.LocationName, d.BookConditionName FROM Book AS a 
                # INNER JOIN Genre AS b ON a.GenreID = b.GenreID INNER JOIN Location AS c ON a.LocationID = c.LocationID 
                # INNER JOIN BookCondition AS d ON a.BookConditionID = d.BookConditionID
                # INNER JOIN BookStatus AS e ON a.BookStatusID = e.BookStatusID 
                # WHERE a.Email != "test4@gmail.com" 
                # AND e.BookStatusName = "Avaliable" 
                # AND a.Price >= 0
                # AND a.Price <= 5
                # AND b.GenreID in (0, 1, 2)
                # AND c.LocationID in (1) 
                # AND d.BookConditionID in (0);

                minmaxQuery = ""
                genreQuery = ""
                locationQuery = ""
                bookConditionQuery = ""
                filterQuery = ""
                # checks if min and max price filter is None, if not none build the command for min and max price filter
                if minPriceFilter is not None and maxPriceFilter is not None:
                    
                    # check if the values is not negative
                    if minPriceFilter >= 0 and maxPriceFilter >= 0:

                        minmaxQuery += "a.Price >= {} AND a.Price <= {} ".format(minPriceFilter, maxPriceFilter)
                    
                elif minPriceFilter is not None and maxPriceFilter is None:

                    # check if the values is not negative
                    if minPriceFilter >= 0:

                        minmaxQuery += "a.Price >= {} ".format(minPriceFilter)
                    
                elif minPriceFilter is None and maxPriceFilter is not None:

                    # check if the values is not negative
                    if maxPriceFilter >= 0:

                        minmaxQuery += "a.Price <= {} ".format(maxPriceFilter)


                # checks if genre is None, if not none build the command for genre filter
                if genreFilter is not None:
                    tempData = "("
                    for idx, genre in enumerate(genreFilter):
                        tempData += str(genre)
                        if idx < len(genreFilter) - 1:
                            tempData += ","
                        else:
                            tempData += ")"

                        
                    genreQuery += "b.GenreID in {}".format(tempData)


                # checks if location is None, if not none build the command for location filter
                if locationFilter is not None:
                    tempData2 = "("
                    for idx, location in enumerate(locationFilter):
                        tempData2 += str(location)
                        if idx < len(locationFilter) - 1:
                            tempData2 += ","
                        else:
                            tempData2 += ")"

                        
                    locationQuery += "b.LocationID in {}".format(tempData2)

                
                # checks if book Condition Query is None, if not none build the command for book Condition Query filter
                if bookConditionFilter is not None:
                    tempData3 = "("
                    for idx, bookCondition in enumerate(bookConditionFilter):
                        tempData3 += str(bookCondition)
                        if idx < len(bookConditionFilter) - 1:
                            tempData3 += ","
                        else:
                            tempData3 += ")"

                        
                    bookConditionQuery += "b.BookConditionID in {}".format(tempData3)

                filterQuery += minmaxQuery + genreQuery + locationQuery + bookConditionQuery
                print(filterQuery)

                if filterQuery == "":
                    cur.execute("SELECT a.bookID, a.Title, a.Price, a.Description, a.Image, b.GenreName, c.LocationName, d.BookConditionName  FROM {} AS a INNER JOIN {} AS b ON a.GenreID = b.GenreID INNER JOIN {} AS c ON a.LocationID = c.LocationID INNER JOIN {} AS d ON a.BookConditionID = d.BookConditionID INNER JOIN {} AS e ON a.BookStatusID = e.BookStatusID WHERE a.Email != ? AND e.BookStatusName = ?".format(self.tablename, self.genretablename, self.locationtablename, self.bookconditiontablename, self.bookstatustablename), (userEmail, "Avaliable"))
                
                else:
                    cur.execute("SELECT a.bookID, a.Title, a.Price, a.Description, a.Image, b.GenreName, c.LocationName, d.BookConditionName  FROM {} AS a INNER JOIN {} AS b ON a.GenreID = b.GenreID INNER JOIN {} AS c ON a.LocationID = c.LocationID INNER JOIN {} AS d ON a.BookConditionID = d.BookConditionID INNER JOIN {} AS e ON a.BookStatusID = e.BookStatusID WHERE a.Email != ? AND e.BookStatusName = ? AND {}".format(self.tablename, self.genretablename, self.locationtablename, self.bookconditiontablename, self.bookstatustablename, filterQuery), (userEmail, "Avaliable"))
                
                rows = cur.fetchall()
                   
                # if there are book records found:
                if len(rows) > 0:
                    print("rows of records:")
                    returnData = []
                    for records in rows:
                        print(records)


                        # builds the image url
                        fileurl = url_for('static', filename='BookImages/{}'.format(records[4]))
                        imgurl = "http://127.0.0.1:5000" + fileurl

                        # creates a dictonary for each book record and inserts into a list for return
                        roledict = {'BookID': records[0], 'Title': records[1], 'Price': records[2], 'Description': records[3], 'Image': imgurl, 'Genre': records[5], 'Location': records[6], 'BookCondition': records[7]}
                        returnData.append(roledict)
                    return(returnData)
                else:
                    return("Error no records in database") 

        except sqlite3.Error as er:
            con.rollback()
            return("Error in fetching books")

        finally:
            con.close()
            print("Successfully closed connection")


    def get_all_user_books(self, email):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                cur = con.cursor()

                #fetches the books the user has created
                cur.execute("SELECT a.bookID, a.Title, a.Price, a.Description, a.Image, b.GenreName, c.LocationName, d.BookConditionName, e.BookStatusName  FROM {} AS a INNER JOIN {} AS b ON a.GenreID = b.GenreID INNER JOIN {} AS c ON a.LocationID = c.LocationID INNER JOIN {} AS d ON a.BookConditionID = d.BookConditionID INNER JOIN {} AS e ON a.BookStatusID = e.BookStatusID WHERE a.Email = ?".format(self.tablename, self.genretablename, self.locationtablename, self.bookconditiontablename, self.bookstatustablename), (email,))
                rows = cur.fetchall()
                   
                # if there are book records, fetches the status, genre and builds the image  url for front end use
                if len(rows) > 0:
                    print("rows of records:")
                    returnData = []
                    for records in rows:
                        print(records)

                        # builds the image url
                        fileurl = url_for('static', filename='BookImages/{}'.format(records[4]))
                        imgurl = "http://127.0.0.1:5000" + fileurl

                        # creates a dictonary for each book record and inserts into a list for return
                        roledict = roledict = {'BookID': records[0], 'Title': records[1], 'Price': records[2], 'Description': records[3], 'Image': imgurl, 'Genre': records[5], 'Location': records[6], 'BookCondition': records[7], 'BookStatus': records[8]}
                        returnData.append(roledict)
                    return(returnData)
                else:
                    return("No records in database") 

        except sqlite3.Error as er:
            con.rollback()
            return("Error in fetching books")

        finally:
            con.close()
            print("Successfully closed connection")


    def get_book_offers(self, bookID, ownerEmail, userTableName):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                cur = con.cursor()

                # check if the book belongs to the user
                cur.execute("SELECT COUNT(*) FROM {} WHERE Email = ? AND BookID = ?".format(self.tablename), (ownerEmail, bookID))
                recordCount = cur.fetchall()

                if recordCount[0][0] == 1:

                    cur.execute("SELECT a.BookOfferID, a.BookID, a.OfferPrice, b.BookOfferStatusName, c.Username FROM {} AS a INNER JOIN {} AS b ON a.BookOfferStatusID = b.BookOfferStatusID INNER JOIN {} AS c ON a.OffererEmail = c.Email WHERE a.BookID = ?".format(self.bookoffertablename, self.bookofferstatustablename, userTableName), (bookID,))
                    rows = cur.fetchall()
                    # if there are book offer records for selected bookid, fetches the BookOfferID, BookID, OfferPrice, BookOfferStatusName, Username and BookOffers 
                    if len(rows) > 0:
                        dataList = []
                        for row in rows:
                            dataList.append({'BookOfferID': row[0], 'BookID': row[1], 'OfferPrice': row[2], 'BookOfferStatus': row[3], 'Username': row[4]})
                            
                        return dataList
                    else:
                        return("No book offers found")
                
                else:
                    return("Error Book Does not belong to user")

        except sqlite3.Error as er:
            con.rollback()
            return("Error in fetching book offers")

        finally:
            con.close()
            print("Successfully closed connection")


    def get_all_user_book_offers(self, OffererEmail):
        try:
            
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")

                if OffererEmail is not None and isemail(OffererEmail):
                    cur = con.cursor()

                    # gets 
                    cur.execute("SELECT a.BookOfferID, a.BookID, c.Title, a.OfferPrice, b.BookOfferStatusName FROM {} AS a INNER JOIN {} AS b ON a.BookOfferStatusID = b.BookOfferStatusID INNER JOIN {} AS c ON a.BookID = c.BookID  WHERE a.OffererEmail = ?".format(self.bookoffertablename,self.bookofferstatustablename,self.tablename), (OffererEmail,))
                    offerRecords = cur.fetchall()

                    if len(offerRecords) > 0:

                        dataList = []
                        for offers in offerRecords:

                            dataList.append({'BookOfferID': offers[0], 'BookID': offers[1],'BookTitle': offers[2], 'OfferPrice': offers[3], 'BookOfferStatus': offers[4]})
                                
                        return dataList
                    else:
                        return("No book offers found")
                
                else:
                    return("No book offers found")
                

        except sqlite3.Error as er:
            con.rollback()
            return("Error in fetching book offers")

        finally:
            con.close()
            print("Successfully closed connection")

    # def add_book_offer(self, bookID, email, offer):
    #     try:
        
    #         with sqlite3.connect(self.dbname + ".db") as con:
    #             print ("Opened database successfully")

    #             # this command forces sqlite to enforce the foreign key rules set  for the tables
    #             con.execute("PRAGMA foreign_keys = 1")
                
    #             returnResult = False
    #             # checks if the row exists
    #             cur = con.cursor()
    #             cur.execute("SELECT BookID, OffererEmail FROM {} WHERE BookID = ? AND OffererEmail = ?".format(self.bookoffertablename),(bookID, email))
    #             rows = cur.fetchall()
    #             print(rows)
    #             # if there are no book offer records for selected bookid and email, insert offer, else return error message
    #             if len(rows) == 0:
    #                 print("no offers from  this user found, inserting offer")
    #                 cur.execute("SELECT BookOfferStatusID FROM {} WHERE BookOfferStatusName = ?".format(self.bookofferstatustablename),("Pending",))
    #                 result = cur.fetchall()

    #                 if len(result) == 1:
    #                     bookOfferStatusID = result[0][0]
    #                     cur.execute("INSERT INTO {} (BookID,OfferPrice,BuyerEmail,BookOfferStatusID) VALUES (?, ?, ?, ?)".format(self.bookoffertablename), (bookID, offer, email, bookOfferStatusID))
    #                     returnResult = True
    #             return returnResult

    #     except sqlite3.Error as er:
    #         con.rollback()
    #         returnResult = None
    #         return returnResult

    #     finally:
    #         con.close()
    #         print("Successfully closed connection")

    def delete_book_offer(self, bookOfferID, bookID, email):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")
                
                returnResult = False
                # checks if the row exists
                cur = con.cursor()
                cur.execute("SELECT b.BookOfferStatusName FROM {} as a INNER JOIN {} AS b WHERE a.BookOfferID = ? AND a.BookID = ? AND a.OffererEmail = ? AND b.BookOfferStatusName != ?".format(self.bookoffertablename, self.bookofferstatustablename), (bookOfferID, bookID, email, "Accepted"))
                rows = cur.fetchall()
                # if there are a exact book offer records for selected bookid and email, delete offer, else return error message
                if len(rows) == 1:

                    cur.execute("DELETE FROM {} WHERE BookOfferID = ? AND BookID = ? AND OffererEmail = ?".format(self.bookoffertablename),(bookOfferID, bookID, email))
                    returnResult = True
                return returnResult

        except sqlite3.Error as er:
            con.rollback()
            returnResult = None
            return returnResult

        finally:
            con.close()
            print("Successfully closed connection")


    def search_book_by_title(self, userEmail, bookTitle):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                

                
                cur = con.cursor()

                # if user is logged in, hide user books
                if userEmail is not None:
                    cur.execute("SELECT a.bookID, a.Title, a.Price, a.Description, a.Image, b.GenreName, c.LocationName, d.BookConditionName  FROM {} AS a INNER JOIN {} AS b ON a.GenreID = b.GenreID INNER JOIN {} AS c ON a.LocationID = c.LocationID INNER JOIN {} AS d ON a.BookConditionID = d.BookConditionID INNER JOIN {} AS e ON a.BookStatusID = e.BookStatusID WHERE a.Email != ? AND a.Title LIKE ? AND e.BookStatusName = ?".format(self.tablename, self.genretablename, self.locationtablename, self.bookconditiontablename, self.bookstatustablename), (userEmail, "%" + bookTitle + "%", "Avaliable"))
                
                # if no user email is provided when not logged in:
                else:
                    cur.execute("SELECT a.bookID, a.Title, a.Price, a.Description, a.Image, b.GenreName, c.LocationName, d.BookConditionName  FROM {} AS a INNER JOIN {} AS b ON a.GenreID = b.GenreID INNER JOIN {} AS c ON a.LocationID = c.LocationID INNER JOIN {} AS d ON a.BookConditionID = d.BookConditionID INNER JOIN {} AS e ON a.BookStatusID = e.BookStatusID WHERE a.Title LIKE ? AND e.BookStatusName = ?".format(self.tablename, self.genretablename, self.locationtablename, self.bookconditiontablename, self.bookstatustablename), ("%" + bookTitle + "%", "Avaliable"))
                rows = cur.fetchall()
                   
                # if there are book records found:
                if len(rows) > 0:
                    print("rows of records:")
                    returnData = []
                    for records in rows:
                        print(records)


                        # builds the image url
                        fileurl = url_for('static', filename='BookImages/{}'.format(records[4]))
                        imgurl = "http://127.0.0.1:5000" + fileurl

                        # creates a dictonary for each book record and inserts into a list for return
                        roledict = {'BookID': records[0], 'Title': records[1], 'Price': records[2], 'Description': records[3], 'Image': imgurl, 'Genre': records[5], 'Location': records[6], 'BookCondition': records[7]}
                        returnData.append(roledict)
                    return(returnData)
                else:
                    return("No records in database") 

        except sqlite3.Error as er:
            print(er)
            con.rollback()
            return("Error in fetching books")

        finally:
            con.close()
            print("Successfully closed connection")


    def search_book_by_ID(self, bookID):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()
                cur.execute("SELECT Title, Price, email FROM {} WHERE BookID = ?".format(self.tablename), (bookID,))
                result = cur.fetchall()

                # if there are a matchin book record, fetches the title and price
                # this ensures that only 1 record is returned
                if len(result) == 1 :
                    return(result)
                else:
                    return("Error in fetching book details") 

        except sqlite3.Error as er:
            con.rollback()
            return("Error in fetching book details")

        finally:
            con.close()
            print("Successfully closed connection")

    def update_book_details(self, bookID, title, price, description, genreID, image, locationID):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()
                cur.execute("UPDATE {} SET Title = ?, Price = ?, Description = ?, GenreID = ?, Image = ?, LocationID = ? WHERE BookID = ?".format(self.tablename),(title, price, description, genreID, image, locationID, bookID))
                #rows = cur.fetchall()
                #print(rows)
                con.commit()
                return("successfully updated")

        except sqlite3.Error as er:
            con.rollback()
            return("Error in updating book")

        finally:
            con.close()
            print("Successfully closed connection")

    def delete_book(self, bookID, ownerEmail):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                cur = con.cursor()
                cur.execute("DELETE FROM {} WHERE BookID = ? AND Email = ?".format(self.tablename), (bookID, ownerEmail))
                con.commit()
                return("successfully deleted")

        except sqlite3.Error as er:
            con.rollback()
            return("Error in deleting book")

        finally:
            con.close()
            print("Successfully closed connection")

    def send_book_offer(self, bookID, offer, email):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()
                
                # checks if the book belongs to the offerer email
                cur.execute("SELECT COUNT(*) FROM {} WHERE Email = ? AND BookID = ?".format(self.tablename), (email, bookID))
                bookCount = cur.fetchall()[0][0]

                # if the book does not belong to the offerer email, check if a offer for the book is already made by offer email
                # else return false as the book cannot have owners making offers on their own books
                if bookCount == 0:

                    # tries to fetch a record if previous offer for the same bookid and email
                    cur.execute("SELECT COUNT(*) FROM {} WHERE BookID = ? AND OffererEmail = ?".format(self.bookoffertablename), (bookID, email))
                    recordCount = cur.fetchall()[0][0]

                    # if there is a record for the book with the same offerer email, return error, else proceed to insert
                    if recordCount == 0:

                        # gets the status ID relating to "Pending" book status
                        cur.execute("SELECT BookOfferStatusID FROM {} WHERE BookOfferStatusName = ?".format(self.bookofferstatustablename), ("Pending",))
                        bookOfferStatusID = cur.fetchall()[0][0]

                        con.execute("INSERT INTO {} (BookID,OfferPrice,OffererEmail,BookOfferStatusID) VALUES(?,?,?,?)".format(self.bookoffertablename), (bookID, offer, email, bookOfferStatusID))
                        con.commit()
                        return("Successfully Sent Offer")

                    else:
                        return("Error cannot send offer again for same Book")

                else:
                    return("Error cannot send offer for own Book")

        except sqlite3.Error as er:
            con.rollback()
            return("Error sending offer for Book")

        finally:
            con.close()
            print("Successfully closed connection") 

    def accept_book_offer(self, bookOfferID, ownerEmail):
        try:
            if bookOfferID is not None and ownerEmail is not None:
                with sqlite3.connect(self.dbname + ".db") as con:
                    print ("Opened database successfully")
                    
                    # this command forces sqlite to enforce the foreign key rules set  for the tables
                    con.execute("PRAGMA foreign_keys = 1")

                    cur = con.cursor()
                    
                    # checks if the book offer belongs to the owner email
                    cur.execute("SELECT COUNT(*) FROM {} WHERE BookOfferID = ? AND OffererEmail = ?".format(self.bookoffertablename), (bookOfferID, ownerEmail))
                    bookCount = cur.fetchall()[0][0]

                    # if the offer does not belong to the owner email, check if the offer is not Accepted or Rejected
                    if bookCount == 0:

                        # tries to fetch a record of the BookOfferID with "Pending" status
                        cur.execute("SELECT COUNT(*) FROM {} AS a INNER JOIN {} AS b ON a.BookOfferStatusID = b.BookOfferStatusID WHERE a.BookOfferID = ? AND b.BookOfferStatusName = ?".format(self.bookoffertablename, self.bookofferstatustablename), (bookOfferID, "Pending"))
                        recordCount = cur.fetchall()[0][0]
                        # if there is a record for the book offer with the same bookOfferID and with "Pending" status, proceed to update, else return error
                        if recordCount == 1:

                            # gets the status ID relating to "Accepted" book status
                            cur.execute("SELECT BookOfferStatusID FROM {} WHERE BookOfferStatusName = ?".format(self.bookofferstatustablename), ("Accepted",))
                            bookOfferStatusID = cur.fetchall()[0][0]
                            con.execute("UPDATE {} SET BookOfferStatusID = ? WHERE BookOfferID = ?".format(self.bookoffertablename), (bookOfferStatusID, bookOfferID))

                            # getting setting book status of sold to set bookstatus to sold:
                            
                            cur.execute("SELECT BookID FROM {} WHERE BookOfferID = ?".format(self.bookoffertablename),(bookOfferID,))
                            bookID = cur.fetchall()[0][0]

                            cur.execute("SELECT BookStatusID FROM {} WHERE BookStatusName = ?".format(self.bookstatustablename), ("Sold",))
                            bookStatusID = cur.fetchall()[0][0]

                            # builds the return data for transaction
                            if bookID is not None:

                                con.execute("UPDATE {} SET BookStatusID = ? WHERE BookID = ?".format(self.tablename), (bookStatusID, bookID))
                                returnData = []
                                
                                cur.execute("SELECT Title, Email FROM {} WHERE BookID = ?".format(self.tablename),(bookID,))
                                bookInfo = cur.fetchall()[0]

                                cur.execute("SELECT OffererEmail, OfferPrice FROM {} WHERE BookOfferID = ?".format(self.bookoffertablename), (bookOfferID,))
                                offerInfo = cur.fetchall()[0]

                                returnData.append(bookInfo[0])
                                returnData.append(offerInfo[1])
                                returnData.append(bookInfo[1])
                                returnData.append(offerInfo[1])
                                
                                return(returnData)
                            
                            con.commit()
                        else:
                            return("Error Accepting offer for Book")

                    else:
                        return("Error Accepting offer for Book")
            else:
                return("Error Accepting offer for Book")

        except sqlite3.Error as er:
            con.rollback()
            print(er)
            return("Error Accepting offer for Book")

        finally:
            con.close()
            print("Successfully closed connection") 
    

    def edit_book_offer(self, bookOfferID, offererEmail, newOffer):
        try:
            if bookOfferID is not None and offererEmail is not None and newOffer is not None:
                with sqlite3.connect(self.dbname + ".db") as con:
                    print ("Opened database successfully")
                    
                    # this command forces sqlite to enforce the foreign key rules set  for the tables
                    con.execute("PRAGMA foreign_keys = 1")

                    cur = con.cursor()
                    
                    # checks if the book offer belongs to the offerer email
                    cur.execute("SELECT COUNT(*) FROM {} WHERE BookOfferID = ? AND OffererEmail = ?".format(self.bookoffertablename), (bookOfferID, offererEmail))
                    bookCount = cur.fetchall()[0][0]

                    # if the offer belong to the offerer email, check if the offer is not Accepted
                    if bookCount == 1:
                        
                        # tries to fetch a record of the BookOfferID with "Pending" or "Rejected" status (Not Accepted)
                        cur.execute("SELECT COUNT(*) FROM {} AS a INNER JOIN {} AS b ON a.BookOfferStatusID = b.BookOfferStatusID WHERE a.BookOfferID = ? AND b.BookOfferStatusName != ?".format(self.bookoffertablename, self.bookofferstatustablename), (bookOfferID, "Accepted"))
                        recordCount = cur.fetchall()[0][0]

                        # if there is a record for the book offer with the same bookOfferID and with "Pending" or "Rejected" status, proceed to update offer and status back to "Pending", else return error
                        if recordCount == 1:

                            # gets the status ID relating to "Pending" book status
                            cur.execute("SELECT BookOfferStatusID FROM {} WHERE BookOfferStatusName = ?".format(self.bookofferstatustablename), ("Pending",))
                            bookOfferStatusID = cur.fetchall()[0][0]

                            con.execute("UPDATE {} SET BookOfferStatusID = ?, OfferPrice = ? WHERE BookOfferID = ?".format(self.bookoffertablename), (bookOfferStatusID, newOffer, bookOfferID))
                            con.commit()
            
                            return("Successfully edited book offer")
                        else:
                            return("Error no book offer found")

                    else:
                        return("Error failed to edit book offer")

        except sqlite3.Error as er:
            con.rollback()
            return("Error failed to edit book offer")

        finally:
            con.close()
            print("Successfully closed connection") 


    def delete_book_offer(self, bookOfferID, offererEmail):
        try:
        
            with sqlite3.connect(self.dbname + ".db") as con:
                print ("Opened database successfully")
                
                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()
                
                # checks if the book offer belongs to the offerer email
                cur.execute("SELECT COUNT(*) FROM {} WHERE BookOfferID = ? AND OffererEmail = ?".format(self.bookoffertablename), (bookOfferID, offererEmail))
                bookCount = cur.fetchall()[0][0]

                # if the offer belong to the offerer email, check if the offer is not Accepted
                if bookCount == 1:

                    # tries to fetch a record of the BookOfferID with "Pending" or "Rejected" status (Not Accepted)
                    cur.execute("SELECT COUNT(*) FROM {} AS a INNER JOIN {} AS b ON a.BookOfferStatusID = b.BookOfferStatusID WHERE a.BookOfferID = ? AND b.BookOfferStatusName != ?".format(self.bookoffertablename, self.bookofferstatustablename), (bookOfferID, "Accepted"))
                    recordCount = cur.fetchall()[0][0]

                    # if there is a record for the book offer with the same bookOfferID and with "Pending" or "Rejected" status, proceed to update offer and status back to "Pending", else return error
                    if recordCount == 1:

                        # gets the status ID relating to "Pending" book status
                        cur.execute("SELECT BookOfferStatusID FROM {} WHERE BookOfferStatusName = ?".format(self.bookofferstatustablename), ("Pending",))
                        bookOfferStatusID = cur.fetchall()[0][0]

                        con.execute("DELETE FROM {} WHERE BookOfferID = ? AND OffererEmail = ?".format(self.bookoffertablename), (bookOfferID, offererEmail))
                        con.commit()
                        return("Successfully deleted book offer")
                    else:
                        return("Error failed to deleted book offer")

                else:
                    return("Error failed to deleted book offer")

        except sqlite3.Error as er:
            con.rollback()
            return("Error failed to delete book offer")

        finally:
            con.close()
            print("Successfully closed connection") 