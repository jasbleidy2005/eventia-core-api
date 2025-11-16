import pytest
import mysql.connector
import os
import sys 
from src.config.settings import Config

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config.settings import Config
from src.app import create_app

@pytest.fixture
def client():
    """Cliente de pruebas de Flask"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_database():
    """Limpiar base de datos antes de cada prueba"""
    conn = mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )
    cursor = conn.cursor()
    
    # Limpiar tablas antes de cada test
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE attendance")
    cursor.execute("TRUNCATE TABLE events")
    cursor.execute("TRUNCATE TABLE participants")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    yield
    
    # Opcional: limpiar también después del test
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