from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from app import app
from flask_migrate import Migrate
migrate = Migrate(app,db)