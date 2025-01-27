from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from flask_migrate import Migrate

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

