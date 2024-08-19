document.getElementById('appointmentForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const patient_name = document.getElementById('patient_name').value;
    const doctor_name = document.getElementById('doctor_name').value;
    const appointment_time = document.getElementById('appointment_time').value;

    const response = await fetch('/appointments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            patient_name: patient_name,
            doctor_name: doctor_name,
            appointment_time: appointment_time.replace('T', ' ')
        })
    });

    if (response.ok) {
        alert('Appointment scheduled successfully!');
        loadAppointments();
    } else {
        alert('Failed to schedule appointment.');
    }
});

async function loadAppointments() {
    const response = await fetch('/appointments');
    const appointments = await response.json();

    const appointmentsList = document.getElementById('appointmentsList');
    appointmentsList.innerHTML = '';

    appointments.forEach(appointment => {
        const li = document.createElement('li');
        li.textContent = `Patient: ${appointment.patient_name}, Doctor: ${appointment.doctor_name}, Time: ${appointment.appointment_time}`;
        appointmentsList.appendChild(li);
    });
}

loadAppointments();
