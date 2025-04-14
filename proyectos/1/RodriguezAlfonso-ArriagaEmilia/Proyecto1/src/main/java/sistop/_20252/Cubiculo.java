package sistop._20252;

public class Cubiculo {
    boolean estaOcupado = false;
    int lugaresDisponibles = 2;

    public synchronized void usar(String nombre, boolean prioridad) {
        if (!estaOcupado && lugaresDisponibles > 0) {
            System.out.println(nombre + " (prioridad: " + prioridad + ") está usando el cubículo.");
            lugaresDisponibles--;
            estaOcupado = true;
        } else {
            System.out.println(nombre + " (prioridad: " + prioridad + ") no pudo usar el cubículo.");
        }
    }
}
