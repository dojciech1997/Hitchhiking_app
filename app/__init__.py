from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.run(port=5000)
app.run(port=5001)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wojtek:password@db:5432/devops_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devops.db'
app.config['DEBUG'] = True
app.config['TESTING'] = True
from app.db_file import db

db.init_app(app)

from app import models, views

