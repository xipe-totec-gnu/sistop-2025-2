package sistop._20252;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;

import java.util.concurrent.Semaphore;

class Mesa {
    private final Semaphore semaforo = new Semaphore(3);
    private final int id;
    private ImageView seat1, seat2, seat3;
    private final String tableColour;


    public Mesa(int id, String tableColour, ImageView seat1, ImageView seat2, ImageView seat3) {
        this.id = id;
        this.seat1 = seat1;
        this.seat2 = seat2;
        this.seat3 = seat3;
        this.tableColour = tableColour;
    }

    public void usar(String nombre, boolean prioridad, Persona person) {
        try {
            System.out.println(nombre + " quiere entrar a la mesa " + id + ". Prioridad: " + prioridad);
            semaforo.acquire();
            findAvailable(person);
            System.out.println(nombre + " está usando la mesa " + id + ".");
            Thread.sleep(1000);
            System.out.println(nombre + " ha salido de la mesa " + id + ".");
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
