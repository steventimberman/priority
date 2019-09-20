# priority

#### Flask api to be used with an application that stores priorities

### Repo Guide
**__init__.py**
Where the `create_app` function resides.

**run.py**
The runfile for the flask server.

**db.py**
Where to import the mongodb database object (Flask-PyMongo object) from.

**extensions.py**
Where extensions should be imported from. The extensions that live here are:
- Bcrypt
- JWTManager

**user directory**
All routes involed with users, including authentication and registration, are in this directory.

**goals directory**
All routes for accessing goals can be found in this directory.

**High level schema**
A user object stores user info, along with the users goals (in order). These goals however only store the bare minimum amout of data (the goal string, and the rank of the goal). There is a separate goal object that this goal points to that is used to keep track of more information about each goal.

### Docker
To run, enter `docker build -t priority .`
*docker not complete yet, for now, use `flask run`*
