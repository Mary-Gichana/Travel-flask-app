from flask import Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Trip, Destination, Trip_Destination
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

class User(Resource):
    def get(self):
        return make_response([user.to_dict() for user in User.query.all()], 200)
    def post(self):
        data = request.get_json()
        user = User(name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return make_response(user.to_dict(), 201)



if __name__ == '__main__':
    app.run(debug=True)

