from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_name = db.Column(db.String(50), nullable=False)
    car_model = db.Column(db.String(50), nullable=False)
    manufacture_year = db.Column(db.Integer, nullable=False)
    vin = db.Column(db.String(17), nullable=False, unique=True)
    license_plate = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Vehicle('{self.car_name}', '{self.car_model}', '{self.vin}')"