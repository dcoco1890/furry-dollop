from tempfile import mkdtemp

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
FLASK_APP = 'wsgi.py'
TEMPLATES_AUTO_RELOAD = True
SESSION_FILE_DIR = mkdtemp()
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"
SQLALCHEMY_DATABASE_URI = 'sqlite:///final.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
