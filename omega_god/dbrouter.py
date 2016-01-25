class OmegaRouter(object):
    """
    A router to control all database operations on models in the
    omega application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read omega models go to omega.
        """
        if model._meta.app_label == 'omega':
            return 'omega'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write omega models go to omega.
        """
        if model._meta.app_label == 'omega':
            return 'omega'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the omega app is involved.
        """
        if obj1._meta.app_label == 'omega' or \
           obj2._meta.app_label == 'omega':
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the omega app only appears in the 'omega'
        database.
        """
        if app_label == 'omega':
            return db == 'omega'
        return None

class OappRouter(object):
    """
    A router to control all database operations on models in the
    oapp application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read oapp models go to oapp.
        """
        if model._meta.app_label == 'oapp':
            return 'oapp'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write oapp models go to oapp.
        """
        if model._meta.app_label == 'oapp':
            return 'oapp'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the oapp app is involved.
        """
        if obj1._meta.app_label == 'oapp' or \
           obj2._meta.app_label == 'oapp':
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the omega app only appears in the 'oapp'
        database.
        """
        if app_label == 'oapp':
            return db == 'oapp'
        return None
