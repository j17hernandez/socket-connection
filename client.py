import socket

# Creamos un objeto de tipo socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Obtenemos la dirección IP del servidor
host = socket.gethostname()
port = 12345

# Nos conectamos al servidor
client_socket.connect((host, port))

# Enviamos el número de teléfono al servidor
phone_number = input("Ingrese el número de teléfono del empleado: ")
client_socket.send(phone_number.encode())

# Recibimos la respuesta del servidor
response = client_socket.recv(1024).decode()
print(f"Respuesta del servidor: \n {response}")

# Cerramos la conexión con el servidor
client_socket.close()
