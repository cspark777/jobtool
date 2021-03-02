from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def create_app():
	"""Construct the core application."""
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'your secret key'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'

	db.init_app(app)
	with app.app_context():
		#from . import routes  # Import routes
		db.create_all()  # Create sql tables for our data models
		return app
	
