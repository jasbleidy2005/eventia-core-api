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

