import os

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'MYSECRETKEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

