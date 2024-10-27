from flask import render_template, redirect, url_for, flash, request, jsonify, make_response
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, AddVehicleForm, InspectionForm
from app.models import User, Vehicle, Inspection
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import quote
import json
import matplotlib
from fpdf import FPDF
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, ast, json
import base64
from collections import defaultdict

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
    
    if request.method == 'POST' and form.validate_on_submit():
        selected_vehicle = form.vehicle_id.data

        if not selected_vehicle:
            flash('Please select a vehicle.', 'danger')
            return render_template('inspect.html', form=form, vehicles=vehicles)

        # Create a new inspection entry
        inspection = Inspection(
            vehicle_id=selected_vehicle,
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

            # Count pass/fail fields and generate the results dictionary
            pass_count = 0
            fail_count = 0
            results = {}
 
            fail_criteria = ['dented', 'misaligned', 'cracked', 'not_properly_sealed', 'noise_detected', 'worn', 
                 'leaking', 'scratched', 'defect', 'no', 'defects', 'hard', 'not_working', 
                 'faulty', 'scratches', 'blurry', 'damaged', 'low', 'old', 'worn_out', 
                 'uncomfortable', 'defects_occurring', 'not_available', 'misalignment']
            
            # Define pass criteria (examples added, adjust as needed)
            pass_criteria = ['no_noise', 'no_scratches', 'no_leaks', 'working_properly', 'aligned', 'sealed', 'new', 
                 'comfortable', 'clear', 'full', 'functional', 'good_condition', 'yes']
            
            # Count pass/fail fields and generate the results dictionary
            for field, value in form.data.items():
                if field != 'csrf_token' and isinstance(value, str):
                    value = value.strip().lower()

                    # Check for fail criteria first
                    if any(fail_word in value for fail_word in fail_criteria):
                        fail_count += 1
                        results[field] = value  # Only add to results if it is a failure

                    # Check for pass criteria (optional: you can still track passes if needed)
                    elif any(pass_word in value for pass_word in pass_criteria):
                        pass_count += 1
                                
            # Prepare defects identified for results
            defects_identified = {field: value for field, value in results.items() if any(fail_word in value for fail_word in fail_criteria)}

            # Calculate percentages
            total_tests = pass_count + fail_count
            pass_percentage = (pass_count / total_tests) * 100 if total_tests > 0 else 0
            fail_percentage = (fail_count / total_tests) * 100 if total_tests > 0 else 0


            # Serialize the results dictionary to JSON for reporting

            return redirect(url_for('report',
                        pass_percentage=pass_percentage,
                        fail_percentage=fail_percentage,
                        results=json.dumps(defects_identified)))

        except Exception as e:
            db.session.rollback()  # Rollback the session if an error occurs
            print(f"Error during commit: {e}")
            flash('An error occurred while recording the inspection. Please try again.', 'danger')

    return render_template('inspect.html', form=form, vehicles=vehicles, name=current_user.username)

@app.route('/report')
@login_required
def report():
    pass_percentage = float(request.args.get('pass_percentage', 0))
    fail_percentage = float(request.args.get('fail_percentage', 0))
    results_str = request.args.get('results', '{}')

    # Convert the results string back into a dictionary
    results = json.loads(results_str)

    # Generate pie chart
    labels = ['Pass', 'Fail']
    sizes = [pass_percentage, fail_percentage]
    colors = ['#00ff00', '#ff0000']
    explode = (0.1, 0)

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=90)
    ax.axis('equal')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    

    # Show report page with pie chart and defects
    return render_template('report.html', plot_url=plot_url, results=results)

@app.route('/document', methods=['GET', 'POST'])
def document():
    if request.method == 'POST':
        # Get form data
        checked_documents = request.form.getlist('documents')

        # List of all documents
        all_documents = [
            'paperwork', 'invoice', 'sales_certificate', 'payment_receipts',
            'registration_book', 'insurance', 'puc', 'owners_manual',
            'duplicate_keys', 'warranty', 'extended_warranty', 'battery_warranty',
            'roadside_assistance', 'business_cards'
        ]

        # Determine unchecked documents
        unchecked_documents = list(set(all_documents) - set(checked_documents))

        return redirect(url_for('report2', unchecked_documents=json.dumps(unchecked_documents)))

    return render_template('document.html')

@app.route('/report2')
def report2():
    # Get the unchecked documents from the URL parameters
    unchecked_documents = request.args.get('unchecked_documents', '[]')
    unchecked_documents = json.loads(unchecked_documents)

    return render_template('report2.html', unchecked_documents=unchecked_documents)

@app.route('/download_report')
def download_report():
    # Get the unchecked documents from the URL parameters (if necessary)
    unchecked_documents = request.args.get('unchecked_documents', '[]')
    unchecked_documents = json.loads(unchecked_documents)

    # Create a PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add content to the PDF
    pdf.cell(200, 10, txt="Inspection Report", ln=True, align='C')
    pdf.cell(200, 10, txt="Unchecked Documents:", ln=True)

    for doc in unchecked_documents:
        pdf.cell(200, 10, txt=doc, ln=True)

    # Create a response object with the PDF
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Disposition'] = 'attachment; filename=inspection_report.pdf'
    response.headers['Content-Type'] = 'application/pdf'

    return response

@app.route('/logout')
@login_required  # Ensure that only logged-in users can access this route
def logout():
    # Log out the user
    logout_user()
    
    # Optionally, flash a message to indicate successful logout
    flash('You have been logged out successfully.', 'success')
    
    # Redirect the user to the login page or home page
    return redirect(url_for('login'))

@app.route('/download_inspection_report')
def download_inspection_report():
    # Get parameters from the request
    results = request.args.get('results', '{}')
    plot_url = request.args.get('plot_url', None)

    # Debug output
    print("Incoming Results:", results)
    print("Incoming Plot URL:", plot_url)

    # Safely load results from JSON
    try:
        results = json.loads(results)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        results = {}

    # Check the structure of results
    print("Parsed Results:", results)

    # Create a PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, txt="Inspection Report", ln=True, align='C')

    # Check if plot_url is valid
    if plot_url and "," in plot_url:
        try:
            # Extract base64 content for image
            base64_image = plot_url.split(",")[1]
            with open("temp_image.png", "wb") as img_file:
                img_file.write(base64.b64decode(base64_image))  # Decode base64 image
            pdf.image("temp_image.png", x=10, y=20, w=180)  # Adjust as needed
            pdf.ln(85)  # Move below the image
        except Exception as e:
            print("Error processing plot_url:", e)
            pdf.cell(200, 10, txt="Error loading image.", ln=True)
    else:
        pdf.cell(200, 10, txt="No image available.", ln=True)

    # Add defects identified
    pdf.cell(200, 10, txt="Defects Identified:", ln=True)
    
    if not results:
        pdf.cell(200, 10, txt="No defects identified. All fields passed inspection!", ln=True)
    else:
        for field, defect in results.items():
            pdf.cell(200, 10, txt=f"{field}: {defect}", ln=True)

    # Create a response object with the PDF
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Disposition'] = 'attachment; filename=inspection_report.pdf'
    response.headers['Content-Type'] = 'application/pdf'

    return response



@app.context_processor
def utility_processor():
    return dict(json=json)