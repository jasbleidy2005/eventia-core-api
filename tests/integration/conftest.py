import pytest
import mysql.connector
from src.config.settings import Config

@pytest.fixture(autouse=True)
def clean_database():
    """Limpiar base de datos antes de cada prueba de integración"""
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor()
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE attendance")
        cursor.execute("TRUNCATE TABLE events")
        cursor.execute("TRUNCATE TABLE participants")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Warning: Could not clean database: {e}")
    
    yield