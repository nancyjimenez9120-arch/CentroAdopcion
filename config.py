import mysql.connector 
from mysql.connector import Error

# Configuración con el nuevo usuario que creaste en Linux
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "admin_perros",
    "password": "nancy123",
    "database": "CentroAdopcion"
}

def get_db_connection():
    try:
        # Los ** sirven para pasar toda la configuración de arriba
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        # Si sale un error, lo veremos en la terminal
        print(f"❌ Error conectando a MySQL: {e}")
        return None