from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
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
    car_name = StringField('Car Name', validators=[DataRequired(), Length(min=2, max=50)])
    car_model = StringField('Car Model', validators=[DataRequired(), Length(min=2, max=50)])
    manufacture_year = IntegerField('Manufacture Year', validators=[DataRequired()])
    vin = StringField('Vehicle Identification Number (VIN)', validators=[DataRequired(), Length(min=10, max=17)])
    license_plate = StringField('License Plate Number', validators=[DataRequired(), Length(min=2, max=10)])
    color = StringField('Color', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add Vehicle')