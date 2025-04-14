package sistop._20252;

import java.util.Random;

public class Persona {
    private String nombre;
    private Object recurso;
    private boolean prioridad;

    public Persona(String nombre, Object recurso) {
        this.nombre = nombre;
        this.recurso = recurso;
        this.prioridad = new Random().nextBoolean();
    }

    @Override
    public void run() {
        System.out.println(nombre + " tiene prioridad alta? " + prioridad);
        if (recurso instanceof Cubiculo) {
            ((Cubiculo) recurso).usar(nombre, prioridad);
        } else if (recurso instanceof Mesa) {
            ((Mesa) recurso).usar(nombre, prioridad);
        }
    }

    public boolean hasPrioridad() {
        return prioridad;
    }

    public String getNombre() {
        return nombre;
    }


}
