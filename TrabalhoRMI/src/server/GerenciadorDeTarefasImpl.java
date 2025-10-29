package server;

import shared.GerenciadorDeTarefas;
import shared.Tarefa;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

public class GerenciadorDeTarefasImpl extends UnicastRemoteObject implements GerenciadorDeTarefas {
    private final List<Tarefa> listaDeTarefas = Collections.synchronizedList(new ArrayList<Tarefa>());
    private final AtomicInteger proximoId = new AtomicInteger(1);

    protected GerenciadorDeTarefasImpl() throws RemoteException{
        super();
    }

    @Override
    public void adicionarTarefa(String descricao, String nomeUsuario) throws RemoteException {
        int id = proximoId.getAndIncrement();
        Tarefa novaTarefa = new Tarefa(id, descricao, nomeUsuario);
        listaDeTarefas.add(novaTarefa);
        System.out.println("Servidor: Tarefa adicionada por " + nomeUsuario + " -> " + novaTarefa);
    }

    @Override
    public List<Tarefa> listarTarefa(String nomeUsuario) throws RemoteException {
        System.out.println("Servidor: Requisição para listar tarefas recebida. Usuario: "+ nomeUsuario);
        return new ArrayList<>(listaDeTarefas);
    }

    @Override
    public boolean removerTarefa(int id, String nomeUsuario) throws RemoteException {
        synchronized (listaDeTarefas) {
            Tarefa tarefaParaRemover = null;
            boolean idEncontrado = false;

            for (Tarefa tarefa : listaDeTarefas) {
                if (tarefa.getId() == id) {
                    idEncontrado = true;

                    if (tarefa.getUsuario().equals(nomeUsuario)) {
                        tarefaParaRemover = tarefa;
                    }
                    break;
                }
            }

            if (tarefaParaRemover != null) {
                listaDeTarefas.remove(tarefaParaRemover);
                System.out.println("Servidor: Tarefa com ID " + id + " removida por " + nomeUsuario + " (proprietário verificado).");
                return true;
            } else {
                if (idEncontrado) {
                    System.out.println("Servidor: Tentativa de remover tarefa com ID " + id + " por " + nomeUsuario + ". Falha: Usuário não é o proprietário.");
                } else {
                    System.out.println("Servidor: Tentativa de remover tarefa com ID " + id + " por " + nomeUsuario + ". Falha: Tarefa não encontrada.");
                }
                return false;
            }
        }
    }
}
