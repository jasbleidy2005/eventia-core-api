from src.database.connection import Database
from src.cache.redis_client import RedisClient
from src.models.event import Event
from datetime import datetime

class EventService:
    def __init__(self):
        self.cache = RedisClient.get_instance()
    
    def create_event(self, event: Event):
        conn = Database.get_connection()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")
        
        cursor = conn.cursor()
        query = """
            INSERT INTO events (name, description, date, location, capacity)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            event.name, event.description, event.date,
            event.location, event.capacity
        ))
        conn.commit()
        event.id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        # Invalidar caché
        self.cache.delete('all_events')
        
        return event
    
    def get_all_events(self):
        # Intentar obtener del caché
        cached = self.cache.get('all_events')
        if cached:
            return cached
        
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        cursor.close()
        conn.close()
        
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        cursor.close()
        conn.close()

        for event in events:
            if 'date' in event and event['date']:
             event['date'] = event['date'].isoformat() if hasattr(event['date'], 'isoformat') else str(event['date'])
            if 'created_at' in event and event['created_at']:
                event['created_at'] = event['created_at'].isoformat() if hasattr(event['created_at'], 'isoformat') else str(event['created_at'])
        
        # Guardar en caché
        self.cache.set('all_events', events, expire=600)
        
        return events
    
    def get_event_by_id(self, event_id):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        event = cursor.fetchone()
        cursor.close()
        conn.close()

        if event:
            if 'date' in event and event['date']:
                event['date'] = event['date'].isoformat() if hasattr(event['date'], 'isoformat') else str(event['date'])
            if 'created_at' in event and event['created_at']:
                event['created_at'] = event['created_at'].isoformat() if hasattr(event['created_at'], 'isoformat') else str(event['created_at'])
    
        return event
    
    def update_event(self, event_id, event_data):
        conn = Database.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE events 
            SET name=%s, description=%s, date=%s, location=%s, capacity=%s
            WHERE id=%s
        """
        cursor.execute(query, (
            event_data['name'], event_data['description'],
            event_data['date'], event_data['location'],
            event_data['capacity'], event_id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        
        self.cache.delete('all_events')
        return True
    
    def delete_event(self, event_id):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        self.cache.delete('all_events')
        return True