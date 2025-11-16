from flask import request, jsonify
from src.services.participant_service import ParticipantService
from src.models.participant import Participant

class ParticipantController:
    def __init__(self):
        self.service = ParticipantService()
    
    def create_participant(self):
        try:
            data = request.get_json()
            
            if not data.get('name') or not data.get('email'):
                return jsonify({'error': 'Faltan campos requeridos'}), 400
            
            participant = Participant(
                name=data['name'],
                email=data['email'],
                phone=data.get('phone', '')
            )
            
            created_participant = self.service.create_participant(participant)
            return jsonify(created_participant.to_dict()), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_all_participants(self):
        try:
            participants = self.service.get_all_participants()
            return jsonify(participants), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_participant(self, participant_id):
        try:
            participant = self.service.get_participant_by_id(participant_id)
            if not participant:
                return jsonify({'error': 'Participante no encontrado'}), 404
            return jsonify(participant), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def update_participant(self, participant_id):
        try:
            data = request.get_json()
            self.service.update_participant(participant_id, data)
            return jsonify({'message': 'Participante actualizado exitosamente'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def delete_participant(self, participant_id):
        try:
            self.service.delete_participant(participant_id)
            return jsonify({'message': 'Participante eliminado exitosamente'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500