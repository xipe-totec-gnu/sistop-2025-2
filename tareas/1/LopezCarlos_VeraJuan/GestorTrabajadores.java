import java.util.concurrent.Semaphore;
import java.util.concurrent.atomic.AtomicInteger;

public class GestorTrabajadores {
    // Numero total de trabajadores disponibles
    private static final int NUM_TRABAJADORES = 5;
    // Contador para llevar el control de trabajadores disponibles
    private static final AtomicInteger trabajadoresDispo = new AtomicInteger(NUM_TRABAJADORES);
    // Semaforo para sincronizar el acceso a los trabajadores
    private static final Semaphore semaforo = new Semaphore(0); // Inicialmente en 0, espera solicitudes

    // Clase interna trabajador
    static class Trabajador implements Runnable {
        private final int id; // id del trabajador
        private String paginaProcesada; // Pagina procesada por el trabajador

        public Trabajador(int id) {
            this.id = id;
        }

        @Override
        public void run() {
            while (true) {
                try {
                    // El trabajador espera ser notificado para procesar una solicitud
                    System.out.println("Trabajador " + id + " en espera.");
                    trabajadoresDispo.incrementAndGet(); // Incrementa el contador de trabajadores disponibles
                    semaforo.acquire(); // Espera hasta que el gestor libere una tarea
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt(); // Si es interrumpido termina
                    return;
                }

                // Simula el procesamiento de una pagina aleatoria
                paginaProcesada = "Pagina_" + (int) (Math.random() * 100);
                System.out.println("Trabajador " + id + " procesando: " + paginaProcesada);

                // Finaliza el procesamiento
                System.out.println("Trabajador " + id + " completo: " + paginaProcesada);
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        // Crea y lanza los hilos de los trabajadores
        for (int i = 0; i < NUM_TRABAJADORES; i++) {
            new Thread(new Trabajador(i)).start();
        }

        // Asigna 10 solicitudes de procesamiento
        for (int i = 0; i < 10; i++) {
            Thread.sleep(1000); // Espera 1 segundo entre solicitudes
            if (trabajadoresDispo.get() > 0) {
                semaforo.release(); // Libera un trabajador para procesar la solicitud
                trabajadoresDispo.decrementAndGet(); // Reduce el contador de trabajadores disponibles
                System.out.println("Gestor asigno solicitud " + i);
            } else {
                System.out.println("No hay trabajadores disponibles para solicitud " + i);
            }
        }
    }
}
