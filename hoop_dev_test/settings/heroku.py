"""
Extends the base settings to use the postgres DB provided by heroku
"""
# noinspection PyUnresolvedReferences
from base import *


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
import dj_database_url
DATABASES = {
    'default': dj_database_url.config()
}