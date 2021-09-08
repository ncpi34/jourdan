import os
import uuid
from django.utils.deconstruct import deconstructible
from django.utils import timezone


@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        # @note It's up to the validators to check if it's the correct file type in name or if one even exist.
        now = timezone.now()
        milliseconds = now.microsecond // 1000
        unq_str = f"{now:%Y%m%d%H%M%S}{milliseconds}"
        extension = os.path.splitext(filename)[1]
        return self.path % (unq_str, extension)
        # return self.path % (uuid.uuid4(), extension)
