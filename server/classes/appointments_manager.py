class AppointmentsManager:
    def __init__(self, db):
        self.db = db

    def get_appointments(self):
        """Retrieve all appointments."""

        query = '''
                SELECT a.*, d.full_name AS doctor_name
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.doctor_id;
                '''
        
        response = {}
        

        appointments = self.db.execute_query(query)

        for a in appointments:
            response['doctor_id'] = a[0]
            response['date'] = a[1].strftime("%Y-%m-%d %H:%M:%S")
            response['patient_id'] = a[2]
            response['doctors_full_name'] = a[3]
            response['available'] = True if not a[2] else False

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

