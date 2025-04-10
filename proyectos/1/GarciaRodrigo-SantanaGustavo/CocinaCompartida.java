import java.util.concurrent.*;              // Para ExecutorService, Executors, Semaphore
import java.util.concurrent.locks.*;        // Para Lock y ReentrantLock
import java.util.*;                         // Para Random, List, etc.

public class CocinaCompartida {

    // Recursos compartidos
    private static final Semaphore estufa = new Semaphore(4); // 4 quemadores
    private static final Lock sarten = new ReentrantLock();
    private static final Lock microondas = new ReentrantLock();
    private static final Lock licuadora = new ReentrantLock();
    private static final Lock lavaplatos = new ReentrantLock();

    // Log centralizado
    private static final List<String> logDeCocina = Collections.synchronizedList(new ArrayList<>());

    static class Roomie implements Runnable {
        private final String nombre;
        private final Random rand = new Random();
        private final List<String> rutina;

        public Roomie(String nombre) {
            this.nombre = nombre;
            this.rutina = generarRutina();
        }

        private List<String> generarRutina() {
            List<String> acciones = new ArrayList<>();

            // Paso obligatorio
            acciones.add("preparar");
            acciones.add("cocinar");

            // Extras aleatorios
            List<String> extras = new ArrayList<>(Arrays.asList("microondas", "licuadora"));
            Collections.shuffle(extras);
            int numExtras = rand.nextInt(2) + 1; // 1 o 2

            for (int i = 0; i < numExtras; i++) {
                acciones.add(extras.get(i));
            }

            // Paso final obligatorio
            acciones.add("lavar");

            return acciones;
        }

        @Override
        public void run() {
            try {
                log("Iniciando rutina...");
                for (String accion : rutina) {
                    Thread.sleep(rand.nextInt(2000) + 1000);
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
                        case "lavar":
                            lavarUtensilios();
                            break;
                    }
                }
                log("Terminó toda la rutina.\n");
            } catch (InterruptedException e) {
                log("Fue interrumpido.");
            }
        }

        private void prepararIngredientes() throws InterruptedException {
            log("está preparando ingredientes...");
            Thread.sleep(rand.nextInt(1000) + 500);
        }

        private void cocinar() throws InterruptedException {
            log("quiere usar la estufa y el sartén.");

            estufa.acquire();
            log("obtuvo un quemador de la estufa.");

            sarten.lock();
            try {
                log("está cocinando con el sartén...");
                Thread.sleep(rand.nextInt(1000) + 1000);
            } finally {
                sarten.unlock();
                estufa.release();
                log("liberó la estufa y el sartén.");
            }
        }

        private void usarMicroondas() throws InterruptedException {
            log("quiere usar el microondas.");
            microondas.lock();
            try {
                log("está usando el microondas...");
                Thread.sleep(rand.nextInt(1000) + 500);
            } finally {
                microondas.unlock();
                log("terminó con el microondas.");
            }
        }

        private void usarLicuadora() throws InterruptedException {
            log("quiere usar la licuadora.");
            licuadora.lock();
            try {
                log("está usando la licuadora...");
                Thread.sleep(rand.nextInt(1000) + 500);
            } finally {
                licuadora.unlock();
                log("terminó con la licuadora.");
            }
        }

        private void lavarUtensilios() throws InterruptedException {
            log("quiere usar el lavaplatos.");
            lavaplatos.lock();
            try {
                log("está lavando los utensilios...");
                Thread.sleep(rand.nextInt(1000) + 500);
            } finally {
                lavaplatos.unlock();
                log("terminó de lavar los utensilios.");
            }
        }

        private void log(String mensaje) {
            String entrada = "[" + nombre + "] " + mensaje;
            logDeCocina.add(entrada);
            System.out.println(entrada);
        }
    }

    public static void main(String[] args) {
        String[] nombres = {"Santan", "Roy", "Moi"};
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

        System.out.println("\n=== LOG FINAL DE LA COCINA ===");
        for (String linea : logDeCocina) {
            System.out.println(linea);
        }
    }
}






