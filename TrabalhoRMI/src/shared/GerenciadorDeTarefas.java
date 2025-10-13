package shared;

import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.List;

public interface GerenciadorDeTarefas extends Remote {
    void adicionarTarefa(String descricao) throws RemoteException;
    List<Tarefa> listarTarefa() throws RemoteException;
    boolean removerTarefa(int id) throws RemoteException;
}
