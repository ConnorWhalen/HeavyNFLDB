import os
import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, has_request_context, request
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'heavy-nfld.db')
    LOG_DIRECTORY = '/usr/local/var/log/HeavyNFLDB/'

class ServerConfig(Config):
    LOG_DIRECTORY = '/var/log/HeavyNFLDB/'

    
app = Flask("server")
app.config.from_object(Config)
db = SQLAlchemy(app)

file_log_handler = TimedRotatingFileHandler(
    app.config["LOG_DIRECTORY"] + "webserver.log",
    when='D',
    backupCount=30
)
file_log_handler.setLevel(logging.INFO)

class RequestFormatter(Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)

formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
default_handler.setFormatter(formatter)
file_log_handler.setFormatter(formatter)

app.logger.addHandler(file_log_handler)

from server import api
