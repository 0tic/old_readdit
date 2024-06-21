# Isaac Young
# MCS 275 Project 4
# This project was adapted from createdb.py that was created for OrderNova in MCS 275 Spring 2024
# and I am the sole author of the changes except as noted in README.md.

"Initialize the database"
import sqlite3

#sets the name of the database file
DB_FILE = "readdit.sqlite"

#creates the table posts if it does not exist
create_query = """
CREATE TABLE IF NOT EXISTS posts (
    poid INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    user TEXT NOT NULL,
    created_ts REAL NOT NULL,
    votes REAL,
    subreaddit TEXT NOT NULL
);
"""

#creates teh table comments if it does not exist
create_query_COM = """
CREATE TABLE IF NOT EXISTS comments (
    coid INTEGER PRIMARY KEY,
    poid INTEGER NOT NULL,
    description TEXT NOT NULL,
    user TEXT NOT NULL,
    created_ts REAL NOT NULL
)
"""

# The function below this line is adapted from
# https://github.com/daviddumas/mcs275spring2023/blob/main/samplecode/html/ordernova/createdb.py
# by David Dumas
# The addition of 'c.execute(create_query_COM)' was solely my contribution.
def db_create_tables(c):
    "Make the tables with connection `c`"
    c.execute(create_query) #executes create_query
    c.execute(create_query_COM) #executes create_query_COM

# The function below this line is adapted from
# https://github.com/daviddumas/mcs275spring2023/blob/main/samplecode/html/ordernova/createdb.py
# by David Dumas
# The addition of 'c.execute("DELETE FROM comments;")' was solely my contribution.
def db_clear_tables(c):
    "Remove all work orders with connection `c`"
    c.execute("DELETE FROM posts;") #deletes all rows from posts
    c.execute("DELETE FROM comments;") #deletes all rows from comments

# The function below this line is adapted from
# https://github.com/daviddumas/mcs275spring2023/blob/main/samplecode/html/ordernova/createdb.py
# by David Dumas
# All sample data (for posts and comments) and SQL query modifications were solely my contributions.
def db_add_sample_data(c):
    "Add sample rows to orders table with connection `c`"
    sample_data = [
    ("Just throwing a man away", "Just throwing a man away.", "ddumas", 1680876333.0,0, "Random"), #sample post data 1
    ("So my son just might be a sociopath.", "I have no words to describe my son's key layout.", "iyoun", 1680894498.0,0, "Sociopathy"), #sample post data 2
    ]

    for t in sample_data:
        c.execute( #inserts sample data into database
            "INSERT INTO posts (title, description, user, created_ts, votes, subreaddit) VALUES (?,?,?,?,?,?);",
            t,
        )

    sample_comments = [
        (1,'Why would you throw a man away?','bbumas',1680876333.0), #sample comment data 1
        (2,'What is wrong with son/s key layout?','jjoyce',1680876333.0), #sample comment data 2
    ]

    for t in sample_comments:
        c.execute( #inserts sample data into database
            "INSERT INTO comments (poid, description,user,created_ts) VALUES (?,?,?,?);",
            t
        )
        

# The code to be run if the program is run as a script is adapted from
# https://github.com/daviddumas/mcs275spring2023/blob/main/samplecode/html/ordernova/createdb.py
# by David Dumas
# All below code is written solely by David Dumas.
if __name__ == "__main__":
    #if python file is run as a script, creates the tables if not already there
    #gets rid of all the rows
    #adds sample data
    con = sqlite3.connect(DB_FILE)

    db_create_tables(con)
    db_clear_tables(con)
    db_add_sample_data(con)

    con.commit()  # write queries are discarded unless you do this
    con.close()