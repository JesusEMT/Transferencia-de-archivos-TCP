import socket
IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")
        if cmd == "DESCONECTADO":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]
        if cmd == "AYUDA":
            client.send(cmd.encode(FORMAT))

        elif cmd == "SALIR":
            client.send(cmd.encode(FORMAT))
            break

        elif cmd == "LISTAR":
            client.send(cmd.encode(FORMAT))

        elif cmd == "BORRAR":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))

        elif cmd == "CARGAR":
            path = data[1]
            with open(f"{path}", "r") as f:
                text = f.read()
                # print(f)
            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))
            # try:
            # f= open(f"{path}", "r")
            # text = f.read()
            # filename = path.split("/")[-1]
            # send_data = f"{cmd}@{filename}@{text}"
            # client.send(send_data.encode(FORMAT))
            # # except FileNotFoundError:
                # print("No existe el archivo")
                # main()

    print("Se ah desconectado del servidor.")
    client.close()

if __name__ == "__main__":
    main()
