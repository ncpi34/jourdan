import os
from app.settings import BASE_DIR

"""
Static files (CSS, JavaScript, Images)
"""
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'  # path admin statics
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # path to save (public)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = (
    # os.path.join(BASE_DIR + 'static_root'),  # path  not admin statics
    os.path.join(BASE_DIR + '/website/staticfiles'),  # path  not admin statics
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
# STATICFILES_FINDERS = [
#     "django.contrib.staticfiles.finders.FileSystemFinder",
#     "django.contrib.staticfiles.finders.AppDirectoriesFinder",
#     "compressor.finders.CompressorFinder"
# ]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# COMPRESS_ENABLED = True
# COMPRESS_OFFLINE = True
# COMPRESS_YUGLIFY_BINARY = "yuglify"
# # COMPRESS_YUGLIFY_JS_ARGUMENTS = "--mangle"
#
# COMPRESS_CSS_FILTERS = [
#     'compressor.filters.css_default.CssAbsoluteFilter',
#     'compressor.filters.yuglify.YUglifyCSSFilter'
# ]
# COMPRESS_JS_FILTERS = [
#     'compressor.filters.jsmin.JSMinFilter',
#     'compressor.filters.yuglify.YUglifyJSFilter',
# ]