import mysql.connector
from mysql.connector import Error
from src.config.settings import Config

class Database:
    _instance = None
    
    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )
            return connection
        except Error as e:
            print(f"Error conectando a MySQL: {e}")
            return None