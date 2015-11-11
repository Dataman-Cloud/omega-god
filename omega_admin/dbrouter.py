class OmegaRouter(object):
    """
    A router to control all database operations on models in the
    omega application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read omega models go to omega_db.
        """
        if model._meta.app_label == 'info':
            return 'omega'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write omega models go to omega_db.
        """
        if model._meta.app_label == 'info':
            return 'omega'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the omega app is involved.
        """
        if obj1._meta.app_label == 'info' or \
           obj2._meta.app_label == 'info':
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the omega app only appears in the 'omega_db'
        database.
        """
        if app_label == 'info':
            return db == 'omega'
        return None

