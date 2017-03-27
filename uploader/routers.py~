class uploaderRouter(object):
    """
    A router to control all database operations on models in
    the uploader application
    """
 
    def db_for_read(self, model, **hints):
        """
        Point all operations on uploader models to 'userstats'
        """
        if model._meta.app_label == 'uploader':
            return 'default'
        return None
 
    def db_for_write(self, model, **hints):
        """
        Point all operations on uploader models to 'other'
        """
        if model._meta.app_label == 'uploader':
            return 'default'
        return None
 
    def allow_syncdb(self, db, model):
        """
        Make sure the 'uploader' app only appears on the 'other' db
        """
        if db == 'default':
            return model._meta.app_label == 'uploader'
        elif model._meta.app_label == 'uploader':
            return False
        return None
