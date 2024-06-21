# Isaac Young
# MCS 275 Project 4
# I am the sole author of this project, except where contributions of others
# are noted in README.md.

import flask
import sqlite3
import os
import createdb
import time
from createdb import DB_FILE

app = flask.Flask("readdit")

@app.route("/")
def show_front():
    '''
    Shows the front page of the website.
    '''
    con = sqlite3.connect(DB_FILE) #connects to database
    res = con.execute(
        '''
        SELECT poid, title, description, user, created_ts, votes, subreaddit
        FROM posts
        ORDER BY votes DESC;
        '''
    )
    posts_data = []
    subreaddit_data = []
    for row in res: # for each row in the result, takes information and assigns each column to a key in a dictionary
        res_COM = con.execute(
        '''
        SELECT COUNT(*) FROM comments where poid =?;
        ''',
        (row[0],),
    )
        d = { #creates dictionary for each row that has each column assigned to a key
            'poid': row[0],
            'title': row[1],
            'description': row[2],
            'user': row[3],
            'created_ts': row[4],
            'votes': int(row[5]),
            'comments': res_COM.fetchone()[0]
        }
        subreaddit_data.append(row[6]) #adds what subreaddit each post is under
        posts_data.append(d) #adds each dictionary/row to a list that contains all posts
    con.close()
    return flask.render_template(
        'old_readdit.html', #home page html
        posts_data = posts_data,
        subreaddit_data = set(subreaddit_data) #converts list to a set so that it doesn't relist any subreaddits
    )

@app.route("/r/<subreaddit>/")
def show_subreaddit(subreaddit):
    '''
    Shows a subreaddit, lists all posts that are associated
    with the selected subreaddit.
    '''
    con = sqlite3.connect(DB_FILE) #connects to the databse
    res = con.execute( #gets data about all posts that are under specified subreaddit
        """
        SELECT poid, title, description, user, created_ts, votes, subreaddit
        FROM posts
        WHERE subreaddit = ?
        ORDER BY votes DESC;
        """,
        (subreaddit,),
    )
    res_subreaddit = con.execute( #gets data about all subreaddits by descreasing order by votes
        """
        SELECT subreaddit
        FROM posts
        ORDER BY votes DESC;
        """
    )
    posts_data = []
    subreaddit_data = []
    for row in res: # for each row in the result, takes information and assigns each column to a key in a dictionary
        res_COM = con.execute(
        '''
        SELECT COUNT(*) FROM comments where poid =?;
        ''',
        (row[0],),
    )
        d = {
            'poid': row[0],
            'title': row[1],
            'description': row[2],
            'user': row[3],
            'created_ts': row[4],
            'votes': int(row[5]),
            'comments': res_COM.fetchone()[0]
        }
        posts_data.append(d)
    for row in res_subreaddit:
        subreaddit_data.append(row[0]) #adds subreaddit data to the lsit subreaddit_data
    con.close()
    return flask.render_template(
        'old_readdit.html',
        posts_data = posts_data,
        subreaddit_data = set(subreaddit_data) #converts list to a set so that it doesn't relist any subreaddits
    )

@app.route('/newpost/')
def new_post():
    '''
    Directs user to new html that allows them to create 
    a new post.
    '''
    return flask.render_template( 
        'new_post.html', #directs user to a new html that allows them to enter information for a new post
    )

@app.route('/newpost/submit', methods=['POST','GET'])
def create_new_post():
    '''
    When a user creates a new post, it takes the information
    and inserts all of the information into the database.
    '''
    title = flask.request.values.get("title") # gets 'title' information from new_post.html and assigns to variable
    description = flask.request.values.get("description") # gets 'description' information from new_post.html and assigns to variable
    user = flask.request.values.get("user") # gets 'uesr' information from new_post.html and assigns to variable
    subreaddit = flask.request.values.get("subreaddit") # gets 'subreaddit' information from new_post.html and assigns to variable
    con = sqlite3.connect(DB_FILE)
    res = con.execute( #inserts all the post details into the posts table in the database
        """
        INSERT INTO posts (title,description,user,created_ts,votes,subreaddit)
        VALUES (?,?,?,?,?,?);
        """,
        (title,description,user,time.time(),0,subreaddit),
    )
    res = con.execute("SELECT last_insert_rowid();")
    poid = res.fetchone()[0]
    con.commit() #commits database
    con.close() #closes database
    return flask.redirect("/post/{}/".format(poid)) #redirects to that post that shows comments and the ability to create comments

