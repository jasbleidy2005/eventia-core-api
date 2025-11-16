from src.database.connection import Database
from src.cache.redis_client import RedisClient
from src.models import participant
from src.models.participant import Participant

class ParticipantService:
    def __init__(self):
        self.cache = RedisClient.get_instance()
    
    def create_participant(self, participant: Participant):
        conn = Database.get_connection()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")
    
        cursor = conn.cursor()
        query = """
            INSERT INTO participants (name, email, phone)
            VALUES (%s, %s, %s)
        """
        try:
            cursor.execute(query, (participant.name, participant.email, participant.phone))
            conn.commit()
            participant.id = cursor.lastrowid
            cursor.close()
        
            # Obtener created_at con un nuevo cursor
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT created_at FROM participants WHERE id = %s", (participant.id,))
            result = cursor.fetchone()  # ← Agregué los paréntesis ()
            if result and 'created_at' in result:
                participant.created_at = result['created_at']  # ← Corregí el nombre
        
            cursor.close()
            conn.close()
        
            self.cache.delete('all_participants')
            return participant
        except Exception as e:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            raise Exception(f"Error al crear participante: {str(e)}")
    
    def get_all_participants(self):
        cached = self.cache.get('all_participants')
        if cached:
            return cached
        
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM participants")
        participants = cursor.fetchall()
        cursor.close()
        conn.close()
        
        for participant in participants:
            if 'created_at' in participant and participant['created_at']:
                participant['created_at'] = participant['created_at'].isoformat() if hasattr(participant['created_at'], 'isoformat') else str(participant['created_at'])

        self.cache.set('all_participants', participants, expire=600)
        return participants
    
    def get_participant_by_id(self, participant_id):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM participants WHERE id = %s", (participant_id,))
        participant = cursor.fetchone()
        cursor.close()
        conn.close()

        if participant and 'created_at' in participant and participant['created_at']:
            participant['created_at'] = participant['created_at'].isoformat() if hasattr(participant['created_at'], 'isoformat') else str(participant['created_at'])
        
        return participant
    
    def get_participant_by_email(self, email):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM participants WHERE email = %s", (email,))
        participant = cursor.fetchone()
        cursor.close()
        conn.close()

        if participant and 'created_at' in participant and participant['created_at']:
            participant['created_at'] = participant['created_at'].isoformat() if hasattr(participant['created_at'], 'isoformat') else str(participant['created_at'])
        
        return participant
    
    def update_participant(self, participant_id, participant_data):
        conn = Database.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE participants 
            SET name=%s, email=%s, phone=%s
            WHERE id=%s
        """
        cursor.execute(query, (
            participant_data['name'],
            participant_data['email'],
            participant_data['phone'],
            participant_id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        
        self.cache.delete('all_participants')
        return True
    
    def delete_participant(self, participant_id):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM participants WHERE id = %s", (participant_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        self.cache.delete('all_participants')
        return True