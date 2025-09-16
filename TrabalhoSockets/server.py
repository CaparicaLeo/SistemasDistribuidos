import socket
import threading

# --- Estado Global do Servidor (Lobby) ---
jogadores = [] # Lista de tuplas (conn, addr, simbolo, nickname)
lock = threading.Lock()

def broadcast(jogadores_da_partida, mensagem, excecao=None):
    for conn, _, _, _ in jogadores_da_partida:
        if conn != excecao:
            try:
                conn.sendall(mensagem.encode('utf-8'))
            except:
                pass

def iniciar_jogo(jogadores_da_partida):
    """Gerencia o fluxo de UMA partida."""
    tabuleiro = [" " for _ in range(9)]
    vez_do_jogador_idx = 0
    
    _, _, p1_simbolo, p1_nick = jogadores_da_partida[0]
    _, _, p2_simbolo, p2_nick = jogadores_da_partida[1]

    try:
        broadcast(jogadores_da_partida, f"MSG|{p1_nick} vs {p2_nick}! O jogo vai começar.\nMSG|{p1_nick} ({p1_simbolo}) inicia.\n")

        while True:
            conn_atual, _, simbolo_atual, nickname_atual = jogadores_da_partida[vez_do_jogador_idx]
            
            prompt_msg = f"TURN|Sua vez, {nickname_atual}. Escolha (0-8) ou 'sair':\n"
            broadcast(jogadores_da_partida, f"BOARD|\n {tabuleiro[0]} | {tabuleiro[1]} | {tabuleiro[2]} \n---+---+---\n {tabuleiro[3]} | {tabuleiro[4]} | {tabuleiro[5]} \n---+---+---\n {tabuleiro[6]} | {tabuleiro[7]} | {tabuleiro[8]} \n")
            conn_atual.send(prompt_msg.encode('utf-8'))
            broadcast(jogadores_da_partida, f"WAIT|Aguardando a jogada de {nickname_atual} ({simbolo_atual})...\n", excecao=conn_atual)

            data = conn_atual.recv(1024).decode('utf-8').strip()
            if not data: raise ConnectionError(f"Jogador {nickname_atual} desconectou.")

            if data.lower() == 'sair':
                outro_jogador_idx = 1 - vez_do_jogador_idx
                conn_outro, _, _, _ = jogadores_da_partida[outro_jogador_idx]
                
                print(f"Jogador {nickname_atual} saiu.")
                conn_outro.send(f"MSG|{nickname_atual} saiu do jogo. Aguardando um novo oponente...\n".encode('utf-8'))
                conn_atual.send("END|Você saiu do jogo.\n".encode('utf-8'))
                
                with lock:
                    jogadores.remove(jogadores_da_partida[vez_do_jogador_idx])
                conn_atual.close()
                return

            if data.isdigit() and 0 <= int(data) <= 8 and tabuleiro[int(data)] == " ":
                tabuleiro[int(data)] = simbolo_atual
            else:
                conn_atual.send("MSG|Jogada inválida. Tente novamente.\n".encode('utf-8'))
                continue

            vencedor_simbolo = verificar_vencedor(tabuleiro)
            if vencedor_simbolo:
                vencedor_nick = p1_nick if vencedor_simbolo == p1_simbolo else p2_nick
                final_board = f"BOARD|\n {tabuleiro[0]} | {tabuleiro[1]} | {tabuleiro[2]} \n---+---+---\n {tabuleiro[3]} | {tabuleiro[4]} | {tabuleiro[5]} \n---+---+---\n {tabuleiro[6]} | {tabuleiro[7]} | {tabuleiro[8]} \n"
                broadcast(jogadores_da_partida, final_board)
                if vencedor_simbolo == "EMPATE": broadcast(jogadores_da_partida, "END|⚖️  Deu velha! O jogo empatou.\n")
                else: broadcast(jogadores_da_partida, f"END|🏆 {vencedor_nick} ({vencedor_simbolo}) venceu!\n")
                
                with lock:
                    for jogador in jogadores_da_partida:
                        jogadores.remove(jogador)
                        try: jogador[0].close()
                        except: pass
                return
            else:
                vez_do_jogador_idx = 1 - vez_do_jogador_idx
    
    except (ConnectionError, ConnectionResetError) as e:
        print(f"Partida encerrada por desconexão: {e}")
        with lock:
            for jogador in jogadores_da_partida:
                if jogador in jogadores:
                    jogadores.remove(jogador)
                try: jogador[0].close()
                except: pass

def verificar_vencedor(tabuleiro):
    # (código sem alterações)
    combinacoes_vitoria = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in combinacoes_vitoria:
        if tabuleiro[a] == tabuleiro[b] == tabuleiro[c] and tabuleiro[a] != " ":
            return tabuleiro[a]
    if " " not in tabuleiro:
        return "EMPATE"
    return None

def main():
    """Função principal que atua como LOBBY."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 5000))
    server_socket.listen()
    print("✔ Servidor/Lobby iniciado. Aguardando jogadores...")

    while True:
        conn, addr = server_socket.accept()
        with lock:
            if len(jogadores) < 2:
                try:
                    nickname = conn.recv(1024).decode('utf-8').strip()
                    if not nickname:
                        nickname = f"Jogador_{addr[1]}"
                except:
                    conn.close()
                    continue

                if len(jogadores) == 0:
                    simbolo = 'X'
                else:
                    simbolo_existente = jogadores[0][2]
                    simbolo = 'O' if simbolo_existente == 'X' else 'X'
                
                jogador_novo = (conn, addr, simbolo, nickname)
                jogadores.append(jogador_novo)
                print(f"{nickname} ({simbolo}) entrou no lobby. Jogadores online: {len(jogadores)}")
                conn.send(f"MSG|Bem-vindo, {nickname}! Você é o jogador {simbolo}. Aguardando oponente...\n".encode('utf-8'))

                if len(jogadores) == 2:
                    print("Lobby cheio! Iniciando uma nova partida...")
                    partida_atual = tuple(jogadores)
                    threading.Thread(target=iniciar_jogo, args=(partida_atual,)).start()
            else:
                conn.send("MSG|Servidor cheio, tente mais tarde.\n".encode('utf-8'))
                conn.close()

if __name__ == "__main__":
    main()