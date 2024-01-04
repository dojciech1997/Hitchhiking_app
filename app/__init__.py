from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from app import app


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@db:5432/devops_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devops.db'
from app.db_file import db
db.init_app(app)

from app import models, views

