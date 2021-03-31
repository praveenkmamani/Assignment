import sqlite3


def createDBconnection():
    """
    Function :       Creates database connection with emails.db
    Arguments :     No arguments provided
    Return Values : returns the cursor of the database
    """
    try:
        con = sqlite3.connect('emails.db')
        cur = con.cursor()
        return con, cur
    except Exception as e:
        print(e)
        return None

def createTable(cur):
    """
    Function :      Creates the table GMAIL by running a sql query
    Arguments :     cur - the cursor of the connected database.
    Return Values : No return value
    """
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS GMAIL
                       (
                       DATE DATETIME NOT NULL,
                       SUBJECT TEXT NOT NULL,
                       SENDER TEXT NOT NULL,
                       MSGID TEXT NOT NULL)''')
    except Exception as e:
        print(e)


def insertRow(con, cur, dat, sub, sen, mid):
    """
    Function :      Inserts rows to the database GMAIL
    Arguments :     con - database connection string
                    cur - the cursor of the connected database.
                    dat - date value
                    sub - subject value
                    sen - senders email address
                    mid - message id
    Return Values : No return values.
    """
    try:
        sql = ''' INSERT INTO GMAIL ('DATE','SUBJECT','SENDER','MSGID')
                      VALUES(?,?,?,?) '''
        sqlValue = (dat, sub, sen, mid)
        cur.execute(sql, sqlValue)
        con.commit()
    except Exception as e:
        print(e)


def readTable(cur):
    """
    Function :      Reads the table GMAIL and its rows
    Arguments :     cur - the cursor of the connected database.
    Return Values : No return value
    """
    try:
        cur.execute("SELECT * FROM GMAIL")
        allEmails = cur.fetchall()
        return allEmails
        # for email in allEmails:
        #     print(email)
    except Exception as e:
        print(e)

