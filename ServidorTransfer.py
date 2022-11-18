import os           #Libreria para Sistema Operativo
import socket       #Libreria Socket
import threading    #Libreria para hilo
from pathlib import Path

IP = socket.gethostbyname(socket.gethostname()) # consiegue la direccion de cada compu
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

carpeta= os.path.exists('server_data') # verifica que exista una carpeta donde guardaremos archivos
if (carpeta):
    SERVER_DATA_PATH = "server_data"    # Ruta de la carpeta para almacenar archivos
else:
    os.mkdir('server_data')            #Crea carpeta si no exite
    SERVER_DATA_PATH = "server_data"    # Ruta de la carpeta para almacenar archivos


def handle_client(conn, addr):      #funcion  para conectar al servidor
    print(f"[NUEVA CONEXION] {addr} Conectado.")

    conn.send("OK@Bienvenido al servidor de archivos".encode(FORMAT)) # Formato  comando @ mensaje

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")                      #split divide  cadena con el @
        cmd = data[0]

        if cmd == "LISTAR":                         #listar los archivos que esten en la carpeta del servidor
            files = os.listdir(SERVER_DATA_PATH)    #metodo directorios
            send_data = "OK@"

            if len(files) == 0:
               send_data += "El servidor está vacío"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "CARGAR":               # cargar el archivos seleccionado
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(text)
            send_data = "OK@Archivo cargado exitosamente."
            conn.send(send_data.encode(FORMAT))

        elif cmd == "BORRAR":                # Borrar de la lista archivo
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]
            if len(files) == 0:
                send_data += "El servidor está vacío"
            else:
                if filename in files:
                    os.system(f"rm {SERVER_DATA_PATH}/{filename}")    # con rm para remover archivo
                    send_data += "Archivo borrado exitosamente"
                else:
                    send_data += "Archivo no encontrado"

            conn.send(send_data.encode(FORMAT))

        elif cmd == "SALIR": #SAlir
            break

        elif cmd == "AYUDA":
            data = "OK@"
            data += "LISTAR: Listar todos los archivos del servidor.\n"
            data += "CARGAR <path>: Cargar un archivo al servidor.\n"
            data += "BORRAR <filename>: Borrar archivo del servidor.\n"
            data += "SALIR: Disconnect from the server.\n"
            data += "AYUDA: Listar los comandos."
            conn.send(data.encode(FORMAT))

    print(f"[DESCONECTADO] {addr} se a desconectado") #Manda msj al cliente de desconexion
    conn.close()                                      #cierra la conexion

def main():
    print("[INICIANDO] el servidor está iniciando")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # protocolos INET = ipv4 y SOCK_STREAM = tcp

    server.bind(ADDR)
    server.listen()
    print(f"[ESCUCHANDO] Servidor escuchando en  {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr)) # Crea y asiga hilo a cada cliente para que sea concurrente
        thread.start()                                                     # Se ejecuta el hilo creado
        print(f"[CONEXIONES ACTIVAS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()
