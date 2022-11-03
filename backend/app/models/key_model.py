import sqlite3

class key:

    def __init__(self):
            self.dbname = "database"
            self.tablename = "Keys"

    def get_key(self, keyName):
        try:
            
            with sqlite3.connect(self.dbname + ".db") as con:
                print("Opened database successfully")

                # this command forces sqlite to enforce the foreign key rules set  for the tables
                con.execute("PRAGMA foreign_keys = 1")

                cur = con.cursor()
                cur.execute("SELECT key FROM {} WHERE KeyName = ?".format(self.tablename),(keyName,))
                keyRow = cur.fetchall()

                # each keyname should only have 1 key
                if len(keyRow) == 1:
                    return keyRow[0][0]
                else:
                    return None
        except sqlite3.Error as er:
            con.rollback()
            return ("Error in getting key")

        finally:
            con.close()
            print("Successfully closed connection")