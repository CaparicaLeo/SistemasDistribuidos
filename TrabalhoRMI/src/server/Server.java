package server;

import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

public class Server {
    public static void main(String[] args) {
        try{
            LocateRegistry.createRegistry(1099);
            GerenciadorDeTarefasImpl gerenciador = new GerenciadorDeTarefasImpl();
            Naming.rebind("GerenciadorTarefasService",gerenciador);
            System.out.print(">>> Servidor do Gerenciador de Tarefas está pronto. <<<");

        }catch (Exception e){
            System.err.println("Erro no servidor: " + e.toString());
            e.printStackTrace();
        }
    }
}
