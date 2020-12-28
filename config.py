import os
class Configuration(object):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/stocks.db' % APPLICATION_DIR
    SECRET_KEY = '2b3b393d409797649c77ae1a01ae7b20'
    #set FLASK_APP = beanstalk.py
    