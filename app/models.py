from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

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
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year_of_manufacture = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(50), nullable=False)
    transmission_type = db.Column(db.String(50), nullable=False)
    fuel_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Vehicle('{self.brand}', '{self.model}', '{self.year_of_manufacture}')"

class Inspection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    # Dashboard Condition
    dashboard_defects = db.Column(db.String(10), nullable=False)  # a) Perfect b) Defects

    # Seats
    seat_condition = db.Column(db.String(10), nullable=False)  # a) Good Condition b) Defect
    seat_comfort = db.Column(db.String(10), nullable=False)  # a) Comfortable b) Uncomfortable
    seatbelts = db.Column(db.String(10), nullable=False)  # a) Yes b) No

    # Driver's Seat
    steering_condition = db.Column(db.String(10), nullable=False)  # a) Working Accurately b) Defects Occurring
    clutch_pedal = db.Column(db.String(10), nullable=False)  # a) Soft b) Hard

    # Floor Mats and Glove Box
    floor_mats = db.Column(db.String(10), nullable=False)  # a) Available b) Not Available
    glove_box = db.Column(db.String(10), nullable=False)  # a) Yes b) No

    # Switch Controls Condition
    headlight_switch = db.Column(db.String(10), nullable=False)  # a) Working b) Not Working
    turn_signal_switch = db.Column(db.String(10), nullable=False)  # a) Working b) Not Working
    hazard_light_switch = db.Column(db.String(10), nullable=False)  # a) Working b) Not Working
    wiper_switch = db.Column(db.String(10), nullable=False)  # a) Working b) Not Working
    fog_light_switch = db.Column(db.String(10), nullable=False)  # a) Working b) Not Working
    audio_system_control = db.Column(db.String(10), nullable=False)  # a) Working b) Not Working
    switch_illumination = db.Column(db.String(10), nullable=False)  # a) Working b) Not Working

    # Exterior - Front Bumper
    front_bumper_condition = db.Column(db.String(10), nullable=False)  # a) Good b) Defect
    front_bumper_alignment = db.Column(db.String(10), nullable=False)  # a) Perfect b) Misalignment
    fog_lights = db.Column(db.String(10), nullable=False)  # a) Perfect b) Not Working
    bumper_scratches = db.Column(db.String(10), nullable=False)  # a) Clean b) Scratches

    # Exterior - Hood
    hood_condition = db.Column(db.String(10), nullable=False)  # a) Good b) Defects
    hood_alignment = db.Column(db.String(10), nullable=False)  # a) Perfect b) Misalignment
    hood_functionality = db.Column(db.String(10), nullable=False)  # a) Perfect b) Not Working

    # Exterior - Front Windshield
    front_windshield_condition = db.Column(db.String(10), nullable=False)  # a) Clear b) Scratches or Cracks
    windshield_sealing = db.Column(db.String(10), nullable=False)  # a) Perfect b) Fault
    windshield_wipers = db.Column(db.String(10), nullable=False)  # a) Good b) Not Working
    windshield_clarity = db.Column(db.String(10), nullable=False)  # a) Perfect b) Not Clear

    # Roof
    roof_noise = db.Column(db.String(10), nullable=False)  # a) Perfect b) Fault
    roof_condition = db.Column(db.String(10), nullable=False)  # a) Good b) Fault
    roof_rail = db.Column(db.String(10), nullable=False)  # a) Perfect b) Fault

    # Rear Windshield
    rear_windshield_condition = db.Column(db.String(10), nullable=False)  # a) Clear b) Scratches or Cracks
    rear_windshield_sealing = db.Column(db.String(10), nullable=False)  # a) Perfect b) Fault
    rear_windshield_wipers = db.Column(db.String(10), nullable=False)  # a) Good b) Not Working
    rear_windshield_clarity = db.Column(db.String(10), nullable=False)  # a) Perfect b) Not Clear

    # Tail Gate
    tail_gate_condition = db.Column(db.String(10), nullable=False)  # a) Clean b) Scratches or Dents
    tail_gate_alignment = db.Column(db.String(10), nullable=False)  # a) Perfect b) Misalignment
    tail_gate_functionality = db.Column(db.String(10), nullable=False)  # a) Perfect b) Not Working

    # Rear Bumper
    rear_bumper_condition = db.Column(db.String(10), nullable=False)  # a) Good b) Defect
    rear_bumper_alignment = db.Column(db.String(10), nullable=False)  # a) Perfect b) Misalignment
    rear_bumper_scratches = db.Column(db.String(10), nullable=False)  # a) Clean b) Scratches

    # Engine Bay
    engine_oil_leaks = db.Column(db.String(10), nullable=False)  # a) Clean b) Oil Stains
    coolant_level = db.Column(db.String(10), nullable=False)  # a) Accurate b) Inaccurate
    engine_oil_level = db.Column(db.String(10), nullable=False)  # a) Accurate b) Inaccurate
    washer_fluid_level = db.Column(db.String(10), nullable=False)  # a) Accurate b) Inaccurate
    wiring_condition = db.Column(db.String(10), nullable=False)  # a) Perfect b) Wear and Tear

    # Tyres
    tyre_damage = db.Column(db.String(10), nullable=False)  # a) Perfect b) Wear and Tear
    tyre_manufacturing_date = db.Column(db.String(10), nullable=False)  # a) Perfect b) Old Tyres
    tyre_grip = db.Column(db.String(10), nullable=False)  # a) Perfect b) Wear Down

    # Notes
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Inspection {self.id}'