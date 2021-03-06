from .base import *  # noqa

CELERY_ALWAYS_EAGER = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_EAGER_TRANSACTION = True
BROKER_BACKEND = 'memory'

developfilesdir = 'devilry_testfiles'
if not exists(developfilesdir):
    os.mkdir(developfilesdir)
logdir = join(developfilesdir, 'log')
if not exists(logdir):
    os.mkdir(logdir)
MEDIA_ROOT = join(developfilesdir, "filestore")
DEVILRY_FSHIERDELIVERYSTORE_ROOT = join(developfilesdir, 'deliverystorehier')


if 'devilry.utils.logexceptionsmiddleware.TracebackLoggingMiddleware' in MIDDLEWARE_CLASSES:
    MIDDLEWARE_CLASSES.remove('devilry.utils.logexceptionsmiddleware.TracebackLoggingMiddleware')

# Use database for search in tests
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# We need to use this because loads of tests uses username and password to login
DJANGO_CRADMIN_USE_EMAIL_AUTH_BACKEND = False
AUTHENTICATION_BACKENDS = (
    'devilry.devilry_account.authbackend.default.UsernameAuthBackend',
    'devilry.devilry_account.authbackend.default.EmailAuthBackend',
)

# Ensures we are testing against the default translation strings.
DEVILRY_JAVASCRIPT_LOCALE_OVERRIDE_APPS = []

# Default to skipping selenium tests
SKIP_SELENIUMTESTS = True
# SELENIUM_BROWSER = 'phantomjs'
# SELENIUM_DEFAULT_TIMEOUT = 20


# Disable migrations except custom test-only migrations when running tests
class DisableMigrations(object):
    apps_with_test_migrations = {
        # 'devilry_account': 'devilry.devilry_account.testmigrations',
    }

    def __contains__(self, key):
        return True

    def __getitem__(self, key):
        return self.apps_with_test_migrations.get(key, 'notmigrations')

MIGRATION_MODULES = DisableMigrations()


DEVILRY_ELASTICSEARCH_HOSTS = [
    {"host": "localhost", "port": 9492}
]
