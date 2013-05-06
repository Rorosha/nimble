import imp
from migrate.versioning import api
from app import db
import config

migration = config.SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_migration.py' % (api.db_version(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO) + 1)

temp_module = imp.new_module('old_module')
old_model = api.create_model(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)
exec old_model in temp_module.__dict__

script = api.make_update_script_for_model(config.SQLALCHEMY_DATABASE_URI,
                                          config.SQLALCHEMY_MIGRATE_REPO,
                                          temp_module.meta,
                                          db.metadata)

open(migration, 'wt').write(script)

a = api.upgrade(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)

print 'New migration script saved as ' + migration
print 'Current database version: ' + str(api.db_version(config.SQLALCHEMY_DATABASE_URI,
                                                        config.SQLALCHEMY_MIGRATE_REPO))
