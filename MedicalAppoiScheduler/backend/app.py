import os
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Setup Flask and SQLAlchemy
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(basedir, '../db')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
db_path = os.path.join(db_dir, 'appointments.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

# Model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    doctor_name = db.Column(db.String(100), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    reminder_sent = db.Column(db.Boolean, default=False)

# Serve the frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

# Serve static files (CSS/JS)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('../frontend/static', path)

# API endpoints
@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    new_appointment = Appointment(
        patient_name=data['patient_name'],
        doctor_name=data['doctor_name'],
        appointment_time=datetime.strptime(data['appointment_time'], '%Y-%m-%d %H:%M:%S')
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({"message": "Appointment created successfully!"}), 201

@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    print(appointments)  # Debugging line to print the raw SQLAlchemy objects
    output = []
    for appointment in appointments:
        appointment_data = {
            'patient_name': appointment.patient_name,
            'doctor_name': appointment.doctor_name,
            'appointment_time': appointment.appointment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'reminder_sent': appointment.reminder_sent
        }
        output.append(appointment_data)
    print(output)  # Debugging line to print the output list
    return jsonify(output)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
