package sistop._20252;
import java.util.concurrent.Semaphore;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.atomic.AtomicInteger;

class Cubiculo {
    private final Semaphore semaforo = new Semaphore(2);
    private final int id;
    private final CyclicBarrier barrier;
    private final AtomicInteger prioridadesEsperando = new AtomicInteger(0);

    public Cubiculo(int id) {
        this.id = id;
        this.barrier = new CyclicBarrier(2, () -> {
            System.out.println("La puerta del cubículo " + id + " se abre. Está completamente ocupado.");
        });
    }

    public void usar(String nombre, boolean prioridad) {
        try {
            System.out.println(nombre + " quiere entrar al cubículo " + id + ". Prioridad: " + prioridad);

            if (prioridad) {
                prioridadesEsperando.incrementAndGet();
            }

            while (!prioridad && prioridadesEsperando.get() > 0) {
                System.out.println(nombre + " espera porque hay personas con prioridad en el cubículo " + id);
                Thread.sleep(3000);
            }

            semaforo.acquire();

            if (prioridad) {
                prioridadesEsperando.decrementAndGet();
            }

            System.out.println(nombre + " está usando el cubículo " + id + ".");
            barrier.await();

            Thread.sleep(3000);
            System.out.println(nombre + " ha salido del cubículo " + id + ".");
            semaforo.release();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
