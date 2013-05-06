from migrate import api
import config

api.upgrade(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)

print 'Current database version: ' + str(api.db_version(config.SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))
