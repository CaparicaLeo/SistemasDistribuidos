import socket
import threading

# Tabuleiro inicial
tabuleiro = [" " for _ in range(9)]
jogadores = []
vez = 0  # 0 -> jogador 1 (X), 1 -> jogador 2 (O)

def imprimir_tabuleiro():
    return f"""
 {tabuleiro[0]} | {tabuleiro[1]} | {tabuleiro[2]}
---+---+---
 {tabuleiro[3]} | {tabuleiro[4]} | {tabuleiro[5]}
---+---+---
 {tabuleiro[6]} | {tabuleiro[7]} | {tabuleiro[8]}
"""

def verificar_vencedor():
    combinacoes = [
        (0,1,2), (3,4,5), (6,7,8),  # linhas
        (0,3,6), (1,4,7), (2,5,8),  # colunas
        (0,4,8), (2,4,6)            # diagonais
    ]
    for a,b,c in combinacoes:
        if tabuleiro[a] == tabuleiro[b] == tabuleiro[c] != " ":
            return True
    return False

def jogo(conn, jogador_id):
    global vez

    simbolo = "X" if jogador_id == 0 else "O"
    conn.send(f"Você é o jogador {simbolo}!\n".encode())

    while True:
        if vez == jogador_id:
            conn.send(f"Sua vez!\n{imprimir_tabuleiro()}Escolha (0-8): ".encode())
            pos = conn.recv(1024).decode().strip()

            if not pos.isdigit() or int(pos) not in range(9) or tabuleiro[int(pos)] != " ":
                conn.send("Jogada inválida, tente de novo.\n".encode())
                continue

            pos = int(pos)
            tabuleiro[pos] = simbolo

            # Atualizar todos os jogadores
            for c in jogadores:
                c.send(f"\n{imprimir_tabuleiro()}".encode())

            if verificar_vencedor():
                for c in jogadores:
                    c.send(f"Jogador {simbolo} venceu!\n".encode())
                break

            if " " not in tabuleiro:
                for c in jogadores:
                    c.send("Empate!\n".encode())
                break

            vez = (vez + 1) % 2
        else:
            conn.send("Aguarde sua vez...\n".encode())

    conn.close()

# --- Servidor principal ---
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 5000))
server_socket.listen(2)

print("Aguardando 2 jogadores...")

while len(jogadores) < 2:
    conn, addr = server_socket.accept()
    jogadores.append(conn)
    print(f"Jogador conectado: {addr}")

# Criar threads para os dois jogadores
for i, conn in enumerate(jogadores):
    threading.Thread(target=jogo, args=(conn,i)).start()
