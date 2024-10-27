from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddVehicleForm(FlaskForm):
    brand = SelectField('Brand', choices=[('Suzuki', 'Suzuki'), ('Tata', 'Tata'), ('Mahendra', 'Mahendra'),
                                          ('Hyundai', 'Hyundai'), ('Honda', 'Honda'), ('MG', 'MG'), 
                                          ('KIA', 'KIA'), ('BYD', 'BYD'), ('Jeep', 'Jeep'), ('Toyota', 'Toyota'),
                                          ('Mercedes-Benz', 'Mercedes-Benz'), ('BMW', 'BMW'), ('Audi', 'Audi'),
                                          ('Jaguar', 'Jaguar'), ('Land Rover', 'Land Rover'), ('Range Rover', 'Range Rover')],
                        validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year_of_manufacture = IntegerField('Year of Manufacture', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    transmission_type = SelectField('Transmission Type', choices=[('Manual', 'Manual'), ('Automatic', 'Automatic')], validators=[DataRequired()])
    fuel_type = SelectField('Fuel Type', choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('CNG', 'CNG'),('Electric', 'Electric')], validators=[DataRequired()])
    submit = SubmitField('Add Vehicle')

class InspectionForm(FlaskForm):
    # Dropdown for vehicle selection
    vehicle_id = SelectField('Vehicle', coerce=int)

     # Interior - Dashboard
    dashboard_defects = SelectField('Do you notice any scratches, stains, or other defects on the dashboard?',choices=[('Perfect', 'Perfect'), ('Defects', 'Defects')])

    # Interior - Seats
    seats_condition = SelectField('Seats should have no tears, stains, or damage', choices=[('Good Condition', 'Good Condition'), ('Defect', 'Defect')])
    seat_comfort = SelectField('Try both the front and back seats', choices=[('Comfortable', 'Comfortable'), ('Uncomfortable', 'Uncomfortable')])
    seatbelts = SelectField('Do all the seatbelts work?', choices=[('Yes', 'Yes'), ('No', 'No')])

    # Interior - Driver's Seat
    steering_condition = SelectField('Steering wheel positioning, tilt, telescope, lock, horn, and cruise control', choices=[('Working Accurately', 'Working Accurately'), ('Defects Occurring', 'Defects Occurring')])
    clutch_pedal = SelectField('Is the clutch pedal soft or Hard?', choices=[('Soft', 'Soft'), ('Hard', 'Hard')])
    floor_mats = SelectField('Are the floor mats you ordered in the car present?', choices=[('Available', 'Available'), ('Not Available', 'Not Available')])
    glove_box = SelectField('Does the glove box open properly?', choices=[('Yes', 'Yes'), ('No', 'No')])

    # Switch Controls
    headlight_switch = SelectField('Headlight switch functionality', choices=[('Working', 'Working'), ('Not Working', 'Not Working')])
    turn_signal_switch = SelectField('Turn signal switch operation', choices=[('Working', 'Working'), ('Not Working', 'Not Working')])
    hazard_light_switch = SelectField('Hazard light switch activation', choices=[('Working', 'Working'), ('Not Working', 'Not Working')])
    wiper_switch = SelectField('Wiper switch functionality', choices=[('Working', 'Working'), ('Not Working', 'Not Working')])
    fog_light_switch = SelectField('Fog light switch operation', choices=[('Working', 'Working'), ('Not Working', 'Not Working')])
    audio_system_control = SelectField('Audio system control functionality', choices=[('Working', 'Working'), ('Not Working', 'Not Working')])
    switch_illumination = SelectField('Switch illumination and indicator light', choices=[('Working', 'Working'), ('Not Working', 'Not Working')])

    # Exterior - Front bumper
    front_bumper_condition = RadioField('Front bumper condition', choices=[('Good', 'Good'), ('Defect', 'Defect')], validators=[DataRequired()])
    front_bumper_alignment = RadioField('Bumper alignment with vehicle body', choices=[('Perfect', 'Perfect'), ('Misalignment', 'Misalignment')], validators=[DataRequired()])
    fog_lights = RadioField('Functionality (fog lights, sensors)', choices=[('Perfect', 'Perfect'), ('Not Working', 'Not Working')], validators=[DataRequired()])
    bumper_scratches = RadioField('Scratches on bumper', choices=[('Clean', 'Clean'), ('Scratches', 'Scratches')], validators=[DataRequired()])


    # Inspection Fields for Hood
    hood_condition = RadioField('Hood Condition (scratches, dents)', choices=[('good', 'Good'), ('scratched', 'Scratched'), ('dented', 'Dented')], validators=[DataRequired()])
    hood_alignment = RadioField('Proper alignment of the hood', choices=[('aligned', 'Aligned'), ('misaligned', 'Misaligned')], validators=[DataRequired()])
    hood_functionality = RadioField('Functionality of the hood (locking mechanism)', choices=[('working', 'Working'), ('faulty', 'Faulty')], validators=[DataRequired()])

    # Front Windshield
    front_windshield_condition = RadioField('Front Windshield Condition', choices=[('good', 'Good'), ('scratched', 'Scratched'), ('cracked', 'Cracked')], validators=[DataRequired()])
    windshield_sealing = RadioField('Windshield Sealing', choices=[('sealed', 'Properly Sealed'), ('not_sealed', 'Not Properly Sealed')], validators=[DataRequired()])
    windshield_wipers_functionality = RadioField(' Functionality of windshield wipers', choices=[('working', 'Working'), ('not_working', 'Not Working')], validators=[DataRequired()])
    windshield_clarity = RadioField(' Windshield clarity and visibility', choices=[('clear', 'Clear'), ('blurry', 'Blurry')], validators=[DataRequired()])

    # Roof
    roof_noise = RadioField('Roof Noise or Vibration', choices=[('no_noise', 'No Noise'), ('noise', 'Noise Detected')], validators=[DataRequired()])
    roof_condition = RadioField('Roof Condition', choices=[('good', 'Good'), ('scratched', 'Scratched'), ('dented', 'Dented')], validators=[DataRequired()])
    roof_rails = RadioField('Roof Rails Condition', choices=[('good', 'Good'), ('worn', 'Worn')], validators=[DataRequired()])

    # Rear Windshield
    rear_windshield_condition = RadioField('Rear Windshield Condition', choices=[('good', 'Good'), ('scratched', 'Scratched'), ('cracked', 'Cracked')], validators=[DataRequired()])
    rear_windshield_sealing = RadioField('Properly installed and sealed with rubber beadings', choices=[('sealed', 'Properly Sealed'), ('not_sealed', 'Not Properly Sealed')], validators=[DataRequired()])
    rear_windshield_wipers = RadioField('Rear Windshield Wipers Functionality', choices=[('working', 'Working'), ('not_working', 'Not Working')], validators=[DataRequired()])
    rear_windshield_clarity = RadioField('Windshield clarity and visibility', choices=[('clear', 'Clear'), ('blurry', 'Blurry')], validators=[DataRequired()])

    # Tail Gate
    tail_gate_condition = RadioField('Tail Gate Condition', choices=[('good', 'Good'), ('scratched', 'Scratched'), ('dented', 'Dented')], validators=[DataRequired()])
    tail_gate_alignment = RadioField('Tail Gate Alignment', choices=[('aligned', 'Aligned'), ('misaligned', 'Misaligned')], validators=[DataRequired()])
    tail_gate_functionality = RadioField('Tail Gate Functionality', choices=[('working', 'Working'), ('faulty', 'Faulty')], validators=[DataRequired()])

    # Rear Bumper
    rear_bumper_condition = RadioField('Rear Bumper Condition', choices=[('good', 'Good'), ('scratched', 'Scratched')], validators=[DataRequired()])
    rear_bumper_alignment = RadioField('Rear Bumper Alignment', choices=[('aligned', 'Aligned'), ('misaligned', 'Misaligned')], validators=[DataRequired()])
    rear_bumper_scratches = RadioField('Rear Bumper Scratches', choices=[('no_scratches', 'No Scratches'), ('scratched', 'Scratched')], validators=[DataRequired()])

    # Engine Bay
    engine_oil_leaks = RadioField('Oil Leaks in Engine Bay', choices=[('no_leaks', 'No Leaks'), ('leaking', 'Leaking')], validators=[DataRequired()])
    coolant_level = RadioField('Coolant Level', choices=[('good', 'Good'), ('low', 'Low')], validators=[DataRequired()])
    engine_oil_level = RadioField('Engine Oil Level', choices=[('good', 'Good'), ('low', 'Low')], validators=[DataRequired()])
    washer_fluid_level = RadioField('Washer Fluid Level', choices=[('good', 'Good'), ('low', 'Low')], validators=[DataRequired()])
    wiring_condition = RadioField('Electrical Wiring Condition', choices=[('good', 'Good'), ('damaged', 'Damaged')], validators=[DataRequired()])

    # Tyres
    tyre_damage = RadioField('Tyre Damage', choices=[('good', 'Good'), ('damaged', 'Damaged')], validators=[DataRequired()])
    tyre_manufacturing_date = RadioField('Tyre Manufacturing Date', choices=[('recent', 'Recent'), ('old', 'Old')], validators=[DataRequired()])
    tyre_grip = RadioField('Tyre Grip Condition', choices=[('good', 'Good'), ('worn_out', 'Worn Out')], validators=[DataRequired()])

    #notes
    notes = TextAreaField('Additional Notes')

    submit = SubmitField('Submit Inspection')