import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.List;

public interface GerenciadorDeTarefas extends Remote {
    void adicionarTarefa(String descricao, String nomeUsuario) throws RemoteException;
    List<Tarefa> listarTarefa(String nomeUsuario) throws RemoteException;
    boolean removerTarefa(int id, String nomeUsuario) throws RemoteException;
}