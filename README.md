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

### Docker
To run, enter `docker build -t priority .`
