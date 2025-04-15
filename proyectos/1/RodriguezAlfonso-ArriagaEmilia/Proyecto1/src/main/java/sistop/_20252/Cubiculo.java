// Autores: Emilia Macarena y Alfonso D'Hernán

package sistop._20252;
import javafx.application.Platform;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;

import java.util.concurrent.Semaphore;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.atomic.AtomicInteger;

// Comenzamos por definir cada clase que será recurso compartido y por cada lugar (2 en caso del cubículo) se creará un semáforo, con la intencion de implementar un apagador.


class Cubiculo {
    private final Semaphore semaforo = new Semaphore(2);
    private final int id;
    private final CyclicBarrier barrier;
    private final AtomicInteger prioridadesEsperando = new AtomicInteger(0);
    private ImageView seat1, seat2;
    private Label cubicleInfo;

    public Cubiculo(int id, ImageView seat1, ImageView seat2, Label cubicleInfo) {
         //Para poder reflejar que al llenarse el cubículo se debe de mantener la puerta de éste abierta, se implementó una barrera que se abrirá en el momento en que 2 hilos accedan al mismo recurso (el cubículo).

        this.id = id;
        this.barrier = new CyclicBarrier(2, () -> {
            Platform.runLater(() -> cubicleInfo.setText("La puerta del cubículo " + id + " se abre. Está completamente ocupado."));
        });
        this.seat1 = seat1;
        this.seat2 = seat2;
        this.cubicleInfo = cubicleInfo;
    }

    public void usar(String nombre, boolean prioridad, Persona person) {
        try {
            Platform.runLater(() -> cubicleInfo.setText(nombre + " quiere entrar al cubículo " + id + ". Prioridad: " + prioridad));
//Para poder respetar la prioridad existente dentro de los cubículos se manejaron diversos condicionales y con ayuda de Atomic Integer, donde en caso de sea true y esté en espera de un cubículo, entrará primero.

            if (prioridad) {
                prioridadesEsperando.incrementAndGet();
            }

            if(!prioridad && prioridadesEsperando.get() > 0){
                Platform.runLater(() -> cubicleInfo.setText(nombre + " espera porque hay personas con prioridad en el cubículo " + id));
            }

            while (!prioridad && prioridadesEsperando.get() > 0) {
                Thread.sleep(ExecutionController.randomizer.nextInt(OptionsController.minTime, OptionsController.maxTime));
            }

            semaforo.acquire();
            findAvailable(person);

            if (prioridad) {
                prioridadesEsperando.decrementAndGet();
            }

            Platform.runLater(() -> cubicleInfo.setText(nombre + " está usando el cubículo " + id + "."));
            barrier.await();

            Thread.sleep(ExecutionController.randomizer.nextInt(OptionsController.minTime, OptionsController.maxTime));
            Platform.runLater(() -> cubicleInfo.setText(nombre + " ha salido del cubículo " + id + "."));
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