@app.route('/newcomment/<int:poid>/submit', methods = ['POST','GET'])
def create_new_comment(poid):
    '''
    When a user creates a new comment, it takes the information
    and inserts all of the information into the database.
    '''
    description = flask.request.values.get('description') # gets 'description' information from new_post.html and assigns to variable
    user = flask.request.values.get('user') # gets 'user' information from new_post.html and assigns to variable
    con = sqlite3.connect(DB_FILE) #connects to database
    res = con.execute( #inserts all the comment details into the comments table in the database
        '''
        INSERT INTO comments (poid,description,user,created_ts)
        VALUES (?,?,?,?);
        ''',
        (poid,description,user,time.time())
    )
    con.commit() #commits database
    con.close() #closes database
    return flask.redirect('/post/{}/'.format(poid)) #redirects to that post that shows comments and the ability to create comments
    

@app.route('/post/<int:poid>/')
def post(poid):
    '''
    Directs user to a webpage that displays a specfic post
    and all of the comments associated with that post.
    '''
    con = sqlite3.connect(DB_FILE) #connects to database
    res = con.execute( #gets information about post from designated poid
        '''
        SELECT title,description,user,created_ts FROM posts WHERE poid = ?;
        ''',
        (poid,),
    )
    title,description,user,created_ts = res.fetchone() #assigns information to variables

    res_com = con.execute( #gets information about comments from designated poid
        """
        SELECT description,user,created_ts FROM comments WHERE poid = ?;
        """,
        (poid,),
    )
    comments_data = []
    for row in res_com: # for each row in the result, takes information and assigns each column to a key in a dictionary
        d = {
            'description': row[0],
            'user': row[1],
            'created_ts': row[2],
        }
        comments_data.append(d)

    con.close()

    return flask.render_template( #goes to post.html page and transfers information from variables
        "post.html",
        title = title,
        description = description,
        user = user,
        created_ts = created_ts,
        comments_data = comments_data,
        poid = poid
    )

@app.route('/post/<int:poid>/upvote/')
def upvote(poid):
    '''
    When the user clicks the uparrow, this function executes.
    Updates the votes in the database by adding one everytime it is 
    clicked.
    '''
    con = sqlite3.connect(DB_FILE) #connects to database
    res = con.execute( #gets number of votes on specific post via poid
        '''
        SELECT votes
        FROM posts
        WHERE poid = ?;
        ''',
        (poid,),
    )
    votes = res.fetchone()[0]
    votes += 1 #adds one to votes
    res = con.execute( #updates number of votes to the database
        '''
        UPDATE posts
        SET votes = ?
        WHERE poid = ?;
        ''',
        (votes,poid),
    )
    con.commit() #commits the connection
    con.close() #closes the connection
    return flask.redirect('/') #redirects to homepage

@app.route('/post/<int:poid>/downvote/')
def downvote(poid):
    '''
    When the user clicks the downarrow, this function executes.
    Updates the votes in the database by subtracting one everytime 
    the arrow is clicked.
    '''
    con = sqlite3.connect(DB_FILE) #connects to database
    res = con.execute( #gets number of votes on specific post via poid
        '''
        SELECT votes
        FROM posts
        WHERE poid = ?;
        ''',
        (poid,),
    )
    votes = res.fetchone()[0]
    votes -= 1 #subtracts one to votes
    res = con.execute( #updates number of votes to the database
        '''
        UPDATE posts
        SET votes = ?
        WHERE poid = ?;
        ''',
        (votes,poid,),
    )
    con.commit() #commits the connection
    con.close() #closes the connection
    return flask.redirect("/") #redirects to the homepage


# The code below this line is adapted from
# https://github.com/daviddumas/mcs275spring2023/blob/main/samplecode/html/ordernova/ordernova.py
# by David Dumas
add_sample_data = False
if not os.path.exists(DB_FILE): #if the database is not found in the directory, makes sample data
    print("The database '{}' was not found.  Creating it.".format(DB_FILE))
    add_sample_data = True

con = sqlite3.connect(DB_FILE) #connects to database

print("Making sure the DB contains the necessary tables...", end="")
createdb.db_create_tables(con) #creates necessary tables for code to work
print("Done")

if add_sample_data:
    print("Populating DB with sample data, since it was empty...", end="")
    createdb.db_add_sample_data(con) #adds sample data since the database was empty
    print("Done")

con.commit() #commits changes
con.close() #closes the connection

app.run() #runs the app