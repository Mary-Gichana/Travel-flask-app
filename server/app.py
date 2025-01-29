from flask import Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Trip, Destination, Trip_Destination
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from datetime import datetime


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

class Home(Resource):
    def get(self):
        return {'message': 'Welcome to the travel app!'}

api.add_resource(Home, '/')

class UserResource(Resource):
    def get(self):
        return make_response([user.to_dict() for user in User.query.all()], 200)
    def post(self):
        data = request.get_json()
        user = User(name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return make_response(user.to_dict(), 201)
    
api.add_resource(UserResource, '/users')

class UserbyIDResource(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user:
            return make_response(user.to_dict(), 200)
        return make_response({'error': 'user not found'}, 404)
    def patch(self, id):
        user = User.query.get(id)
        if user:
            data = request.get_json()
            user.name = data['name']
            user.email = data['email']
            db.session.commit()
            return make_response(user.to_dict(), 200)
        return make_response({'error': 'user not found'}, 404)
    def delete(self, id):
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response({'message': 'user deleted'}, 200)
        return make_response({'error': 'user not found'}, 404)  

api.add_resource(UserbyIDResource, '/users/<int:id>')





class TripResource(Resource):
    def get(self):
        return make_response([trip.to_dict() for trip in Trip.query.all()], 200)
    def post(self):
        data = request.get_json()

        try:
            # Convert string dates to Python date objects
            start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
            end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
        except ValueError:
            return make_response({"error": "Invalid date format. Use YYYY-MM-DD."}, 400)

        # Create a new Trip instance with converted dates
        trip = Trip(
            name=data['name'], 
            start_date=start_date, 
            end_date=end_date, 
            user_id=data['user_id']
        )
        db.session.add(trip)
        db.session.commit()
        return make_response(trip.to_dict(), 201)

api.add_resource(TripResource, '/trips')





class DestinationResource(Resource):
    def get(self):
        return make_response([destination.to_dict() for destination in Destination.query.all()], 200)
    def post(self):
        data = request.get_json()
        destination = Destination(name=data['name'], description=data['description'], user_id=data['user_id'])
        db.session.add(destination)
        db.session.commit()
        return make_response(destination.to_dict(), 201)
api.add_resource(DestinationResource, '/destinations')

class DestinationbyIDResource(Resource):
    def get(self, id):
        destination = Destination.query.get(id)
        if destination:
            return make_response(destination.to_dict(), 200)
        return make_response({'error': 'destination not found'}, 404)
    def patch(self, id):
        destination = Destination.query.get(id)
        if destination:
            data = request.get_json()
            destination.name = data['name']
            destination.description = data['description']
            destination.user_id = data['user_id']
            db.session.commit()
            return make_response(destination.to_dict(), 200)
        return make_response({'error': 'destination not found'}, 404)
    def delete(self, id):
        destination = Destination.query.get(id)
        if destination:
            db.session.delete(destination)
            db.session.commit()
            return make_response({'message': 'destination deleted'}, 200)
        return make_response({'error': 'destination not found'}, 404)
api.add_resource(DestinationbyIDResource, '/destinations/<int:id>')







class TripDestinationResource(Resource):
    def get(self):
        return make_response([trip_destination.to_dict() for trip_destination in Trip_Destination.query.all()], 200)
    def post(self):
        data = request.get_json()
        trip_destination = Trip_Destination(trip_id=data['trip_id'], destination_id=data['destination_id'])
        db.session.add(trip_destination)
        db.session.commit()
        return make_response(trip_destination.to_dict(), 201)
api.add_resource(TripDestinationResource, '/trip_destinations')

class TripDestinationbyIDResource(Resource):
    def get(self, id):
        trip_destination = Trip_Destination.query.get(id)
        if trip_destination:
            return make_response(trip_destination.to_dict(), 200)
        return make_response({'error': 'trip_destination not found'}, 404)
    def delete(self, id):
        trip_destination = Trip_Destination.query.get(id)
        if trip_destination:
            db.session.delete(trip_destination)
            db.session.commit()
            return make_response({'message': 'trip_destination deleted'}, 200)
        return make_response({'error': 'trip_destination not found'}, 404)
api.add_resource(TripDestinationbyIDResource, '/trip_destinations/<int:id>')





if __name__ == '__main__':
    app.run(debug=True)

