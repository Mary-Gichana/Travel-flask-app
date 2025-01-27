from app import db

class User(db.model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name} {self.email}>'
