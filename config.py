import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'nimble.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'aekl.ijsdfghadfskjghdfklgjadefklgmawer74f54df6asd54f+s5df+85sd'

AUTH_PROVIDERS = [
  {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' }]
