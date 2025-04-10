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

    // Recursos compartidos
    private static final Semaphore estufa = new Semaphore(4); // 4 quemadores
    private static final Semaphore sarten = new Semaphore(2); // 2 sartenes
    private static final Semaphore olla = new Semaphore(2); // 2 ollas gordas jajaja
    private static final Lock tostador = new ReentrantLock();
    private static final Lock microondas = new ReentrantLock();
    private static final Lock licuadora = new ReentrantLock();
    private static final Lock lavaplatos = new ReentrantLock();


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
            List<String> extras = new ArrayList<>(Arrays.asList("microondas", "licuadora", "tostar"));
            Collections.shuffle(extras);
            int numExtras = rand.nextInt(3) + 1; // 1 o 2

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
                        case "tostar":
                        usarTostador();
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
            int preparacion = rand.nextInt(3000) + 1000;
            log("está preparando ingredientes...");
            Thread.sleep(preparacion);
        }

        private void cocinar() throws InterruptedException {
            int traste = rand.nextInt(2);
            int coccion = rand.nextInt(7000)+ 3000;
            switch (traste){
                case 0: {
                    int olla_gorda = rand.nextInt(5000)+ 1000;
                    log("quiere usar la estufa y una olla gorda.");

                    olla.acquire();
                    log("obtuvo una olla gorda.");

                    estufa.acquire(2);
                    log("obtuvo un quemador y tapó otro de la estufa.");

                    try {
                        log("está cocinando con la olla...");
                        Thread.sleep(coccion + olla_gorda);
                    } finally {
                        olla.release();
                        estufa.release(2);
                        log("liberó la estufa y la olla.");
                    }
                    break;
                }
                case 1: {
                    log("quiere usar la estufa y el sartén.");

                    sarten.acquire();
                    log("obtuvo un sartén.");

                    estufa.acquire();
                    log("obtuvo un quemador de la estufa.");
                    try {
                        log("está cocinando con el sartén...");
                        Thread.sleep(coccion);
                    } finally {
                        sarten.release();
                        estufa.release();
                        log("liberó la estufa y el sartén.");
                    }
                    break;
                }
            }
        }

        private void usarMicroondas() throws InterruptedException {
            log("quiere usar el microondas.");
            microondas.lock();
            int microondeando = rand.nextInt(4000)+ 2000;
            try {
                log("está usando el microondas...");
                Thread.sleep(microondeando);
            } finally {
                microondas.unlock();
                log("terminó con el microondas.");
            }
        }

        private void usarLicuadora() throws InterruptedException {
            log("quiere usar la licuadora.");
            licuadora.lock();
            int licuando = rand.nextInt(3000) + 1500;
            try {
                log("está usando la licuadora...");
                Thread.sleep(licuando);
            } finally {
                licuadora.unlock();
                log("terminó con la licuadora.");
            }
        }

        private void usarTostador() throws InterruptedException {
            log("quiere usar el tostador");
            tostador.lock();
            int tostando = rand.nextInt(4000) + 2000;
            try {
                log("está usando el tostador...");
                Thread.sleep(tostando);
            } finally {
                tostador.unlock();
                log("terminó con el tostador.");
            }
        }

        private void lavarUtensilios() throws InterruptedException {
            log("quiere usar el lavaplatos.");
            lavaplatos.lock();
            int lavando = rand.nextInt(6000) + 4000;
            try {
                log("está lavando los utensilios...");
                Thread.sleep(lavando);
            } finally {
                lavaplatos.unlock();
                log("terminó de lavar los utensilios.");
            }
        }

        private void log(String mensaje) {
            String entrada = "[" + nombre + "] " + mensaje;
            System.out.println(entrada);
        }
    }

    public static void main(String[] args) {
        String[] nombres = {"Santan", "Roy", "Moi","Yayo","Paco","Mau"};
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







