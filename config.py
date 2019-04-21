import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-redicules-did-i-spell-that-shit-right'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'development.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WHOOSH_BASE = os.path.join(basedir, 'search.db')
    MAX_SEARCH_RESULTS = 50

    # For recaptcha verification api keys
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = '6LeGm5MUAAAAANEb9x2q5C1iwGp8mLgfy6xHRoB6'
    RECAPTCHA_PRIVATE_KEY = '6LeGm5MUAAAAAC74Uo4F-LGf90AZfzDjiXDmFhJw'
    RECAPTCHA_OPTIONS = {'theme':'black'}

    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_FILE_UPLOADER = 'upload'
    CKEDITOR_ENABLE_CSRF = True
    UPLOADED_PATH = os.path.join(basedir, 'uploads')
