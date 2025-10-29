package client;

import shared.GerenciadorDeTarefas;
import shared.Tarefa;

import java.rmi.Naming;
import java.util.List;
import java.util.Scanner;

public class Client {
    public static void main(String[] args){
        try{
            // Conecta-se diretamente ao serviço rodando em 'localhost'
            GerenciadorDeTarefas gerenciador = (GerenciadorDeTarefas) Naming.lookup("rmi://localhost/GerenciadorTarefasService");
            Scanner scanner = new Scanner(System.in);

            System.out.print("Digite seu nome de usuário para começar: ");
            String nomeUsuario = scanner.nextLine();
            System.out.println("Bem-vindo(a), " + nomeUsuario + "!");

            int escolha = 0;

            while (escolha != 4) {
                System.out.println("\n--- Gerenciador de Tarefas Remoto ---");
                System.out.println("1. Adicionar Tarefa");
                System.out.println("2. Listar Tarefas");
                System.out.println("3. Remover Tarefa");
                System.out.println("4. Sair");
                System.out.print("Escolha uma opção: ");

                try {
                    escolha = Integer.parseInt(scanner.nextLine());
                } catch (NumberFormatException e) {
                    System.out.println("Opção inválida.");
                    continue;
                }

                switch (escolha) {
                    case 1:
                        System.out.print("Digite a descrição da tarefa: ");
                        String descricao = scanner.nextLine();
                        gerenciador.adicionarTarefa(descricao, nomeUsuario); // Chamada RPC
                        System.out.println("Tarefa adicionada com sucesso!");
                        break;
                    case 2:
                        List<Tarefa> tarefas = gerenciador.listarTarefa(nomeUsuario); // Chamada RPC
                        if (tarefas.isEmpty()) {
                            System.out.println("Nenhuma tarefa na lista.");
                        } else {
                            System.out.println("--- Lista de Tarefas ---");
                            tarefas.forEach(System.out::println);
                        }
                        break;
                    case 3:
                        System.out.print("Digite o ID da tarefa a ser removida: ");
                        try {
                            int id = Integer.parseInt(scanner.nextLine());
                            if (gerenciador.removerTarefa(id, nomeUsuario)) { // Chamada RPC
                                System.out.println("Tarefa removida com sucesso!");
                            } else {
                                System.out.println("Tarefa com o ID informado não encontrada.");
                            }
                        } catch (NumberFormatException e) {
                            System.out.println("ID inválido.");
                        }
                        break;
                    case 4:
                        System.out.println("Saindo...");
                        break;
                    default:
                        System.out.println("Opção inválida.");
                }
            }
            scanner.close();
        }catch(Exception e){
            System.err.println("Erro no cliente: Verifique se o servidor está rodando.");
            e.printStackTrace();
        }
    }
}
