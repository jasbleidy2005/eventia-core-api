import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.event_service import EventService
from src.models.event import Event
from datetime import datetime

class TestEventService:
    
    @patch('src.services.event_service.Database.get_connection')
    @patch('src.services.event_service.RedisClient.get_instance')
    def test_create_event_success(self, mock_redis, mock_db):
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        mock_cache = MagicMock()
        mock_redis.return_value = mock_cache
        
        service = EventService()
        event = Event(
            name="Concierto Rock",
            description="Gran concierto",
            date=datetime(2025, 12, 31, 20, 0),
            location="Estadio Central",
            capacity=1000
        )
        
        # Act
        result = service.create_event(event)
        
        # Assert
        assert result.id == 1
        assert result.name == "Concierto Rock"
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cache.delete.assert_called_with('all_events')
    
    @patch('src.services.event_service.Database.get_connection')
    @patch('src.services.event_service.RedisClient.get_instance')
    def test_get_all_events_from_cache(self, mock_redis, mock_db):
        # Arrange
        mock_cache = MagicMock()
        cached_events = [
            {'id': 1, 'name': 'Evento 1', 'capacity': 100},
            {'id': 2, 'name': 'Evento 2', 'capacity': 200}
        ]
        mock_cache.get.return_value = cached_events
        mock_redis.return_value = mock_cache
        
        service = EventService()
        
        # Act
        result = service.get_all_events()
        
        # Assert
        assert len(result) == 2
        assert result[0]['name'] == 'Evento 1'
        mock_cache.get.assert_called_with('all_events')
        mock_db.assert_not_called()  # No debe consultar la BD si hay cache
    
    @patch('src.services.event_service.Database.get_connection')
    @patch('src.services.event_service.RedisClient.get_instance')
    def test_get_all_events_from_db(self, mock_redis, mock_db):
        # Arrange
        mock_cache = MagicMock()
        mock_cache.get.return_value = None  # Sin caché
        mock_redis.return_value = mock_cache
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        events_from_db = [
            {'id': 1, 'name': 'Evento DB',
              'capacity': 150,
              'date': '2025-12-31T20:00:00',
              'created_at': '2025-11-15T10:00:00'}
        ]
        mock_cursor.fetchall.return_value = events_from_db
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        service = EventService()
        
        # Act
        result = service.get_all_events()
        
        # Assert
        assert len(result) == 1
        assert result[0]['name'] == 'Evento DB'
        assert mock_cursor.execute.called
        assert mock_cursor.fetchall.called
        mock_cache.set.assert_called_once()  # Debe guardar en caché
    
    @patch('src.services.event_service.Database.get_connection')
    @patch('src.services.event_service.RedisClient.get_instance')
    def test_delete_event_success(self, mock_redis, mock_db):
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        mock_cache = MagicMock()
        mock_redis.return_value = mock_cache
        
        service = EventService()
        
        # Act
        result = service.delete_event(1)
        
        # Assert
        assert result is True
        mock_cursor.execute.assert_called_with("DELETE FROM events WHERE id = %s", (1,))
        mock_conn.commit.assert_called_once()
        mock_cache.delete.assert_called_with('all_events')