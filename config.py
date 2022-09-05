import os


class Config(object):

    DATABASE = 'sqlite:///app.db'

    DEBUG = True

    BASE_DIR = os.getcwd()

    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'media')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    CSRF_ENABLED = True

    SECRET_KEY = os.urandom(15)

    SQLALCHEMY_DATABASE_URI = DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
