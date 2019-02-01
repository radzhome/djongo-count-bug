"""
Decides which app uses wcm db vs the default

Needed since auth is broken when using djongo for auth

On fresh install with mongo 3.6.9 you get

ValueError at /admin/login/
Cannot force an update in save() with no primary key.
Request Method:	POST

"""
MONGO_APPS = ('content_app', )


class MyDatabaseRouter:
    """
    A router to control all database operations on models in the
    wcm application.
    """
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label in MONGO_APPS:
            return 'mongo'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in MONGO_APPS:
            return 'mongo'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in MONGO_APPS or \
           obj2._meta.app_label in MONGO_APPS:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in MONGO_APPS:
            return db == 'mongo'
        return None
