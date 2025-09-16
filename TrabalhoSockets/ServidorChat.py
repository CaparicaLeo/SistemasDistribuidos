# servidor_chat.py
import socket
import threading

# --- Configurações do Servidor ---
# Usar '0.0.0.0' para aceitar conexões de qualquer IP na rede
# Ou use 'localhost' (ou '127.0.0.1') para testes apenas na sua máquina
HOST = '0.0.0.0' 
PORT = 55555

# --- Inicialização do Servidor ---
# AF_INET: especifica que usaremos o protocolo IPv4
# SOCK_STREAM: especifica que usaremos o protocolo TCP (confiável e orientado à conexão)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"[*] Servidor escutando em {HOST}:{PORT}")

# --- Gerenciamento de Clientes ---
clients = []
nicknames = []

def broadcast(message, _client=None):
    """ Envia uma mensagem para todos os clientes conectados, exceto para o remetente. """
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                # Se falhar, remove o cliente que não pode ser alcançado
                remove_client(client)

def remove_client(client):
    """ Remove um cliente da lista de ativos. """
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames[index]
        broadcast(f'{nickname} saiu do chat!'.encode('utf-8'))
        nicknames.remove(nickname)
        print(f"[*] Conexão com {nickname} perdida.")

def handle_client(client):
    """ Lida com a comunicação de um cliente específico em uma thread separada. """
    while True:
        try:
            # Recebe mensagens do cliente (buffer de 1024 bytes)
            message = client.recv(1024)
            if not message:
                # Se a mensagem for vazia, o cliente desconectou
                remove_client(client)
                break
            # Transmite a mensagem para os outros clientes
            broadcast(message, client)
        except:
            # Em caso de erro (ex: cliente desconectou abruptamente)
            remove_client(client)
            break

def receive_connections():
    """ Função principal para aceitar novas conexões. """
    while True:
        # A função accept() bloqueia a execução até que uma nova conexão seja feita
        client, address = server.accept()
        print(f"[*] Conexão estabelecida com {str(address)}")

        # Solicita um apelido (nickname) ao cliente
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        
        # Armazena o novo cliente e seu apelido
        nicknames.append(nickname)
        clients.append(client)

        print(f"[*] Apelido do cliente é {nickname}")
        broadcast(f"{nickname} entrou no chat!".encode('utf-8'), client)
        client.send('Conectado ao servidor!'.encode('utf-8'))

        # Inicia uma nova thread para lidar com este cliente
        # Isso permite que o servidor aceite outras conexões simultaneamente
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Inicia a função para aceitar conexões
receive_connections()