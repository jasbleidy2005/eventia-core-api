import pytest
from src.app import create_app
import json


class TestEventAPI:
    
    def test_health_check(self, client):
        """Test del endpoint de health check"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'OK'
    
    def test_create_event(self, client):
        """Test de creación de evento"""
        event_data = {
            'name': 'Evento Test',
            'description': 'Descripción del evento',
            'date': '2025-12-31T20:00:00',
            'location': 'Sala Principal',
            'capacity': 100
        }
        
        response = client.post(
            '/api/events',
            data=json.dumps(event_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Evento Test'
        assert 'id' in data
    
    def test_create_event_missing_fields(self, client):
        """Test de validación de campos requeridos"""
        event_data = {
            'name': 'Evento Incompleto'
            # Faltan campos requeridos
        }
        
        response = client.post(
            '/api/events',
            data=json.dumps(event_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_all_events(self, client):
        """Test de obtención de todos los eventos"""
        response = client.get('/api/events')
        
        if response.status_code != 200:
            print("\n" + "="*50)
            print("\n❌ ERROR:")
            print("="*50)
            print(response.data.decode('utf-8'))
            print("="*50)
    
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_get_event_by_id(self, client):
        """Test de obtención de evento por ID"""
        # Primero crear un evento
        event_data = {
            'name': 'Evento para Buscar',
            'description': 'Test',
            'date': '2025-12-31T20:00:00',
            'location': 'Lugar',
            'capacity': 50
        }
        
        create_response = client.post(
            '/api/events',
            data=json.dumps(event_data),
            content_type='application/json'
        )
        created_event = json.loads(create_response.data)
        event_id = created_event['id']
        
        # Ahora buscar el evento
        response = client.get(f'/api/events/{event_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == event_id
        assert data['name'] == 'Evento para Buscar'
    
    def test_get_nonexistent_event(self, client):
        """Test de búsqueda de evento inexistente"""
        response = client.get('/api/events/99999')
        
        assert response.status_code == 404