from tempfile import mkdtemp

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
TEMPLATES_AUTO_RELOAD = True
SESSION_FILE_DIR = mkdtemp()
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"
