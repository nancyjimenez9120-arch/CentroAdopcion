import config 
from datetime import datetime

def get_available_dogs():
    conn = config.get_db_connection()
    if not conn: return []
    cur = conn.cursor()
    # Forzamos el orden: 0:id, 1:name, 2:breed, 3:age
    # Aunque en tu tabla física 'breed' sea la última, este SELECT la pone en la posición 2
    cur.execute("SELECT id, name, breed, age FROM Dog WHERE adopted = 0")
    dogs = cur.fetchall()
    cur.close()
    conn.close()
    return dogs

def get_dog_by_id(dog_id):
    conn = config.get_db_connection()
    if not conn: return None
    cur = conn.cursor()
    # Mantenemos el mismo orden para que el formulario de adopción no confunda los datos
    cur.execute("SELECT id, name, breed, age FROM Dog WHERE id = %s", (dog_id,))
    dog = cur.fetchone()
    cur.close()
    conn.close()
    return dog

def register_adoption_transactional(dog_id, name, lastname, address, id_card):
    conn = config.get_db_connection()
    if not conn: return False
    
    cur = conn.cursor()
    try:
        # Iniciamos transacción para que se guarde todo o nada
        conn.start_transaction()
        
        # 1. Registrar a la Persona
        cur.execute(
            "INSERT INTO Person (name, lastName, id_card) VALUES (%s, %s, %s)", 
            (name, lastname, id_card)
        )
        person_id = cur.lastrowid 
        
        # 2. Registrar al Adoptante
        cur.execute(
            "INSERT INTO Adopter (person_id, address) VALUES (%s, %s)", 
            (person_id, address)
        )
        
        # 3. Registrar la Adopción con Fecha y Hora actual
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(
            "INSERT INTO Adoption (adopter_id, dog_id, adoption_date) VALUES (%s, %s, %s)", 
            (person_id, dog_id, fecha_actual)
        )
        
        # 4. Marcar al perro como adoptado (cambia el 0 por 1)
        cur.execute("UPDATE Dog SET adopted = 1 WHERE id = %s", (dog_id,))
        
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"Error crítico en la adopción: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def get_adoption_history():
    conn = config.get_db_connection()
    if not conn: return []
    cur = conn.cursor()
    # Consulta optimizada para unir las tablas y mostrar los datos en el historial
    query = """
        SELECT 
            P.name, 
            P.lastName, 
            D.name, 
            D.breed, 
            A.adoption_date
        FROM Adoption A
        JOIN Adopter Ad ON A.adopter_id = Ad.person_id
        JOIN Person P ON Ad.person_id = P.id
        JOIN Dog D ON A.dog_id = D.id
        ORDER BY A.adoption_date DESC
    """
    cur.execute(query)
    history = cur.fetchall()
    cur.close()
    conn.close()
    return history