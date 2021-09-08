from django.conf import settings


def delete_session_settings(keys):
    """
    to delete session key in dict
    """
    try:
        settings.CT_USER_SESS.pop(keys)
    except Exception as e:
        pass
