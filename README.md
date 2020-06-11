# {Furry Dollop}

At some point this will be a python web application (Flask) with a SQL database (sqlite3). I am using the flask-sqlalchemy ORM so I don't have to write SQL statements. I *think* what I'm going to do is make a place for users to upload and edit photos using the PIL library. Currently debating storing pictures in the database as blobs, storing them in the filesystem, or using something external like an s3 bucket. 

Here's the first few things I'm gonna do, in no particular order:
## Done
- [x] Set up the virtual env
- [x] Get the app to listen for requests on "/"
- [x] Build a home page
- [x] Create a DB with a Users table
- [x] Build a login form with validation
- [x] Build a registration form with validation
- [x] Allow log in and save id in flask-session

## Not done, want to do
- [ ] Allow file uploads
- [ ] Allow users to make changes to images they have uploaded

## Not done, not sure if want to do
- [ ] Switch to Flask login? 
- [ ] Use blueprints to separate auth and normal routes?
