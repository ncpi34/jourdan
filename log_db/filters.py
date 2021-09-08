from crum import get_current_user
import logging
from django.conf import settings


class ContextFilter(logging.Filter):
    """
    This is a filter injects the Django user
    """

    def filter(self, record):
        record.user = get_current_user()
        record.app = getattr(settings, 'CURRENT_SITE', None)
        return True
