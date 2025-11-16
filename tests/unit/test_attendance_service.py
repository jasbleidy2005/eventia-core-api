import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.attendance_service import AttendanceService
from src.models.attendance import Attendance

class TestAttendanceService:
    
    @patch('src.services.attendance_service.Database.get_connection')
    @patch('src.services.attendance_service.RedisClient.get_instance')
    def test_register_attendance_success(self, mock_redis, mock_db):
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Simular que evento existe
        mock_cursor.fetchone.side_effect = [
            {'id': 1, 'name': 'Evento Test', 'capacity': 100},  # Evento
            {'id': 1, 'name': 'Juan'},  # Participante
            None,  # No hay registro previo
            {'count': 50}  # 50 asistentes registrados
        ]
        mock_cursor.lastrowid = 1
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        mock_cache = MagicMock()
        mock_redis.return_value = mock_cache
        
        service = AttendanceService()
        attendance = Attendance(event_id=1, participant_id=1)
        
        # Act
        result = service.register_attendance(attendance)
        
        # Assert
        assert result.id == 1
        assert result.event_id == 1
        assert result.participant_id == 1
        mock_cache.delete.assert_called_with('event_stats_1')
    
    @patch('src.services.attendance_service.Database.get_connection')
    @patch('src.services.attendance_service.RedisClient.get_instance')
    def test_register_attendance_event_full(self, mock_redis, mock_db):
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Simular evento lleno
        mock_cursor.fetchone.side_effect = [
            {'id': 1, 'name': 'Evento Lleno', 'capacity': 100},
            {'id': 1, 'name': 'Juan'},
            None,  # No hay registro previo
            {'count': 100}  # Ya hay 100 asistentes (lleno)
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        mock_cache = MagicMock()
        mock_redis.return_value = mock_cache
        
        service = AttendanceService()
        attendance = Attendance(event_id=1, participant_id=1)
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            service.register_attendance(attendance)
        
        assert "capacidad máxima" in str(exc_info.value)
    
    @patch('src.services.attendance_service.Database.get_connection')
    @patch('src.services.attendance_service.RedisClient.get_instance')
    def test_register_attendance_duplicate(self, mock_redis, mock_db):
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Simular registro duplicado
        mock_cursor.fetchone.side_effect = [
            {'id': 1, 'name': 'Evento', 'capacity': 100},
            {'id': 1, 'name': 'Juan'},
            {'id': 1, 'event_id': 1, 'participant_id': 1}  # Ya existe
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        mock_cache = MagicMock()
        mock_redis.return_value = mock_cache
        
        service = AttendanceService()
        attendance = Attendance(event_id=1, participant_id=1)
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            service.register_attendance(attendance)
        
        assert "ya está registrado" in str(exc_info.value)
    
    @patch('src.services.attendance_service.Database.get_connection')
    @patch('src.services.attendance_service.RedisClient.get_instance')
    def test_get_event_statistics(self, mock_redis, mock_db):
        # Arrange
        mock_cache = MagicMock()
        mock_cache.get.return_value = None  # Sin caché
        mock_redis.return_value = mock_cache
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [
            {'id': 1, 'name': 'Concierto', 'capacity': 200},
            {'registered': 150}
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        service = AttendanceService()
        
        # Act
        result = service.get_event_statistics(1)
        
        # Assert
        assert result['capacity'] == 200
        assert result['registered'] == 150
        assert result['available'] == 50
        assert result['occupancy_percentage'] == 75.0
        mock_cache.set.assert_called_once()