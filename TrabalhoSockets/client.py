import socket
import threading
import os

def receive_messages(client_socket):
    buffer = ""
    while True:
        try:
            data = client_socket.recv(2048).decode('utf-8')
            if not data: break
            
            buffer += data
            
            while '\n' in buffer:
                msg, buffer = buffer.split('\n', 1)
                
                if not msg: continue

                if msg.startswith("BOARD|"):
                    board_data = msg[6:]
                    while board_data.count('\n') < 4:
                        more_data, buffer = buffer.split('\n', 1)
                        board_data += '\n' + more_data
                    print(board_data)
                elif msg.startswith("TURN|"):
                    jogada = input(msg[5:] + " ")
                    client_socket.send(jogada.encode('utf-8'))
                elif msg.startswith("WAIT|"): print(msg[5:])
                elif msg.startswith("MSG|"): print(msg[4:])
                elif msg.startswith("END|"):
                    print(msg[4:])
                    raise ConnectionAbortedError("Fim de jogo normal.")
                else:
                    print(msg)
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            break
            
    print("\nVocê foi desconectado. Pressione Enter para sair.")
    try:
        client_socket.close()
    except:
        pass

def start_client():
    SERVER_IP = input("👨‍💻 Digite o endereço IP do servidor: ")
    SERVER_PORT = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        
        nickname = input("🗣️ Digite seu nome para o jogo: ")
        client_socket.send(nickname.encode('utf-8'))
        print("✔ Conectado e nome enviado! Aguardando o jogo...")

    except ConnectionRefusedError:
        print("❌ Servidor offline ou recusou a conexão.")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao conectar: {e}")
        return

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    receive_thread.join()
    
    input()
    os._exit(0)

if __name__ == "__main__":
    start_client()