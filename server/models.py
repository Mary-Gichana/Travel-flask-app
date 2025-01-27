from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    trips = db.relationship('Trip', back_populates='user', cascade='all, delete-orphan')
    destinations = db.relationship('Destination', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.name} {self.email}>'

class Trip(db.model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='trips')

    def __repr__(self):
        return f'<Trip {self.name} {self.start_date} {self.end_date}>'
    
class Destination(db.model):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='destinations')

    def __repr__(self):
        return f'<Destination {self.name} {self.description}>'
    
class Trip_Destination(db.model):
    __tablename__ = 'trip_destinations'

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)



    def __repr__(self):
        return f'<Trip_Destination {self.id}>'