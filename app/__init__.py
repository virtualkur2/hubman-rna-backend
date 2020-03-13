from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.utils import create_celery_app

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.debug = True

celery = create_celery_app(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

uploadFolder = app.config['UPLOAD_FOLDER']

from app.api import bp as api_bp

app.register_blueprint(api_bp, url_prefix = '/rna')
