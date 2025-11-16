import pytest
from src.app import create_app
import json



class TestFullFlow:
    
    def test_complete_event_registration_flow(self, client):
        """
        Test del flujo completo:
        1. Crear evento
        2. Crear participante
        3. Registrar asistencia
        4. Verificar estadísticas
        5. Obtener participantes del evento
        """
        
        # 1. Crear evento
        event_data = {
            'name': 'Workshop Python',
            'description': 'Taller de programación',
            'date': '2025-12-15T10:00:00',
            'location': 'Aula 101',
            'capacity': 30
        }
        
        event_response = client.post(
            '/api/events',
            data=json.dumps(event_data),
            content_type='application/json'
        )
        assert event_response.status_code == 201
        event = json.loads(event_response.data)
        event_id = event['id']
        
        # 2. Crear participante
        participant_data = {
            'name': 'Carlos Rodríguez',
            'email': 'carlos@example.com',
            'phone': '5551234567'
        }
        
        participant_response = client.post(
            '/api/participants',
            data=json.dumps(participant_data),
            content_type='application/json'
        )
        assert participant_response.status_code == 201
        participant = json.loads(participant_response.data)
        participant_id = participant['id']
        
        # 3. Registrar asistencia
        attendance_data = {
            'event_id': event_id,
            'participant_id': participant_id
        }
        
        attendance_response = client.post(
            '/api/attendance',
            data=json.dumps(attendance_data),
            content_type='application/json'
        )
        assert attendance_response.status_code == 201
        
        # 4. Verificar estadísticas
        stats_response = client.get(f'/api/attendance/event/{event_id}/statistics')
        assert stats_response.status_code == 200
        stats = json.loads(stats_response.data)
        assert stats['registered'] == 1
        assert stats['available'] == 29
        assert stats['capacity'] == 30
        
        # 5. Obtener participantes del evento
        participants_response = client.get(f'/api/attendance/event/{event_id}/participants')
        assert participants_response.status_code == 200
        participants = json.loads(participants_response.data)
        assert len(participants) == 1
        assert participants[0]['name'] == 'Carlos Rodríguez'
    
    def test_capacity_limit_enforcement(self, client):
        """Test que verifica que no se puede exceder la capacidad"""
        
        # Crear evento con capacidad de 2
        event_data = {
            'name': 'Evento Pequeño',
            'description': 'Solo 2 personas',
            'date': '2025-12-20T18:00:00',
            'location': 'Sala Pequeña',
            'capacity': 2
        }
        
        event_response = client.post(
            '/api/events',
            data=json.dumps(event_data),
            content_type='application/json'
        )
        event = json.loads(event_response.data)
        event_id = event['id']
        
        # Registrar 2 participantes
        for i in range(2):
            participant_data = {
                'name': f'Participante {i+1}',
                'email': f'participante{i+1}@example.com',
                'phone': f'55512345{i}'
            }
            participant_response = client.post(
                '/api/participants',
                data=json.dumps(participant_data),
                content_type='application/json'
            )
            participant = json.loads(participant_response.data)
            
            attendance_data = {
                'event_id': event_id,
                'participant_id': participant['id']
            }
            attendance_response = client.post(
                '/api/attendance',
                data=json.dumps(attendance_data),
                content_type='application/json'
            )
            assert attendance_response.status_code == 201
        
        # Intentar registrar un tercero (debe fallar)
        participant_data = {
            'name': 'Participante 3',
            'email': 'participante3@example.com',
            'phone': '5551234523'
        }
        participant_response = client.post(
            '/api/participants',
            data=json.dumps(participant_data),
            content_type='application/json'
        )
        participant = json.loads(participant_response.data)
        
        attendance_data = {
            'event_id': event_id,
            'participant_id': participant['id']
        }
        attendance_response = client.post(
            '/api/attendance',
            data=json.dumps(attendance_data),
            content_type='application/json'
        )
        
        assert attendance_response.status_code == 400
        data = json.loads(attendance_response.data)
        assert 'capacidad máxima' in data['error']