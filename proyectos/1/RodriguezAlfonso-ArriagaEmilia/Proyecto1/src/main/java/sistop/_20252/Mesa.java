package sistop._20252;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;

import java.util.concurrent.Semaphore;

class Mesa {
    // Definimos el semáforo que permitirá acceso a la concurrencia.
    private final Semaphore semaforo = new Semaphore(3);
    private final int id;
    // Definimos los elementos visuales que le competen a nuestra mesa.
    private ImageView seat1, seat2, seat3;
    private final String tableColour;
    private Label tableInfo;

    // Constructor de cada mesa.
    public Mesa(int id, String tableColour, ImageView seat1, ImageView seat2, ImageView seat3, Label tableInfo) {
        this.id = id;
        this.seat1 = seat1;
        this.seat2 = seat2;
        this.seat3 = seat3;
        this.tableColour = tableColour;
        this.tableInfo = tableInfo;
    }

    // Uso de las mesas por las usuarias de la Santuaria.
    public void usar(String nombre, boolean prioridad, Persona person) {
        try {
            // Según sea necesario, iremos adquiriendo y soltando los asientos.
            Platform.runLater(() -> tableInfo.setText(nombre + " quiere entrar a la mesa " + id + ". Prioridad: " + prioridad));
            semaforo.acquire();
            // Encontramos una silla disponible para quien se quiere sentar.
            findAvailable(person);
            Platform.runLater(() -> tableInfo.setText(nombre + " está usando la mesa " + id + "."));
            // Esperamos a que se use la mesa.
            Thread.sleep(ExecutionController.randomizer.nextInt(OptionsController.minTime, OptionsController.maxTime));
            Platform.runLater(() -> tableInfo.setText(nombre + " ha salido de la mesa " + id + "."));
            semaforo.release();
            releaseSeat(person);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void findAvailable(Persona person){
        Platform.runLater(() -> {
            if(getSeat1().getImage() == null){
                getSeat1().setImage(new Image(getClass().getResource("/images/" + this.tableColour + "_LIGHT.png").toExternalForm()));
                person.setCurrentSeat(getSeat1());
            } else if(getSeat2().getImage() == null){;
                getSeat2().setImage(new Image(getClass().getResource("/images/" + this.tableColour + "_LIGHT.png").toExternalForm()));
                person.setCurrentSeat(getSeat2());
            } else if(getSeat3().getImage() == null){
                getSeat3().setImage(new Image(getClass().getResource("/images/" + this.tableColour + "_LIGHT.png").toExternalForm()));
                person.setCurrentSeat(getSeat3());
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

    public ImageView getSeat2() {
        return seat2;
    }

    public ImageView getSeat3() {
        return seat3;
    }

    public void setSeat1(ImageView seat1) {
        this.seat1 = seat1;
    }

    public void setSeat2(ImageView seat2) {
        this.seat2 = seat2;
    }

    public void setSeat3(ImageView seat3) {
        this.seat3 = seat3;
    }


}
