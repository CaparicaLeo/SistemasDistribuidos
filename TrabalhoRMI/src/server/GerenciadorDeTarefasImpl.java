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
    public void adicionarTarefa(String descricao) throws RemoteException {
        int id = proximoId.getAndIncrement();
        Tarefa novaTarefa = new Tarefa(id, descricao);
        listaDeTarefas.add(novaTarefa);
        System.out.println("Servidor: Tarefa adicionada -> " + novaTarefa);
    }

    @Override
    public List<Tarefa> listarTarefa() throws RemoteException {
        System.out.println("Servidor: Requisição para listar tarefas recebida.");
        return new ArrayList<>(listaDeTarefas);
    }

    @Override
    public boolean removerTarefa(int id) throws RemoteException {
        boolean removido = listaDeTarefas.removeIf(tarefa -> tarefa.getId() == id);
        if (removido) {
            System.out.println("Servidor: Tarefa com ID " + id + " removida.");
        } else {
            System.out.println("Servidor: Tentativa de remover tarefa com ID " + id + " (não encontrada).");
        }
        return removido;
    }
}
