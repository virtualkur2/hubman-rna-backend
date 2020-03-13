import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  # ...
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app/data/idsapp.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'B9F029FF7D4F3EEEDCECD4756DBA529772A7B0EEFBD8CCD5CF7A9E144C9C3ED6'
  BROKER_URL = os.environ.get('BROKER_URL') or 'redis://localhost:6379/0'
  RESULT_BACKEND = os.environ.get('RESULT_BACKEND') or 'redis://localhost:6379/0'
  UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(basedir,'app/uploads')