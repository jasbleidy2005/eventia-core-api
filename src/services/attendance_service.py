from src.database.connection import Database
from src.cache.redis_client import RedisClient
from src.models.attendance import Attendance

class AttendanceService:
    def __init__(self):
        self.cache = RedisClient.get_instance()
    
    def register_attendance(self, attendance: Attendance):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Validar que el evento existe
        cursor.execute("SELECT * FROM events WHERE id = %s", (attendance.event_id,))
        event = cursor.fetchone()
        if not event:
            cursor.close()
            conn.close()
            raise Exception("El evento no existe")
        
        # Validar que el participante existe
        cursor.execute("SELECT * FROM participants WHERE id = %s", (attendance.participant_id,))
        participant = cursor.fetchone()
        if not participant:
            cursor.close()
            conn.close()
            raise Exception("El participante no existe")
        
        # Verificar si ya está registrado
        cursor.execute("""
            SELECT * FROM attendance 
            WHERE event_id = %s AND participant_id = %s
        """, (attendance.event_id, attendance.participant_id))
        existing = cursor.fetchone()
        if existing:
            cursor.close()
            conn.close()
            raise Exception("El participante ya está registrado en este evento")
        
        # Verificar capacidad disponible
        cursor.execute("""
            SELECT COUNT(*) as count FROM attendance WHERE event_id = %s
        """, (attendance.event_id,))
        count_result = cursor.fetchone()
        current_count = count_result['count']
        
        if current_count >= event['capacity']:
            cursor.close()
            conn.close()
            raise Exception("El evento ha alcanzado su capacidad máxima")
        
        # Registrar asistencia
        cursor.execute("""
            INSERT INTO attendance (event_id, participant_id)
            VALUES (%s, %s)
        """, (attendance.event_id, attendance.participant_id))
        conn.commit()
        attendance.id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        # Invalidar caché de estadísticas
        self.cache.delete(f'event_stats_{attendance.event_id}')
        
        return attendance
    
    def get_event_participants(self, event_id):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT p.*, a.registered_at
            FROM participants p
            INNER JOIN attendance a ON p.id = a.participant_id
            WHERE a.event_id = %s
        """
        cursor.execute(query, (event_id,))
        participants = cursor.fetchall()
        cursor.close()
        conn.close()

        for participant in participants:
            if 'created_at' in participant and participant['created_at']:
                participant['created_at'] = participant['created_at'].isoformat() if hasattr(participant['created_at'], 'isoformat') else str(participant['created_at'])
            if 'registered_at' in participant and participant['registered_at']:
                participant['registered_at'] = participant['registered_at'].isoformat() if hasattr(participant['registered_at'], 'isoformat') else str(participant['registered_at'])
        return participants
    
    def get_participant_events(self, participant_id):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT e.*, a.registered_at
            FROM events e
            INNER JOIN attendance a ON e.id = a.event_id
            WHERE a.participant_id = %s
        """
        cursor.execute(query, (participant_id,))
        events = cursor.fetchall()
        cursor.close()
        conn.close()

        for event in events:
            if 'date' in event and event['date']:
                event['date'] = event['date'].isoformat() if hasattr(event['date'], 'isoformat') else str(event['date'])
            if 'created_at' in event and event['created_at']:
                event['created_at'] = event['created_at'].isoformat() if hasattr(event['created_at'], 'isoformat') else str(event['created_at'])
            if 'registered_at' in event and event['registered_at']:
                event['registered_at'] = event['registered_at'].isoformat() if hasattr(event['registered_at'], 'isoformat') else str(event['registered_at'])
        return events
    
    def get_event_statistics(self, event_id):
        # Intentar obtener del caché
        cache_key = f'event_stats_{event_id}'
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Obtener información del evento
        cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        event = cursor.fetchone()
        
        if not event:
            cursor.close()
            conn.close()
            return None
        
        # Contar asistentes registrados
        cursor.execute("""
            SELECT COUNT(*) as registered FROM attendance WHERE event_id = %s
        """, (event_id,))
        count_result = cursor.fetchone()
        registered = count_result['registered']
        
        cursor.close()
        conn.close()
        
        stats = {
            'event_id': event_id,
            'event_name': event['name'],
            'capacity': event['capacity'],
            'registered': registered,
            'available': event['capacity'] - registered,
            'occupancy_percentage': round((registered / event['capacity']) * 100, 2)
        }
        
        # Guardar en caché
        self.cache.set(cache_key, stats, expire=300)
        
        return stats
    
    def cancel_attendance(self, event_id, participant_id):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM attendance 
            WHERE event_id = %s AND participant_id = %s
        """, (event_id, participant_id))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        
        if affected > 0:
            self.cache.delete(f'event_stats_{event_id}')
            return True
        return False