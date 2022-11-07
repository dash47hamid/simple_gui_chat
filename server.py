import socket
import threading

HOST = 'localhost'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen(2)

clients = []

nicknames = []

# broadcast function (sends 1 mesege to all the clients)


def broadcast(message):
    for client in clients:
        client.send(message)


# handle function (handeling the individual conections)
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print("f{nicknames[clients.index(client)]}says{message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

# receive function  (accept new conection) start in main thread


def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}!")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is{nickname}")
        broadcast(f"{nickname}connected to the server!\n".encode("utf-8"))
        client.send("Connected to the server".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(
            client,))  # , for arg is make it tuple
        thread.start()


print("server running....")

receive()
