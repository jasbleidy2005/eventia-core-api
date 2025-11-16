import pytest
from src.app import create_app
import json



class TestParticipantAPI:
    
    def test_create_participant(self, client):
        """Test de creación de participante"""
        participant_data = {
            'name': 'Juan Pérez',
            'email': 'juan@example.com',
            'phone': '1234567890'
        }
        
        response = client.post(
            '/api/participants',
            data=json.dumps(participant_data),
            content_type='application/json'
        )
        
        print("\n" + "="*50)
        print("❌ ERROR:")
        print("="*50)
        print(response.data.decode('utf-8'))
        print("="*50)

        assert response.status_code == 201
        data = json.loads(response.data)

        print("DATA PARSED:", data)
        print("NAME:", data.get('name'))

        assert data['name'] == 'Juan Pérez'
        assert data['email'] == 'juan@example.com'
    
    def test_create_participant_duplicate_email(self, client):
        """Test de validación de email duplicado"""
        participant_data = {
            'name': 'María García',
            'email': 'maria@example.com',
            'phone': '0987654321'
        }
        
        # Crear primer participante
        client.post(
            '/api/participants',
            data=json.dumps(participant_data),
            content_type='application/json'
        )
        
        # Intentar crear otro con el mismo email
        response = client.post(
            '/api/participants',
            data=json.dumps(participant_data),
            content_type='application/json'
        )
        
        assert response.status_code == 500  # Error por duplicado
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_all_participants(self, client):
        """Test de obtención de todos los participantes"""
        response = client.get('/api/participants')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)