from os import environ, path

from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api

BASE_DIR = path.abspath(path.dirname(__file__))
DATABASE = environ.get(
    "DB_URI", f"sqlite:///{path.join(BASE_DIR, 'app.db')}")

load_dotenv('.env')

app = Flask(__name__)

app.secret_key = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

migrate = Migrate(app, db)

db.init_app(app)
bcrypt = Bcrypt(app)
api = Api(app)
