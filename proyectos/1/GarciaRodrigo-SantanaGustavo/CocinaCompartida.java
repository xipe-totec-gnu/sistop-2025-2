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
    private static final Semaphore olla = new Semaphore(2); // 2 ollas
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
            int numExtras = rand.nextInt(3) + 1;

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
                logEvento("comiendo",this.nombre,"comer");
            } catch (InterruptedException e) {
                System.out.println("Fue interrumpido.");
            }
        }

        private void prepararIngredientes() throws InterruptedException {
            int preparacion = rand.nextInt(3000) + 1000;
            logEvento("activo",this.nombre,"preparar");
            Thread.sleep(preparacion);
        }

        private void cocinar() throws InterruptedException {
            int traste = rand.nextInt(2);
            int coccion = rand.nextInt(7000) + 3000;
            switch (traste){
                case 0: {
                    int olla_gorda = rand.nextInt(5000) + 1000;
                    logEvento("esperando",this.nombre,"cocinar-olla");
                    olla.acquire();
                    estufa.acquire(2);
                    try {
                        logEvento("activo",this.nombre,"cocinar-olla");
                        Thread.sleep(coccion + olla_gorda);
                    } finally {
                        olla.release();
                        estufa.release(2);
                        logEvento("terminado",this.nombre,"cocinar-olla");
                    }
                    break;
                }
                case 1: {
                    logEvento("esperando",this.nombre,"cocinar-sarten");
                    sarten.acquire();
                    estufa.acquire();
                    try {
                        logEvento("activo",this.nombre,"cocinar-sarten");
                        Thread.sleep(coccion);
                    } finally {
                        sarten.release();
                        estufa.release();
                        logEvento("terminado",this.nombre,"cocinar-sarten");
                    }
                    break;
                }
            }
        }

        private void usarMicroondas() throws InterruptedException {
            logEvento("esperando",this.nombre,"microondas");
            microondas.lock();
            int microondeando = rand.nextInt(4000) + 2000;
            try {
                logEvento("activo",this.nombre,"microondas");
                Thread.sleep(microondeando);
            } finally {
                microondas.unlock();
                logEvento("terminado",this.nombre,"microondas");
            }
        }

        private void usarLicuadora() throws InterruptedException {
            logEvento("esperando",this.nombre,"licuadora");
            licuadora.lock();
            int licuando = rand.nextInt(3000) + 1500;
            try {
                logEvento("activo",this.nombre,"licuadora");
                Thread.sleep(licuando);
            } finally {
                licuadora.unlock();
                logEvento("terminado",this.nombre,"licuadora");
            }
        }

        private void usarTostador() throws InterruptedException {
            logEvento("esperando",this.nombre,"tostar");
            tostador.lock();
            int tostando = rand.nextInt(4000) + 2000;
            try {
                logEvento("activo",this.nombre,"tostar");
                Thread.sleep(tostando);
            } finally {
                tostador.unlock();
                logEvento("terminado",this.nombre,"tostar");
            }
        }

        private void lavarUtensilios() throws InterruptedException {
            logEvento("esperando",this.nombre,"lavar");
            lavaplatos.lock();
            int lavando = rand.nextInt(6000) + 4000;
            try {
                logEvento("activo",this.nombre,"lavar");
                Thread.sleep(lavando);
            } finally {
                lavaplatos.unlock();
                logEvento("terminado",this.nombre,"lavar");
            }
        }

        private void logEvento(String estado, String nombre, String accion) {
            System.out.println(estado + ";" + nombre + ";" + accion);
        }

    }

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




