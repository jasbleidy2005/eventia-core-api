from flask import request, jsonify
from src.services.attendance_service import AttendanceService
from src.models.attendance import Attendance

class AttendanceController:
    def __init__(self):
        self.service = AttendanceService()
    
    def register_attendance(self):
        try:
            data = request.get_json()
            
            if not data.get('event_id') or not data.get('participant_id'):
                return jsonify({'error': 'Faltan campos requeridos'}), 400
            
            attendance = Attendance(
                event_id=int(data['event_id']),
                participant_id=int(data['participant_id'])
            )
            
            registered = self.service.register_attendance(attendance)
            return jsonify(registered.to_dict()), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    def get_event_participants(self, event_id):
        try:
            participants = self.service.get_event_participants(event_id)
            return jsonify(participants), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_participant_events(self, participant_id):
        try:
            events = self.service.get_participant_events(participant_id)
            return jsonify(events), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_event_statistics(self, event_id):
        try:
            stats = self.service.get_event_statistics(event_id)
            if not stats:
                return jsonify({'error': 'Evento no encontrado'}), 404
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def cancel_attendance(self, event_id, participant_id):
        try:
            success = self.service.cancel_attendance(event_id, participant_id)
            if success:
                return jsonify({'message': 'Asistencia cancelada exitosamente'}), 200
            return jsonify({'error': 'Registro no encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500