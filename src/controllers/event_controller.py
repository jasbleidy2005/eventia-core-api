from flask import request, jsonify
from src.services.event_service import EventService
from src.models.event import Event
from datetime import datetime

class EventController:
    def __init__(self):
        self.service = EventService()
    
    def create_event(self):
        try:
            data = request.get_json()
            
            # Validaciones básicas
            if not data.get('name') or not data.get('date') or not data.get('capacity'):
                return jsonify({'error': 'Faltan campos requeridos'}), 400
            
            event = Event(
                name=data['name'],
                description=data.get('description', ''),
                date=datetime.fromisoformat(data['date']),
                location=data.get('location', ''),
                capacity=int(data['capacity'])
            )
            
            created_event = self.service.create_event(event)
            return jsonify(created_event.to_dict()), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_all_events(self):
        try:
            events = self.service.get_all_events()
            return jsonify(events), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_event(self, event_id):
        try:
            event = self.service.get_event_by_id(event_id)
            if not event:
                return jsonify({'error': 'Evento no encontrado'}), 404
            return jsonify(event), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def update_event(self, event_id):
        try:
            data = request.get_json()
            self.service.update_event(event_id, data)
            return jsonify({'message': 'Evento actualizado exitosamente'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def delete_event(self, event_id):
        try:
            self.service.delete_event(event_id)
            return jsonify({'message': 'Evento eliminado exitosamente'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500