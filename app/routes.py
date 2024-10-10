from flask import render_template, redirect, url_for, flash
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required, fresh_login_required, current_user
from app.forms import AddVehicleForm
from app.models import Vehicle

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email is already in use. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        # Create new user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route("/add_vehicle", methods=['GET', 'POST'])
@login_required
def add_vehicle():
    form = AddVehicleForm()
    if form.validate_on_submit():
        # Create a new vehicle instance
        vehicle = Vehicle(
            user_id=current_user.id,
            car_name=form.car_name.data,
            car_model=form.car_model.data,
            manufacture_year=form.manufacture_year.data,
            vin=form.vin.data,
            license_plate=form.license_plate.data,
            color=form.color.data
        )
        # Add vehicle to the database
        db.session.add(vehicle)
        db.session.commit()
        flash('Vehicle added successfully!', 'success')
        return redirect(url_for('dashboard'))  # Redirect to dashboard after successful submission
    return render_template('add_vehicle.html', form=form)
