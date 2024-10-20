from flask import render_template, redirect, url_for, flash, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, AddVehicleForm, InspectionForm
from app.models import User, Vehicle, Inspection
from flask_login import login_user, logout_user, login_required, current_user

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
        vehicle = Vehicle(
            brand=form.brand.data,
            model=form.model.data,
            year_of_manufacture=form.year_of_manufacture.data,
            color=form.color.data,
            transmission_type=form.transmission_type.data,
            fuel_type=form.fuel_type.data,
            user_id=current_user.id  # Link vehicle to the logged-in user
        )
        db.session.add(vehicle)
        db.session.commit()
        flash('Vehicle has been added successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        print(form.errors)
    return render_template('add_vehicle.html', form=form)

@app.route("/inspect", methods=['GET', 'POST'])
@login_required
def inspect():
    vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    form = InspectionForm()

    if not vehicles:
        flash('No vehicles found. Please add a vehicle first.', 'danger')
        return redirect(url_for('add_vehicle'))

    # Populate the vehicle choices (ID, Name)
    form.vehicle_id.choices = [(vehicle.id, f"{vehicle.brand} {vehicle.model}") for vehicle in vehicles]
    
    # Check if the request method is POST for form submission
    if request.method == 'POST' and form.validate_on_submit():
        selected_vehicle = form.vehicle_id.data

        if not selected_vehicle:
            flash('Please select a vehicle.', 'danger')
            return render_template('inspect.html', form=form, vehicles=vehicles)

        # Create a new inspection entry
        inspection = Inspection(
            vehicle_id=selected_vehicle,  # Use the selected vehicle
            dashboard_defects=form.dashboard_defects.data,
            seat_condition=form.seats_condition.data,
            seat_comfort=form.seat_comfort.data,
            seatbelts=form.seatbelts.data,
            steering_condition=form.steering_condition.data,
            clutch_pedal=form.clutch_pedal.data,
            floor_mats=form.floor_mats.data,
            glove_box=form.glove_box.data,
            headlight_switch=form.headlight_switch.data,
            turn_signal_switch=form.turn_signal_switch.data,
            hazard_light_switch=form.hazard_light_switch.data,
            wiper_switch=form.wiper_switch.data,
            fog_light_switch=form.fog_light_switch.data,
            audio_system_control=form.audio_system_control.data,
            switch_illumination=form.switch_illumination.data,
            front_bumper_condition=form.front_bumper_condition.data,
            front_bumper_alignment=form.front_bumper_alignment.data,
            fog_lights=form.fog_lights.data,
            bumper_scratches=form.bumper_scratches.data,
            hood_condition=form.hood_condition.data,
            hood_alignment=form.hood_alignment.data,
            hood_functionality=form.hood_functionality.data,
            front_windshield_condition=form.front_windshield_condition.data,
            windshield_sealing=form.windshield_sealing.data,
            windshield_wipers=form.windshield_wipers_functionality.data,
            windshield_clarity=form.windshield_clarity.data,
            roof_noise=form.roof_noise.data,
            roof_condition=form.roof_condition.data,
            roof_rail=form.roof_rails.data,
            rear_windshield_condition=form.rear_windshield_condition.data,
            rear_windshield_sealing=form.rear_windshield_sealing.data,
            rear_windshield_wipers=form.rear_windshield_wipers.data,
            rear_windshield_clarity=form.rear_windshield_clarity.data,
            tail_gate_condition=form.tail_gate_condition.data,
            tail_gate_alignment=form.tail_gate_alignment.data,
            tail_gate_functionality=form.tail_gate_functionality.data,
            rear_bumper_condition=form.rear_bumper_condition.data,
            rear_bumper_alignment=form.rear_bumper_alignment.data,
            rear_bumper_scratches=form.rear_bumper_scratches.data,
            engine_oil_leaks=form.engine_oil_leaks.data,
            coolant_level=form.coolant_level.data,
            engine_oil_level=form.engine_oil_level.data,
            washer_fluid_level=form.washer_fluid_level.data,
            wiring_condition=form.wiring_condition.data,
            tyre_damage=form.tyre_damage.data,
            tyre_manufacturing_date=form.tyre_manufacturing_date.data,
            tyre_grip=form.tyre_grip.data,
            notes=form.notes.data
        )

        db.session.add(inspection)
        try:
            db.session.commit()

             # Calculate pass/fail percentages
            pass_count = 0
            fail_count = 0
            results = {}

            # Define the fail criteria (what counts as a defect)
            fail_criteria = ['Defect', 'No', 'Defects', 'Hard', 'Not Working', 'Faulty', 'Scratches', 'Blurry', 'Damaged', 'Low', 'Old', 'Worn Out']

            # Count passed/failed fields
            for field, value in form.data.items():
                if field != 'csrf_token' and value in fail_criteria:
                    fail_count += 1
                    results[field] = value
                else:
                    pass_count += 1

            total_tests = pass_count + fail_count
            pass_percentage = (pass_count / total_tests) * 100
            fail_percentage = (fail_count / total_tests) * 100

            # Redirect to the report page with the calculated data
            flash('Vehicle inspection recorded successfully.', 'success')
            return redirect(url_for('report', pass_percentage=pass_percentage, fail_percentage=fail_percentage, results=results))
            
        except Exception as e:
            db.session.rollback()  # Rollback the session if an error occurs
            print(f"Error during commit: {e}")  # Print the error message
            flash('An error occurred while recording the inspection. Please try again.', 'danger')
    else:
        # Print and log the errors for debugging
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {getattr(form, field).label.text}: {error}")
        flash('Please correct the errors in the form.', 'danger')

    return render_template('inspect.html', form=form, vehicles=vehicles)


@app.route('/report')
@login_required
def report():
    pass_percentage = float(request.args.get('pass_percentage', 0))
    fail_percentage = float(request.args.get('fail_percentage', 0))
    results = request.args.get('results', {})

    # Generate pie chart
    labels = ['Pass', 'Fail']
    sizes = [pass_percentage, fail_percentage]
    colors = ['#00ff00', '#ff0000']
    explode = (0.1, 0)  # explode the 'Pass' slice

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Convert plot to PNG image and then to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Show report page with pie chart and defects
    return render_template('report.html', plot_url=plot_url, results=results)