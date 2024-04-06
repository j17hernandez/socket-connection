import psycopg2
from psycopg2 import Error
import socket


# Conexión a la base de datos PostgreSQL
def connect_to_database():
    try:
        connection = psycopg2.connect(
            user="admin",
            password="P4ssW0rD",
            host="localhost",
            port="5432",
            database="postgres_db"
        )
        print("Conexión a la base de datos PostgreSQL establecida")
        return connection
    except (Exception, Error) as error:
        print("Error al conectar a la base de datos PostgreSQL:", error)

# Función para buscar una persona por número de teléfono
def find_person_by_dir_tel(phone_number):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Consulta para buscar la persona por número de teléfono
        query = f"""SELECT dir_nombre, dir_tel, dir_tipo_tel, dir_direccion, ciud_nombre
        FROM personas INNER JOIN ciudades ON
        personas.dir_ciud_id = ciudades.ciud_id WHERE dir_tel = '{phone_number}';"""
        cursor.execute(query)

        # Obtenemos los resultados
        person = cursor.fetchone()

        cursor.close()
        connection.close()

        return person
    except (Exception, Error) as error:
        print("Error al buscar la persona en la base de datos:", error)


def init_server():
    # Creamos un objeto de tipo socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Obtenemos la dirección IP de la máquina actual
    host = socket.gethostname()
    port = 12345

    # Enlazamos el socket al host y al puerto
    server_socket.bind((host, port))

    # Escuchamos conexiones entrantes
    server_socket.listen(5)

    print(f"Servidor escuchando en {host}:{port}")

    while True:
        # Aceptamos una nueva conexión
        client_socket, addr = server_socket.accept()
        print(f"Conexión establecida desde {addr}")

        # Recibimos el número de teléfono del cliente
        phone_number = client_socket.recv(1024).decode()
        print(f"Número de teléfono recibido del cliente: {phone_number}")

        # Buscamos la persona en la base de datos
        person = find_person_by_dir_tel(phone_number)

        if person:
            nombre, telefono, tipo_telefono, direccion, ciudad = person
            # Enviamos los datos de la persona al cliente
            response = f"""
            Nombre: {nombre}
            Teléfono: {telefono}
            Tipo de teléfono: {tipo_telefono}
            Dirección: {direccion}
            Ciudad: {ciudad}"""
        else:
            response = "No se encontró ninguna persona con ese número de teléfono"

        # Enviamos la respuesta al cliente
        client_socket.send(response.encode())

        # Cerramos la conexión con el cliente
        client_socket.close()


def create_tables():
    # Conexión a la base de datos PostgreSQL
    connection = connect_to_database()
    # Crear un cursor para ejecutar comandos SQL
    cursor = connection.cursor()

    try:
        # Crear tabla de ciudades
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ciudades (
                ciud_id SERIAL PRIMARY KEY,
                ciud_nombre VARCHAR(100) NOT NULL
            )
        ''')

        # Crear tabla de personas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personas (
                dir_tel SERIAL PRIMARY KEY,
                dir_tipo_tel VARCHAR(50),
                dir_nombre VARCHAR(100),
                dir_direccion VARCHAR(200),
                dir_ciud_id INTEGER REFERENCES ciudades(ciud_id)
            )
        ''')

        # Confirmar los cambios
        connection.commit()
        print("Tablas creadas exitosamente.")

    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)

    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

def preload_data():
    # Conexión a la base de datos PostgreSQL
    connection = connect_to_database()

    # Crear un cursor para ejecutar comandos SQL
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM ciudades")
        cities_count = cursor.fetchone()[0]

        # Verificar si hay registros en la tabla de personas
        cursor.execute("SELECT COUNT(*) FROM personas")
        person_count = cursor.fetchone()[0]

        # Si no hay registros en ambas tablas, cargar datos de prueba
        if cities_count == 0 and person_count == 0:
            # Datos de prueba para ciudades
            data_cities = [
                ("New York",),
                ("Los Angeles",),
                ("Chicago",),
                ("Houston",),
                ("Phoenix",)
            ]


            # Datos de prueba para personas
            data_persons = [
                (123456789, "celular", "Jorge Luis", "123 Main St", 1),
                (987654321, "casa", "Oscar David", "456 Elm St", 2),
                (111222333, "trabajo", "Laura Ximena", "789 Oak St", 3),
                (444555666, "celular", "Emily Brown", "101 Pine St", 4),
                (777888999, "casa", "Christopher Lee", "202 Maple St", 5)
            ]

            # Insertar datos de prueba en la tabla de ciudades
            cursor.executemany("INSERT INTO ciudades (ciud_nombre) VALUES (%s)", data_cities)

            # Insertar datos de prueba en la tabla de personas
            cursor.executemany("INSERT INTO personas (dir_tel, dir_tipo_tel, dir_nombre, dir_direccion, dir_ciud_id) VALUES (%s, %s, %s, %s, %s)", data_persons)

            # Confirmar los cambios
            connection.commit()
            print("Datos de prueba cargados exitosamente.")
        else:
            print("Los datos de prueba ya existen en la base de datos.")

    except psycopg2.Error as e:
        print("Error al cargar los datos de prueba:", e)

    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()


if __name__ == "__main__":
    create_tables()
    preload_data()
    init_server()
    