package sistop._20252;

public class Mesa {
    boolean estaOcupado = false;
    int lugaresDisponibles = 3;

    public synchronized void usar(String nombre, boolean prioridad) {
        if (!estaOcupado && lugaresDisponibles > 0) {
            System.out.println(nombre + " (prioridad: " + prioridad + ") está usando la mesa.");
            lugaresDisponibles--;
            estaOcupado = true;
        } else {
            System.out.println(nombre + " (prioridad: " + prioridad + ") no pudo usar la mesa.");
        }
    }
}
