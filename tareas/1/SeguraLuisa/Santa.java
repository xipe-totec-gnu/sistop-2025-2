// Segura Cedeño Luisa María
// Implementación del prblema de Santa Claus

import java.util.concurrent.*;
import java.util.concurrent.locks.*;
import java.util.Random;

public class Santa {
    private static final int TOTAL_ELFOS = 10; 
    private static final int TOTAL_RENOS = 9;  

    // Contadores compartidos
    private static int problemasElfos = 0;
    private static int renosRegresados = 0;   

    private static final Lock mutex = new ReentrantLock();
    private static final Condition condicionSanta = mutex.newCondition();
    private static final Semaphore semaforoElfos = new Semaphore(0);
    private static final Semaphore semaforoRenos = new Semaphore(0);

    public static void main(String[] args) {
        Thread santa = new Thread(Santa::santa);
        santa.start();

        for (int i = 0; i < TOTAL_ELFOS; i++) {
            new Thread(() -> elfo(Thread.currentThread().getId())).start();
        }

        for (int i = 0; i < TOTAL_RENOS; i++) {
            new Thread(Santa::reno).start();
        }
    }

    private static void santa() {
        while (true) {
            try {
                mutex.lock();
                // Santa duerme mientras no se cumpla ninguna condición de despertar
                while (problemasElfos < 3 && renosRegresados < TOTAL_RENOS) {
                    condicionSanta.await();
                }

                // Si todos los renos han regresado, se inicia el reparto de regalos
                if (renosRegresados == TOTAL_RENOS) {
                    System.out.println("\n--- Santa Claus: ¡Es hora de repartir regalos! ---");
                    for (int i = 0; i < TOTAL_RENOS; i++) {
                        semaforoRenos.release();
                    }
                    renosRegresados = 0;
                } 
                // Si hay al menos 3 elfos con problemas, se les presta ayuda
                else if (problemasElfos >= 3) {
                    System.out.println("\n--- Santa Claus: Ayudando a 3 elfos con problemas ---");
                    for (int i = 0; i < 3; i++) {
                        semaforoElfos.release();
                    }
                    problemasElfos -= 3;
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                System.out.println("Santa interrumpido.");
            } finally {
                mutex.unlock();
            }
        }
    }

    private static void elfo(long id) {
        Random random = new Random();
        while (true) {
            try {
                // El elfo trabaja un tiempo aleatorio
                Thread.sleep(random.nextInt(5000)); 
                // Con cierta probabilidad, el elfo tiene un problema
                if (random.nextDouble() < 0.3) {   
                    mutex.lock();
                    try {
                        problemasElfos++;
                        System.out.println("Elfo " + id + ": Tengo un problema. Total: " + problemasElfos);
                        if (problemasElfos == 3) {
                            // Despertar a Santa si se acumulan 3 elfos con problemas
                            condicionSanta.signal();
                        }
                    } finally {
                        mutex.unlock();
                    }

                    // El elfo espera a recibir ayuda de Santa
                    semaforoElfos.acquire();
                    System.out.println("Elfo " + id + ": Recibí ayuda de Santa.");
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                System.out.println("Elfo " + id + " interrumpido.");
            }
        }
    }

    private static void reno() {
        Random random = new Random();
        try {
            // El reno disfruta de sus vacaciones
            Thread.sleep(random.nextInt(10000)); 
            mutex.lock();
            try {
                renosRegresados++;
                System.out.println("Reno: He regresado. Total: " + renosRegresados);
                if (renosRegresados == TOTAL_RENOS) {
                    // Si todos los renos han regresado, se despierta a Santa
                    condicionSanta.signal();
                }
            } finally {
                mutex.unlock();
            }

            // El reno espera ser enganchado al trineo
            semaforoRenos.acquire();
            System.out.println("Reno: Estoy enganchado al trineo.");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.out.println("Reno interrumpido.");
        }
    }
}
