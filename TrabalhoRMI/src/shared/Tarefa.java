package shared;

import java.io.Serializable;

public class Tarefa implements Serializable {
    private static final long serialVersionUID = 1L;

    private int id;
    private String descricao;

    public Tarefa(int id, String descricao) {
        this.id = id;
        this.descricao = descricao;
    }

    public int getId(){
        return this.id;
    }
    public String getDescricao(){
        return this.descricao;
    }

    @Override
    public String toString(){
        return "Tarefa [ID: "+  id + ", Descrição: "+ descricao + "]";
    }
}
