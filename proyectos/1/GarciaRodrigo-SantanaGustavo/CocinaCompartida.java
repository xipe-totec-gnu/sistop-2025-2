import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Semaphore;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.Random;
import java.util.List;
import java.util.Collections;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.concurrent.TimeUnit;            


public class CocinaCompartida {

    // Recursos compartidos de la cocina (con acceso limitado o exclusivo)
    private static final Semaphore estufa = new Semaphore(4);
    private static final Semaphore sarten = new Semaphore(2);
    private static final Semaphore olla = new Semaphore(2);
    private static final Lock tostador = new ReentrantLock();
    private static final Lock microondas = new ReentrantLock();
    private static final Lock licuadora = new ReentrantLock();
    private static final Lock lavaplatos = new ReentrantLock();

    /**
     * Representa a un compañero de cuarto que ejecuta una rutina de cocina de forma concurrente.
     */
    static class Roomie implements Runnable {
        private final String nombre;
        private final Random rand = new Random();
        private final List<String> rutina;

        public Roomie(String nombre) {
            this.nombre = nombre;
            this.rutina = generarRutina();
        }

        /**
         * Genera una rutina aleatoria de cocina para el Roomie.
         * La rutina siempre incluye:
         * - preparación (inicio)
         * - cocinar (obligatorio)
         * - entre 1 y 3 tareas adicionales aleatorias
         * - lavar (final obligatorio)
         */
        private List<String> generarRutina() {
            List<String> acciones = new ArrayList<>();
            acciones.add("preparar");
            acciones.add("cocinar");

            List<String> extras = new ArrayList<>(Arrays.asList("microondas", "licuadora", "tostar"));
            Collections.shuffle(extras);
            int numExtras = rand.nextInt(3) + 1;

            for (int i = 0; i < numExtras; i++) {
                acciones.add(extras.get(i));
            }

            acciones.add("lavar");
            return acciones;
        }

        @Override
        public void run() {
            try {    
                for (String accion : rutina) {
                    Thread.sleep(rand.nextInt(2000) + 1000); // Simula espera entre pasos
                    switch (accion) {
                        case "preparar":
                            prepararIngredientes();
                            break;
                        case "cocinar":
                            cocinar();
                            break;
                        case "microondas":
                            usarMicroondas();
                            break;
                        case "licuadora":
                            usarLicuadora();
                            break;
                        case "tostar":
                            usarTostador();
                            break;
                        case "lavar":
                            lavarUtensilios();
                            break;
                    }
                }
                logEvento("comiendo", this.nombre, "comer");
            } catch (InterruptedException e) {
                System.out.println(this.nombre + " fue interrumpido.");
            }
        }

        /**
         * Simula la preparación de ingredientes sin sincronización.
         */
        private void prepararIngredientes() throws InterruptedException {
            int preparacion = rand.nextInt(3000) + 1000;
            logEvento("activo", this.nombre, "preparar");
            Thread.sleep(preparacion);
        }
        
        /**
         * Simula la acción de cocinar usando olla o sartén, ambos requieren estufa.
         */
        private void cocinar() throws InterruptedException {
            int traste = rand.nextInt(2);
            int coccion = rand.nextInt(7000) + 3000;
            switch (traste) {
                case 0: {
                    int olla_gorda = rand.nextInt(5000) + 1000;
                    logEvento("esperando", this.nombre, "cocinar-olla");
                    olla.acquire();
                    estufa.acquire(2);
                    try {
                        logEvento("activo", this.nombre, "cocinar-olla");
                        Thread.sleep(coccion + olla_gorda);
                    } finally {
                        olla.release();
                        estufa.release(2);
                        logEvento("terminado", this.nombre, "cocinar-olla");
                    }
                    break;
                }
                case 1: {
                    logEvento("esperando", this.nombre, "cocinar-sarten");
                    sarten.acquire();
                    estufa.acquire();
                    try {
                        logEvento("activo", this.nombre, "cocinar-sarten");
                        Thread.sleep(coccion);
                    } finally {
                        sarten.release();
                        estufa.release();
                        logEvento("terminado", this.nombre, "cocinar-sarten");
                    }
                    break;
                }
            }
        }

        /**
         * Simula el uso exclusivo del microondas.
         */
        private void usarMicroondas() throws InterruptedException {
            int microondeando = rand.nextInt(4000) + 2000;
            logEvento("esperando", this.nombre, "microondas");
            microondas.lock();
            try {
                logEvento("activo", this.nombre, "microondas");
                Thread.sleep(microondeando);
            } finally {
                microondas.unlock();
                logEvento("terminado", this.nombre, "microondas");
            }
        }

        /**
         * Simula el uso exclusivo de la licuadora.
         */
        private void usarLicuadora() throws InterruptedException {
            int licuando = rand.nextInt(3000) + 1500;
            logEvento("esperando", this.nombre, "licuadora");
            licuadora.lock();
            try {
                logEvento("activo", this.nombre, "licuadora");
                Thread.sleep(licuando);
            } finally {
                licuadora.unlock();
                logEvento("terminado", this.nombre, "licuadora");
            }
        }

        /**
         * Simula el uso exclusivo del tostador.
         */
        private void usarTostador() throws InterruptedException {
            int tostando = rand.nextInt(4000) + 2000;
            logEvento("esperando", this.nombre, "tostar");
            tostador.lock();
            try {
                logEvento("activo", this.nombre, "tostar");
                Thread.sleep(tostando);
            } finally {
                tostador.unlock();
                logEvento("terminado", this.nombre, "tostar");
            }
        }

        /**
         * Simula el uso del lavaplatos al final de la rutina.
         */
        private void lavarUtensilios() throws InterruptedException {
            int lavando = rand.nextInt(6000) + 4000;
            logEvento("esperando", this.nombre, "lavar");
            lavaplatos.lock();
            try {
                logEvento("activo", this.nombre, "lavar");
                Thread.sleep(lavando);
            } finally {
                lavaplatos.unlock();
                logEvento("terminado", this.nombre, "lavar");
            }
        }

        /**
         * Registra un evento de la rutina con un estado y acción específica.
         */
        private void logEvento(String estado, String nombre, String accion) {
            System.out.println(estado + ";" + nombre + ";" + accion);
        }

    }

    /**
     * Método principal que lanza la simulación con varios roomies ejecutándose de forma concurrente.
     */
    public static void main(String[] args) {
        String[] nombres = {"Santan", "Roy", "Moi", "Yayo", "Paco", "Mau"};
        ExecutorService executor = Executors.newFixedThreadPool(nombres.length);

        for (String nombre : nombres) {
            executor.execute(new Roomie(nombre));
        }

        executor.shutdown();
        try {
            executor.awaitTermination(2, TimeUnit.MINUTES);
        } catch (InterruptedException e) {
            System.out.println("La cocina fue interrumpida.");
        }

    }
}


