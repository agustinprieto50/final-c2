from datetime import datetime
import jwt
import os
from threading import Lock
from authentication import Authentication

def process_appointment(appointment):
    appointment = dict(appointment)
    appointment['appointment_date'] = appointment['appointment_date'].strftime('%Y-%m-%d %H:%M:%S')
    return appointment

SECRET_KEY = os.getenv('SECRET_KEY')

class AppointmentsManager:
    def __init__(self, db_conn):
        self.db = db_conn
        self.lock = Lock()  
    
    def decode_token(self, token):
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

    def get_appointments(self):
        """Retrieve available appointments where no patient is assigned."""
        query = '''
            SELECT a.appointment_id, u.full_name AS doctor_full_name, a.appointment_date
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            JOIN users u ON d.user_id = u.user_id
            WHERE a.patient_id IS NULL;
        '''
        appointments = self.db.execute_query(query)
        if appointments:
            appointments = [process_appointment(row) for row in appointments]
            return {'status': 'success', 'data': appointments}
        else:
            return {'status': 'error', 'message': 'No available appointments found.'}

    def confirm_appointment(self, appointment_id, token):
        """Confirm an appointment by setting it as confirmed."""
        with self.lock:
                print('Confirming appointment')
                decoded_token = self.decode_token(token)
                user_id = decoded_token['patient_id']
                if user_id:
                    query = '''
                        UPDATE appointments
                        SET patient_id = %s
                        WHERE appointment_id = %s AND patient_id IS NULL;
                        '''
                    self.db.execute_query(query, (int(user_id), int(appointment_id)))
                    return {'status': 'success', 'message': 'Appointment confirmed.'}
                else:
                    return {'status': 'error', 'message': 'Invalid token.'}

    def cancel_appointment(self, appointment_id, token):
        """Cancel an appointment by removing the user from it."""
        with self.lock:
            print('Cancelling appointment')
            decoded_token = self.decode_token(token)
            user_id = decoded_token['patient_id']
            if user_id:
                query = '''
                    UPDATE appointments
                    SET patient_id = NULL
                    WHERE appointment_id = %s AND patient_id = %s;
                    '''
                self.db.execute_query(query, (int(appointment_id), int(user_id)))
                return {'status': 'success', 'message': 'Appointment cancelled.'}
            else:
                return {'status': 'error', 'message': 'Invalid token.'}
            
    def get_appointments_per_patient(self, token):
        """Get all appointments for a specific patient."""
        decoded_token = self.decode_token(token)
        patient_id = decoded_token['patient_id']
        print('Getting appointments for patient:', patient_id)
        query = '''
                SELECT a.appointment_id, u.full_name AS doctor_full_name, a.appointment_date
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.doctor_id
                JOIN users u ON d.user_id = u.user_id
                WHERE a.patient_id = %s;
                '''
        appointments = self.db.execute_query(query, (int(patient_id),))
        if appointments:
            appointments = [process_appointment(row) for row in appointments]
            return {'status': 'success', 'data': appointments}
        else:
            return {'status': 'error', 'message': 'No appointments found.'}

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

