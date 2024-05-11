class AppointmentsManager:
    def __init__(self, db_conn):
        self.db = db_conn
        # self.token = token

    def validate_token(self, token):
        return self.users_manager.validate_token(token)

    def get_appointments(self):
        """Retrieve all appointments with doctor details."""
        query = '''
                SELECT a.appointment_id, a.appointment_date, d.user_id, u.full_name AS doctor_name, u.specialty
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.doctor_id
                JOIN users u ON d.user_id = u.user_id;
                '''
        appointments = self.db.execute_query(query)
        if appointments:
            return {'status': 'success', 'data': appointments}
        else:
            return {'status': 'error', 'message': 'No appointments found.'}

    def confirm_appointment(self, appointment_id, token):
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

