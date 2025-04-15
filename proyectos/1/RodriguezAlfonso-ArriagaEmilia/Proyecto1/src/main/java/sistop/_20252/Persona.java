package sistop._20252;

import javafx.scene.image.ImageView;

import java.util.Random;
import java.util.concurrent.Semaphore;

class Persona implements Runnable {
    private final String nombre;
    private final Random random = new Random();
    private Object recurso;
    private ImageView currentSeat;

    public Persona(String nombre, Object recursoInicial) {
        this.nombre = nombre;
        this.recurso = recursoInicial;
        this.currentSeat = null;
    }

    @Override
    public void run() {
        while (true) {
            boolean prioridad = random.nextBoolean();
            boolean quiereCubiculo = random.nextBoolean();

            if (quiereCubiculo) {
                recurso = ExecutionController.cubiculos[random.nextInt(ExecutionController.cubiculos.length)];
                ((Cubiculo) recurso).usar(nombre, prioridad, this);
            } else {
                recurso = ExecutionController.mesas[random.nextInt(ExecutionController.mesas.length)];
                ((Mesa) recurso).usar(nombre, prioridad, this);
            }


            boolean seguir = random.nextBoolean();
            if (!seguir) {
                System.out.println(nombre + " ha decidido irse por ahora.");
                try {
                    Thread.sleep(OptionsController.absence);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }


            try {
                Thread.sleep(1000 + random.nextInt(3000));
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public ImageView getCurrentSeat() {
        return currentSeat;
    }

    public void setCurrentSeat(ImageView currentSeat) {
        this.currentSeat = currentSeat;
    }
}