class AppointmentsManager:
    def __init__(self, db):
        self.db = db

    def get_appointments(self):
        """Retrieve all appointments."""
        query = '''
                SELECT * FROM Appointments;
                '''
        response = self.db.execute_query(query)
        return response

    def confirm_appointment(self, appointment_id):
        """Confirm an appointment by setting it as confirmed."""
        query = f'''
                UPDATE Appointments
                SET confirmed = TRUE  -- Assuming there is a 'confirmed' column to update
                WHERE id = {appointment_id};
                '''
        response = self.db.execute_query(query)
        return response

    def cancel_appointment(self, appointment_id):
        """Cancel an appointment by removing it."""
        query = f'''
                DELETE FROM Appointments
                WHERE id = {appointment_id};
                '''
        response = self.db.execute_query(query)
        return response

    def get_appointments_per_doctor(self, doctor_id):
        """Get all appointments for a specific doctor."""
        query = f'''
                SELECT * FROM Appointments
                WHERE doctor_id = {doctor_id};
                '''
        response = self.db.execute_query(query)
        return response

    def get_available_appointments(self):
        """Retrieve appointments that have not yet been booked (no patient_id assigned)."""
        query = '''
                SELECT * FROM Appointments
                WHERE patient_id IS NULL;
                '''
        response = self.db.execute_query(query)
        return response

