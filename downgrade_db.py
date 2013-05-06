from migrate.versioning import api
import config

version = api.db_version(config.SQLALCHEMY_DATABASE_URI, 
                         config.SQLALCHEMY_MIGRATE_REPO)

api.downgrade(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO,
              version - 1)

print 'Current database version: ' + str(api.db_version(config.SQLALCHEMY_DATABASE_URI,
                                         config.SQLALCHEMY_MIGRATE_REPO))
