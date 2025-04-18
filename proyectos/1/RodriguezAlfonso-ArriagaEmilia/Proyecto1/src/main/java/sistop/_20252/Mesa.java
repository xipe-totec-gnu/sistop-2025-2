// Autores: Emilia Macarena y Alfonso D'Hernán

package sistop._20252;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;

import java.util.concurrent.Semaphore;

// Comenzamos por definir cada clase que será recurso compartido y por cada lugar (3 en caso de la mesa) se creará un semáforo, con la intencion de implementar un apagador.


class Mesa {
    private final Semaphore semaforo = new Semaphore(3);
    private final int id;
    private ImageView seat1, seat2, seat3;
    private final String tableColour;
    private Label tableInfo;


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
            //El estado del semáforo  cambia respecto a quién ingresa a su recurso.
            Platform.runLater(() -> tableInfo.setText(nombre + " quiere entrar a la mesa " + id + ". Prioridad: " + prioridad));
            semaforo.acquire();
            // Encontramos una silla disponible para quien se quiere sentar.
            findAvailable(person);
            Platform.runLater(() -> tableInfo.setText(nombre + " está usando la mesa " + id + "."));
            // Esperamos a que se use la mesa.
            //Se duerme para simular el uso.
            Thread.sleep(ExecutionController.randomizer.nextInt(OptionsController.minTime, OptionsController.maxTime));
            Platform.runLater(() -> tableInfo.setText(nombre + " ha salido de la mesa " + id + "."));
            // Quitamos el semáforo.
            semaforo.release();
            // Liberamos el asiento.
            releaseSeat(person);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    // Función que encuentra un asiento disponible para cierta persona.
    public void findAvailable(Persona person){
        Platform.runLater(() -> {
            // Va asiento por asiento cersiorándose de que haya un asiento disponible.
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

    // Suelta el asiento para indicar que ya se desocupó.
    public void releaseSeat(Persona person){
        Platform.runLater(() -> {
            person.getCurrentSeat().setImage(null);
        });
    }

    // Getters y setters.

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
