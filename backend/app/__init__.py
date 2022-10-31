from flask import Flask
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from .routes.user_routes import user
from .routes.book_routes import book
from .routes.admin_routes import admin
from .routes.super_admin_routes import superadmin
import sqlite3
import os, traceback
import bcrypt


jwt = JWTManager()
mail = Mail()

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData
def hash_Password(password):

    hashpassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashpassword

def mailSetup():
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "kopickosongml@gmail.com"
    MAIL_PASSWORD = "hEXRsOjFENbBkrcQEZS!"
    SECRET_KEY = 'secretkey'

def sqlite_database_setup():
    try:
        with sqlite3.connect("database.db") as con:
            print ("Opened database successfully")
            

            # this command forces sqlite to enforce the foreign key rules set  for the tables
            con.execute("PRAGMA foreign_keys = 1")

            # creates the tables required in the database
            # below tables are user related
            con.execute("CREATE TABLE IF NOT EXISTS AccountStatus(AccountStatusID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, AccountStatusName VARCHAR(255) NOT NULL)")
            con.execute("CREATE TABLE IF NOT EXISTS Role(RoleID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, RoleName VARCHAR(255) NOT NULL)")
            con.execute("CREATE TABLE IF NOT EXISTS User(Username VARCHAR(255) NOT NULL, Email VARCHAR(255) NOT NULL PRIMARY KEY, Password VARCHAR(255) NOT NULL, ContactNumber INTEGER NOT NULL, RoleID INTEGER NOT NULL, AccountStatusID INTEGER NOT NULL, FOREIGN KEY(RoleID) REFERENCES Role(RoleID), FOREIGN KEY(AccountStatusID) REFERENCES AccountStatus(AccountStatusID))")
            
            
            # below tables are book related
            con.execute("CREATE TABLE IF NOT EXISTS Genre(GenreID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, GenreName VARCHAR(255) NOT NULL)")
            con.execute("CREATE TABLE IF NOT EXISTS BookStatus(BookStatusID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, BookStatusName VARCHAR(255) NOT NULL)")
            con.execute("CREATE TABLE IF NOT EXISTS Location(LocationID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, LocationName VARCHAR(255) NOT NULL)")
            con.execute("CREATE TABLE IF NOT EXISTS BookCondition(BookConditionID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, BookConditionName VARCHAR(255) NOT NULL)")
            con.execute("CREATE TABLE IF NOT EXISTS Book(BookID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Title VARCHAR(255) NOT NULL, Price DOUBLE NOT NULL, BookStatusID INTEGER NOT NULL, Description VARCHAR(255) NOT NULL, GenreID INTEGER NOT NULL, Email VARCHAR(255) NOT NULL, Image VARCHAR(255) NOT NULL, LocationID INTEGER NOT NULL, BookConditionID INTEGER NOT NULL, FOREIGN KEY(BookStatusID) REFERENCES BookStatus(BookStatusID), FOREIGN KEY(Email) REFERENCES User(Email) ON DELETE CASCADE, FOREIGN KEY(GenreID) REFERENCES Genre(GenreID), FOREIGN KEY(LocationID) REFERENCES Location(LocationID), FOREIGN KEY(BookConditionID) REFERENCES BookCondition(BookConditionID))")


            # below tables are book offer related
            con.execute("CREATE TABLE IF NOT EXISTS BookOfferStatus(BookOfferStatusID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,BookOfferStatusName VARCHAR(255) NOT NULL)")
            con.execute("CREATE TABLE IF NOT EXISTS BookOffers(BookOfferID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,BookID INTEGER NOT NULL,OfferPrice DOUBLE NOT NULL,OffererEmail VARCHAR(255) NOT NULL,BookOfferStatusID INTEGER NOT NULL,FOREIGN KEY(BookID) REFERENCES Book(BookID) ON DELETE CASCADE,FOREIGN KEY(BookOfferStatusID) REFERENCES BookOfferStatus(BookOfferStatusID), FOREIGN KEY(OffererEmail) REFERENCES User(Email) ON DELETE CASCADE)")
            

            # below tables are transaction related
            con.execute("CREATE TABLE IF NOT EXISTS Transactions(TransactionID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, BookTitle VARCHAR(255) NOT NULL, Price DOUBLE NOT NULL,Email VARCHAR(255) NOT NULL, PurchaserEmail VARCHAR(255) NOT NULL, FOREIGN KEY(Email) REFERENCES User(Email))")

            print ("Tables created successfully")

            # test data to test db queries 
            
            
            # insert books

            # book binary image data
            #print("Working dir:", os.getcwd())
            #imageblob1 = convertToBinaryData("app\Book1.jpg")
            #imageblob2 = convertToBinaryData("app\Book2.jpg")
            #imageblob3 = convertToBinaryData("app\Book3.jpg")
            
            #NOTE: FOR EXECUTE FIELDS THAT ONLY HAS 1 VALUE, ADD A COMMA (,) AFTER THE SINGLE VALUE TO PREVENT A INCORRECT NUMBER OF BINDINGS ERROR
            # creates cursor for query
            cur = con.cursor()


            # checks if the AccountStatus table is empty, and if empty, insert AccountStatus test data
            cur = cur.execute("SELECT COUNT(*) FROM AccountStatus")
            accountStatusRows = cur.fetchall()

            if accountStatusRows[0][0] == 0:
                con.execute("INSERT INTO AccountStatus (AccountStatusName) VALUES (?)",("Active",) )
                con.execute("INSERT INTO AccountStatus (AccountStatusName) VALUES (?)",("Disabled",) )


            # checks if the Role table is empty, and if empty, insert Role test data
            cur = cur.execute("SELECT COUNT(*) FROM Role")
            roleRows = cur.fetchall()

            if roleRows[0][0] == 0:
                # insert Roles
                con.execute("INSERT INTO Role (RoleName) VALUES (?)",("User",) )
                con.execute("INSERT INTO Role (RoleName) VALUES (?)",("Admin",) )
                con.execute("INSERT INTO Role (RoleName) VALUES (?)",("SuperAdmin",) )


            # checks if the User table is empty, and if empty, insert User test data
            cur = cur.execute("SELECT COUNT(*) FROM User")
            userRows = cur.fetchall()
            
            if userRows[0][0] == 0:
                # insert users
                con.execute("INSERT INTO User (Username, Email, Password, ContactNumber, RoleID, AccountStatusID) VALUES (?,?,?,?,?,?)",("test1","test1@gmail.com", hash_Password("test1"), 98765407, 1, 1) )
                con.execute("INSERT INTO User (Username, Email, Password, ContactNumber, RoleID, AccountStatusID) VALUES (?,?,?,?,?,?)",("test2","test2@gmail.com", hash_Password("test2"), 96543231, 1, 1) )
                con.execute("INSERT INTO User (Username, Email, Password, ContactNumber, RoleID, AccountStatusID) VALUES (?,?,?,?,?,?)",("test3","test3@gmail.com", hash_Password("test3"), 12345678, 1, 1) )
                con.execute("INSERT INTO User (Username, Email, Password, ContactNumber, RoleID, AccountStatusID) VALUES (?,?,?,?,?,?)",("admin","admin@gmail.com", hash_Password("admin"), 00000000, 2, 1) )
                con.execute("INSERT INTO User (Username, Email, Password, ContactNumber, RoleID, AccountStatusID) VALUES (?,?,?,?,?,?)",("superadmin","superadmin@gmail.com", hash_Password("superadmin"), 00000000, 3, 1) )

            # checks if the Genre table is empty, and if empty, insert Genre test data
            cur = cur.execute("SELECT COUNT(*) FROM Genre")
            genreRows = cur.fetchall()
            
            if genreRows[0][0] == 0:
                # insert Genre
                con.execute("INSERT INTO Genre (GenreName) VALUES (?)",("Fiction",) )
                con.execute("INSERT INTO Genre (GenreName) VALUES (?)",("Non-Fiction",) )
                con.execute("INSERT INTO Genre (GenreName) VALUES (?)",("Mystery",) )


            # checks if the BookStatus table is empty, and if empty, insert BookStatus test data
            cur = cur.execute("SELECT COUNT(*) FROM BookStatus")
            bookStatusRows = cur.fetchall()
            
            if bookStatusRows[0][0] == 0:
                # insert BookStatus
                con.execute("INSERT INTO BookStatus (BookStatusName) VALUES (?)",("Available",) )
                con.execute("INSERT INTO BookStatus (BookStatusName) VALUES (?)",("Sold",) )


            # checks if the Location table is empty, and if empty, insert Location test data
            cur = cur.execute("SELECT COUNT(*) FROM Location")
            locationRows = cur.fetchall()
            
            if locationRows[0][0] == 0:
                # insert Locations
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS1 EW24 Jurong East",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS2 Bukit Batok",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS3 Bukit Gombak",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS4 BP1 Choa Chu Kang",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS5 Yew Tee",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS7 Kranji",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS8 Marsiling",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS9 TE2 Woodlands",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS10 Admiralty",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS11 Sembawang",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS12 Canberra",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS13 Yishun",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS14 Khatib",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS15 Yio Chu Kang",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS16 Ang Mo Kio",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS17 CC15 Bishan",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS18 Braddell",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS19 Toa Payoh",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS20 Novena",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS21 DT11 Newton",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS22 Orchard",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS23 Somerset",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS24 NE6 CC1 Dhoby Ghaut",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS25 EW13 City Hall",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS26 EW14 Raffles Place",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS27 CE2 Marina Bay",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("NS28 Marina South Pier",) )

                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW1 Pasir Ris",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW2 DT32 Tampines",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW3 Simei",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW4 CG Tanah Merah",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW5 Bedok",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW6 Kembangan",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW7 Eunos",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW8 CC9 Paya Lebar",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW9 Aljunied",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW10 Kallang",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW11 Lavender",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW12 DT14 Bugis",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW15 Tanjong Pagar",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW16 NE3 Outram Park",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW17 Tiong Bahru",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW18 Redhill",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW19 Queenstown",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW20 Commonwealth",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW21 CC22 Buona Vista",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW22 Dover",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW23 Clementi",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW25 Chinese Garden",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW26 Lakeside",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW27 Boon Lay",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW28 Pioneer",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW29 Joo Koon",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW30 Gul Circle",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW31 Tuas Crescent",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW32 Tuas West Road",) )
                con.execute("INSERT INTO Location (LocationName) VALUES (?)",("EW33 Tuas Link",) )


                
                

            # checks if the book conditon table is empty, and if empty, insert book condition test data
            cur = cur.execute("SELECT COUNT(*) FROM BookCondition")
            bookConditionRows = cur.fetchall()
            
            if bookConditionRows[0][0] == 0:
                # insert Book Conditions
                con.execute("INSERT INTO BookCondition (BookConditionName) VALUES (?)",("New",) )
                con.execute("INSERT INTO BookCondition (BookConditionName) VALUES (?)",("Used",) )

            # checks if the Book table is empty, and if empty, insert Book test data
            cur = cur.execute("SELECT COUNT(*) FROM Book")
            bookRows = cur.fetchall()
            
            if bookRows[0][0] == 0:
                # insert Books
                con.execute("INSERT INTO Book(Title, Price, BookStatusID, Description, GenreID, Email, Image, LocationID, BookConditionID) VALUES (?,?,?,?,?,?,?,?,?)",("God's wisdom for navigating life", 3.50, 1, "A book with proverbs", 1, "test1@gmail.com", "Book1.jpg", 1, 1) )
                con.execute("INSERT INTO Book(Title, Price, BookStatusID, Description, GenreID, Email, Image, LocationID, BookConditionID) VALUES (?,?,?,?,?,?,?,?,?)",("The imperfect disciple", 0.00, 2, "Grace for people who cant get their act together", 2, "test1@gmail.com", "Book2.jpg", 2, 1) )
                con.execute("INSERT INTO Book(Title, Price, BookStatusID, Description, GenreID, Email, Image, LocationID, BookConditionID) VALUES (?,?,?,?,?,?,?,?,?)",("Exodus", 0, 1, "Old testment commentary", 3, "test3@gmail.com", "Book3.jpg", 2, 2) )
                con.execute("INSERT INTO Book(Title, Price, BookStatusID, Description, GenreID, Email, Image, LocationID, BookConditionID) VALUES (?,?,?,?,?,?,?,?,?)",("Destroyer of the gods", 5.00, 1, "Destroying gods", 1, "test2@gmail.com", "Book4.jpg", 3, 2) )
            
            
            # checks if the Book Offer Status table is empty, and if empty, insert Book Offer Status test data
            cur = cur.execute("SELECT COUNT(*) FROM BookOfferStatus")
            bookOfferStatusRows = cur.fetchall()
            if bookOfferStatusRows[0][0] == 0:
                con.execute("INSERT INTO BookOfferStatus (BookOfferStatusName) VALUES (?)", ("Accepted",))
                con.execute("INSERT INTO BookOfferStatus (BookOfferStatusName) VALUES (?)", ("Pending",))
                con.execute("INSERT INTO BookOfferStatus (BookOfferStatusName) VALUES (?)", ("Rejected",))


            # checks if the Book Offer table is empty, and if empty, insert Book Offer test data
            cur = cur.execute("SELECT COUNT(*) FROM BookOffers")
            bookOfferRows = cur.fetchall()
            if bookOfferRows[0][0] == 0:
                con.execute("INSERT INTO BookOffers (BookID,OfferPrice,OffererEmail,BookOfferStatusID) VALUES (?,?,?,?)",(1, 3.00, "test2@gmail.com", 2))
                con.execute("INSERT INTO BookOffers (BookID,OfferPrice,OffererEmail,BookOfferStatusID) VALUES (?,?,?,?)",(2, 0.00, "test2@gmail.com", 1))



            # checks if the Transactions table is empty, and if empty, insert Transactions test data
            cur = cur.execute("SELECT COUNT(*) FROM Transactions")
            transactionsRows = cur.fetchall()
            
            if transactionsRows[0][0] == 0:
                # insert transactions
                con.execute("INSERT INTO Transactions(BookTitle, Price, Email, PurchaserEmail) VALUES (?,?,?,?)",("The imperfect disciple", 0.00, "test1@gmail.com", "test2@gmail.com") )

            con.commit()
            print ("Test Records successfully added")
    except sqlite3.Error:
        con.rollback()
        print ("error in operation")
        print(traceback.print_exc())
    finally:
        con.close()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    sqlite_database_setup()

    app.register_blueprint(user, url_prefix='/apis/user/')
    app.register_blueprint(book, url_prefix='/apis/book/')
    app.register_blueprint(admin, url_prefix='/apis/admin/')
    app.register_blueprint(superadmin, url_prefix='/apis/superadmin/')

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'kopickosongml@gmail.com'
    app.config['MAIL_PASSWORD'] = 'vamjmxizezesorpg'
    app.config['MAIL_USE_SSL'] = True
    app.config['SECRET_KEY'] = 'secretkey'


    UPLOAD_FOLDER = os.path.join('static', 'BookImages')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    jwt.init_app(app)
    mail.init_app(app)
    return app

