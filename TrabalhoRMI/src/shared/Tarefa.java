package shared;

import java.io.Serializable;

public class Tarefa implements Serializable {
    private static final long serialVersionUID = 1L;

    private int id;
    private String descricao;
    private String usuario;

    public Tarefa(int id, String descricao, String usuario) {
        this.id = id;
        this.descricao = descricao;
        this.usuario = usuario;
    }

    public int getId(){
        return this.id;
    }
    public String getDescricao(){
        return this.descricao;
    }
    public String getUsuario(){
        return this.usuario;
    }

    @Override
    public String toString() {
        return "ID: " + id + " | Usuário: " + usuario + " | Tarefa: " + descricao;
    }
}
