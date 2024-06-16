import os
import app
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/copodb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)