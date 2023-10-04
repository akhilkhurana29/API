from flask import Flask, jsonify,request

app = Flask(__name__)

# Sample doctor data for demonstration
doctors = [
    {
        "id": 1,
        "name": "Dr. Rahul k",
        "specialty": "Cardiologist",
         "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "max_patients": 5
    },
    {
        "id": 2,
        "name": "Dr. Akhil J",
        "specialty": "Dermatologist",
         "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "max_patients": 8
    },
    {
        "id": 3,
        "name": "Dr. Ankit",
        "specialty": "Dermatologist",
         "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "max_patients": 2
    },
    {
        "id": 4,
        "name": "Dr. Amar P",
        "specialty": "Dermatologist",
         "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "max_patients": 1
    }
]

@app.route('/api/doctors', methods=['GET'])
def list_doctors():
    return jsonify(doctors)

@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = next((d for d in doctors if d["id"] == doctor_id), None)
    if doctor:
        return jsonify(doctor)
    else:
        return jsonify({"error": "Doctor not found"}), 404


appointments = []

@app.route('/api/appointments', methods=['POST'])
def book_appointment():
    data = request.json
    doctor_id = data.get("doctor_id")
    appointment_date = data.get("appointment_date")
    
    # Check if the doctor exists
    doctor = next((d for d in doctors if d["id"] == doctor_id), None)
    
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404
    
    # Check if the appointment date is valid for the doctor
    if appointment_date not in doctor["available_days"]:
        return jsonify({"error": "doctor is not available"}), 400
    
    # Check if the doctor's maximum patient limit is reached
    if len([a for a in appointments if a["doctor_id"] == doctor_id]) >= doctor["max_patients"]:
        return jsonify({"error": "Doctor's schedule is fully booked"}), 400
    
    # Book the appointment
    appointment = {
        "doctor_id": doctor_id,
        "patient_name": data.get("patient_name"),
        "appointment_date": appointment_date
    }
    appointments.append(appointment)
    
    return jsonify(appointment), 201



if __name__ == '__main__':
    app.run(debug=True)

