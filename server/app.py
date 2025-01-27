from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from flask_migrate import Migrate
from flask_restful import Api, Resource
from datetime import date


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

class Home(Resource):
    def get(self):
        return {'Welcome to the travel app!'}

api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run(debug=True)

