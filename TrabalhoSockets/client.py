import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 5000))

while True:
    msg = client_socket.recv(2048).decode()
    if not msg:
        break
    print(msg)
    if "Escolha" in msg:
        jogada = input(">> ")
        client_socket.send(jogada.encode())
