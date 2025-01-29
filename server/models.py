from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates






db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    trips = db.relationship('Trip', back_populates='user', cascade='all, delete-orphan')
    destinations = db.relationship('Destination', back_populates='user', cascade='all, delete-orphan')
    
    serialize_rules = ('-trips', '-destinations')

    @validates('name')
    def validate_name(self, key, name): 
        if not name.strip():
            raise ValueError('Name can not be empty')
        return name
    
    @validates('email')
    def validate_email(self, key, email): 
        if not email.strip():
            raise ValueError('Email can not be empty')
        if '@' not in email:
            raise ValueError('Email is invalid')
        return email
    def __repr__(self):
        return f'<User {self.name} {self.email}>'

class Trip(db.Model, SerializerMixin):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    

    user = db.relationship('User', back_populates='trips')
    trip_destinations = db.relationship('Trip_Destination', back_populates='trip')
    
    serialize_rules = ('-user.trips', '-user.destinations', '-trip_destinations.trip')

    def __repr__(self):
        return f'<Trip {self.name} {self.start_date} {self.end_date}>'
    
class Destination(db.Model, SerializerMixin):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='destinations')
    
    trip_destinations = db.relationship('Trip_Destination', back_populates='destination')

    serialize_rules = ('-user.trips', '-user.destinations', '-trip_destinations.destination')

    def __repr__(self):
        return f'<Destination {self.name} {self.description}>'
    
class Trip_Destination(db.Model, SerializerMixin):
    __tablename__ = 'trip_destinations'

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)

    trip = db.relationship('Trip', back_populates='trip_destinations')
    destination = db.relationship('Destination', back_populates='trip_destinations')

    serialize_rules = ('-trip.trip_destinations', '-destination.trip_destinations')

    def __repr__(self):
        return f'<Trip_Destination {self.id}>'