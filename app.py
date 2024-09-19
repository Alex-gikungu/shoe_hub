# app.py
from flask import Flask
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def initialize_database():
    db.create_all()  # Create the tables in the database

if __name__ == '__main__':
    app.run(debug=True)