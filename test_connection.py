import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # cámbiala
        database="eventia_db",      # cámbiala si aplica
        port=3306
    )

    if connection.is_connected():
        print("Conexión exitosa a MySQL")

except Exception as e:
    print("Error conectando a MySQL:", e)
