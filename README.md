# readdit

MCS 275 Spring 2023 Project 4 by Isaac Young

## Description

To create something similar to old reddit was the goal of my project.
A website where you could create subreaddits, create posts, upvote and downvote posts,
and create comments on other posts. The website is a form of online interaction
with other users who all have access to the internet. For users to create their
own communities and gather people who have the same interests.


## How to test

There should be no set-up needed. You should only need to run old_readdit.py
and the database should automatically create and create some sample code within
the database.
If you click the word 'readdit' on any page, it should lead you back to the home page.
If you click any subreaddits, it should list posts of that particular subreaddit.
If you click the title of any post, it should lead you to that posts description, where you can see
comments other users have made and the ability to create your own comments.
If you click 'Submit a new text post', you should be able to create your own post, inputting
a title, subreaddit, username, and the description of the post.
For any post, you should see up-arrows and down-arrows which allow you to upvote and downvote particular
posts. (all posts should be listed by order of amount of upvotes)

## Personal contribution

All html files (new_post.html, old_readdit.html, post.html) were my personal contribution. 

The the css file was heavily inspired by OrderNova css file (css file from class). However all
modifications were my personal contribution. The parts that were taken from ordernova.css is stated in source code.
All parts that were not cited in source code were my personal contribution.

All of old_readdit.py was my personal contribution except for the section at the very end
that worked with createdb.py. That last section is cited in the source code.

For createdb.py, I made slight modifications from the createdb.py that was for OrderNova. The modifications include the creation a new table called comments and put sample data in that table. In addition, changing
the column titles and table name that was originally apart of createdb.py. All modifications made to createdb.py were my personal contribution.

## Sources and credits

Johnny Joyce reviewed portions of my code when I was having trouble connecting the creation of comments to a particular
post. He helped me figure out how to transfer a variable (poid) to the location where it could be inserted into the database for comments.

The file createdb.py was taken when David Dumas wrote the file for OrderNova. The base code is the same, however, I made
modifications so that it would work with my database. Some modifications include database name, multiple tables within database, different columns, and different sample data.
The createdb.py file that was written by David Dumas for MCS 275 Spring 2024 can be found at:
https://github.com/daviddumas/mcs275spring2023/blob/main/samplecode/html/ordernova/createdb.py

The file old_readdit.css has sections of code taken from ordernova.css written by David Dumas for MCS 275 Spring 2023.
Similar to createdb.py, it has similar base code, however, I made modiciations so that the style of the website
was to my liking. My modifications were highly inspired by ordernova.css so they may seem similar to previous base
code.
The ordernova.css file that was written by David Dumas for MCS 275 Spring 2024 can be found at:
https://github.com/daviddumas/mcs275spring2023/blob/main/samplecode/html/ordernova/static/ordernova.css

At the end of old_readdit.py, it contains code that works with createdb.py, that code was written solely by David Dumas, and 
no modifications were made by me.
The base code can be found on lines 251-269 from ordernova.py which can be found at:
https://github.com/daviddumas/mcs275spring2023/blob/main/samplecode/html/ordernova/ordernova.py
(The line numbers were taken from 4/28/23, any further edits to ordernova.py since then could
affect the line numbers specififed.)