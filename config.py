import os
import datetime

class Config(object):
    JWT_SECRET_KEY = os.urandom(24) # os.environ.get('SECRET')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRESS = datetime.timedelta(days=1)

    MONGO_DBNAME = 'priority'
    MONGO_URI = 'mongodb://localhost:27017/priority'
