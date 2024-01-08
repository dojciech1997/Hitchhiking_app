from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wojtek:password@database:5432/devops_db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devops.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['TESTING'] = True

db = SQLAlchemy(app)

migrate = Migrate(app,db)

#from app.db_file import db
#db.init_app(app)

# from app import models, views

from app.models import Person, Tag
from app.views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)