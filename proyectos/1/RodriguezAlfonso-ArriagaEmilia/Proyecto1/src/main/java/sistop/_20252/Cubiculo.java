package sistop._20252;
import javafx.application.Platform;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;

import java.util.concurrent.Semaphore;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.atomic.AtomicInteger;

class Cubiculo {
    private final Semaphore semaforo = new Semaphore(2);
    private final int id;
    private final CyclicBarrier barrier;
    private final AtomicInteger prioridadesEsperando = new AtomicInteger(0);
    private ImageView seat1, seat2;

    public Cubiculo(int id, ImageView seat1, ImageView seat2) {
        this.id = id;
        this.barrier = new CyclicBarrier(2, () -> {
            System.out.println("La puerta del cubículo " + id + " se abre. Está completamente ocupado.");
        });
        this.seat1 = seat1;
        this.seat2 = seat2;
    }

    public void usar(String nombre, boolean prioridad, Persona person) {
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
            findAvailable(person);

            if (prioridad) {
                prioridadesEsperando.decrementAndGet();
            }

            System.out.println(nombre + " está usando el cubículo " + id + ".");
            barrier.await();

            Thread.sleep(3000);
            System.out.println(nombre + " ha salido del cubículo " + id + ".");
            semaforo.release();
            releaseSeat(person);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void findAvailable(Persona person){
        Platform.runLater(() -> {
            if(getSeat1().getImage() == null){
                getSeat1().setImage(new Image(getClass().getResource("/images/RED_LIGHT.png").toExternalForm()));
                person.setCurrentSeat(getSeat1());
            } else if(getSeat2().getImage() == null){;
                getSeat2().setImage(new Image(getClass().getResource("/images/RED_LIGHT.png").toExternalForm()));
                person.setCurrentSeat(getSeat2());
            }
        });

    }

    public void releaseSeat(Persona person){
        Platform.runLater(() -> {
            person.getCurrentSeat().setImage(null);
        });
    }

    public ImageView getSeat1() {
        return seat1;
    }

    public void setSeat1(ImageView seat1) {
        this.seat1 = seat1;
    }

    public ImageView getSeat2() {
        return seat2;
    }

    public void setSeat2(ImageView seat2) {
        this.seat2 = seat2;
    }
}
