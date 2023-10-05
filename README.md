# ChatroomFlask

I accidentally deleted main content of this project, so I am going to write it again.

Commit 7: I made initialization, made project structure, some templates, forms for verification and registration and for now I am going to add login.

Commit 8: I updated code of registration and login page.

Commit 9: I determined models for database, but database is in .gitignore file (database is not committed) due to data privacy.

Commit 10: I added number input in register, because I forgot to add an age field.

Commit 11: I Improved register route and integrated it to database.

Commit 12: I improved login system, added logging in and logging out.

Commit 13: I added login requirements for some pages, because on some pages you need access.

Commit 14: I added account updates, integrated code on image files by adding profile_pics directly and default.jpg, added another form for updates. also connected base.html to styles.css.

 Commit 15: I started working on rooms, initialized SocketIO, and made room route
 
Commit 16: fixed bugs with joining room, and learning Flask-SocketIO in order to be able to make an application

Commit 17-18: Came back to my code after break (I've been learning front-end, and still learning). I updated Flask libraries and my IDE this made me problems by flask-login wasn't working at all (it had issue with LoginManager). So I decided to fix this problem by replacing all flask_login code by Flask.g global. My code is refactored and after 3-4 hours of work I still have some bugs to fix for next commit. P.S. Also I deleted all of Socket-IO code because I have to refactor it as well :).

Commit 19: Fixed all problems. Also added validation for rooms URL when someone tries to access the room that does not exist in database.
