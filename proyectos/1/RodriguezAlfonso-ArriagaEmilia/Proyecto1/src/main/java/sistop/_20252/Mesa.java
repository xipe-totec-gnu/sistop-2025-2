package sistop._20252;

import java.util.Random;
import java.util.Scanner;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Semaphore;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.atomic.AtomicInteger;

class Mesa {
    private final Semaphore semaforo = new Semaphore(3);
    private final int id;

    public Mesa(int id) {
        this.id = id;
    }

    public void usar(String nombre, boolean prioridad) {
        try {
            System.out.println(nombre + " quiere entrar a la mesa " + id + ". Prioridad: " + prioridad);
            semaforo.acquire();
            System.out.println(nombre + " está usando la mesa " + id + ".");
            Thread.sleep(1000);
            System.out.println(nombre + " ha salido de la mesa " + id + ".");
            semaforo.release();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
