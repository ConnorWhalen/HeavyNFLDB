import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'heavy-nfld.db')
    
app = Flask("server")
app.config.from_object(Config)
db = SQLAlchemy(app)

from server import api
