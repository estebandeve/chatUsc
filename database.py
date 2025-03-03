import oracledb
import config
import os

oracledb.init_oracle_client(lib_dir="/usr/lib/oracle/21/client64/lib")

def get_connection():
    try:
        connection = oracledb.connect(
            user=config.DB_USERNAME,
            password=config.DB_PASSWORD,
            dsn=f"{config.DB_HOST}:{config.DB_PORT}/{config.DB_DATABASE}"
        )
        return connection
    except oracledb.DatabaseError as e:
        print("Error al conectar a la base de datos:", e)
        return None


# Obtener lista de tablas
def get_tablas():
    conn = get_connection()
    if conn is None:
        print("No se pudo conectar a la base de datos")
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT table_name FROM user_tables")  
        tablas = [row[0] for row in cursor.fetchall()]
        print("Tablas encontradas:", tablas)  
        return tablas
    except Exception as e:
        print(f"Error al obtener tablas: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def get_asistentes():
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT titulo FROM asistentes")  
        asistentes = cursor.fetchall()
        
        asistentes_lista = [{"titulo": row[0]} for row in asistentes]
        
        return asistentes_lista
    except oracledb.DatabaseError as e:
        print(f"Error al obtener asistentes: {e}")
        return []
    finally:
        cursor.close()
        connection.close()
