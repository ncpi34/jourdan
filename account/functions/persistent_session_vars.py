from django.utils.six import wraps
from django.conf import settings


class PersistSessionVars(object):
    """
    Some views, such as login and logout, will reset all session state.
    (via a call to ``request.session.cycle_key()`` or ``session.flush()``).
    That is a security measure to mitigate session fixation vulnerabilities.

    By applying this decorator, some values are retained.
    Be very aware what kind of variables you want to persist.
    """

    def __init__(self, var):
        self.vars = var

    def __call__(self, view_func):

        @wraps(view_func)
        def inner(request, *args, **kwargs):
            # if a not a product
            if settings.PRODUCT_DOES_NOT_EXISTS_ANYMORE:
                del request.session

            # Backup first
            session_backup = {}
            for var in self.vars:
                try:
                    session_backup[var] = request.session[var]
                except KeyError:
                    print('keyerror')
                    pass

            # Call the original view
            response = view_func(request, *args, **kwargs)

            # Restore variables in the new session
            for var, value in session_backup.items():
                request.session[var] = value

            return response

        return inner
