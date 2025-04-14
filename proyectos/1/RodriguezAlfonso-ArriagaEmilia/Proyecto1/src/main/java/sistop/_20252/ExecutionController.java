package sistop._20252;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.stage.Stage;

import java.io.IOException;

import java.util.Random;
import java.util.Scanner;
import java.util.concurrent.CountDownLatch;

public class ExecutionController {
    FXMLLoader fxmlLoader;

    public static final String[] tableColours = {"PINK", "BLUE", "YELLOW"};
    public static Mesa[] mesas;
    public static Cubiculo[] cubiculos;
    public static final int cantidadPersonas = 20;
    // Control de sincronización
    public static CountDownLatch latch = new CountDownLatch(cantidadPersonas);
    public static volatile boolean continuar = true;

    @FXML
    public ImageView t1S1, t1S2, t1S3, t2S1, t2S2, t2S3, t3S1, t3S2, t3S3;
    @FXML
    public ImageView c1S1, c1S2, c2S1, c2S2;

    // Método para regresar al menú principal, de ser necesario.
    // Por el momento, no parece poder ser utilizado con la tecla de escape.
    // Todo: Cambiar el layout de la escena para permitir la existencia de botones.
    @FXML
    public void backToMainMenu(KeyEvent event) throws IOException {
        // Si la tecla presionada es escape:
        if(event.getCode() == KeyCode.ESCAPE){
            // Carga de archivo FXML de la escena principal.
            fxmlLoader = new FXMLLoader(ProjectStart.class.getResource("projectStart.fxml"));
            // Se define el objeto Stage
            Stage stage = (Stage)((Node)event.getSource()).getScene().getWindow();
            // Se define la escena con base en el cargador.
            Scene scene = new Scene(fxmlLoader.load());
            // Se pone el título del stage.
            stage.setTitle("Proyecto 1 de concurrencia");
            // Se pone la escena cargada.
            stage.setScene(scene);
            // Mostramos la escena.
            stage.show();
        } else System.out.println("???");
    }

    // Función para ejecutar procesos una vez que se haya presionado el botón correspondiente.
    @FXML
    public void initialize() {
        mesas = new Mesa[3];
        cubiculos = new Cubiculo[2];

        ImageView[][] tableSeats = {{t1S1, t1S2, t1S3},{t2S1, t2S2, t2S3},{t3S1, t3S2, t3S3}};
        ImageView[][] cubicleSeats = {{c1S1, c1S2},{c2S1, c2S2}};

        for (int i = 0; i < mesas.length; i++) {
            mesas[i] = new Mesa(i + 1, tableColours[i], tableSeats[i][0], tableSeats[i][1], tableSeats[i][2]);
        }

        for (int i = 0; i < cubiculos.length; i++) {
            cubiculos[i] = new Cubiculo(i + 1, cubicleSeats[i][0], cubicleSeats[i][1]);
        }

        String[] nombresFemeninos = {
                "Ana", "Luisa", "Sofía", "Camila", "Valeria", "Mariana",
                "Fernanda", "Isabella", "Daniela", "Gabriela", "Renata", "Andrea"
        };

        Platform.runLater(() -> {
            for (int i = 0; i < cantidadPersonas; i++) {
                String nombre = nombresFemeninos[i % nombresFemeninos.length];
                boolean quiereCubiculo = new Random().nextBoolean();
                Object recurso = quiereCubiculo ? cubiculos[0] : mesas[0]; // Se asigna alguno para arrancar

                Thread persona = new Thread(new Persona(nombre, recurso));
                persona.start();
            }

        });
    }


}
