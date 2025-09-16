# cliente_chat.py
import socket
import threading

# Solicita o apelido ao usuário
nickname = input("Escolha seu apelido: ")

# --- Configurações do Cliente ---
# O cliente PRECISA saber o IP do servidor para se conectar
SERVER_IP = '127.0.0.1' # Mude para o IP da máquina do servidor se for diferente
SERVER_PORT = 55555

# --- Inicialização do Cliente ---
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

def receive_messages():
    """ Recebe mensagens do servidor e as exibe. """
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                # O servidor está pedindo o apelido
                client.send(nickname.encode('utf-8'))
            else:
                # Exibe a mensagem recebida
                print(message)
        except:
            # Se ocorrer um erro, fecha a conexão
            print("Ocorreu um erro! Desconectando...")
            client.close()
            break

def send_messages():
    """ Envia mensagens digitadas pelo usuário para o servidor. """
    while True:
        message_text = input('') # Aguarda o usuário digitar
        message = f'{nickname}: {message_text}'
        client.send(message.encode('utf-8'))

# --- Iniciar Threads ---
# Uma thread para receber mensagens e outra para enviar
# Isso permite que o usuário digite e receba mensagens ao mesmo tempo
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()