# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from pytz import timezone

# Initializes Flask
app = Flask(__name__)

# # initialize database
db = SQLAlchemy(app)

# # Intialize Marshmallow
ma = Marshmallow(app)

# Load config
app.config.from_pyfile('../config.cfg')


##############
### LOGGER ###
##############
def make_logger():
    from logging.config import dictConfig
    import logging
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'verbose': {
                'format': '[%(asctime)s] %(levelname)s [module - %(module)s process - %(process)d  thread - %('
                          'thread)d [ '
                          '%(name)s: %(funcName)s: %(pathname)s: %(lineno)s] %(message)s '
            }
        },

        'handlers': {
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'verbose',
                'filename': 'ccv_error.log',
                'mode': 'a',
                'maxBytes': 50 * 1024 * 1024,
                'backupCount': 10,
            }
        },

        'loggers': {
            'extensive': {
                'level': 'DEBUG',
                'handlers': ['file', ]
            },
        }
    })

    return logging.getLogger('extensive')

# Initialize logger
logging = make_logger()


import ccv.views