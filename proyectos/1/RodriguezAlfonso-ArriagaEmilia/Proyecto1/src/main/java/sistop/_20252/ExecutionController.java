// Autores: Emilia Macarena y Alfonso D'Hernán

package sistop._20252;

import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.image.ImageView;

import java.io.IOException;

import java.util.Random;

public class ExecutionController {
    // Definimos un objeto Random para aleatorizar los
    // tiempos de espera.
    static Random randomizer = new Random();

    // Definimos los elementos que nos ayudarán a identificar a las
    // mesas y a los cubículos.
    public static final String[] tableColours = {"PINK", "BLUE", "YELLOW"};
    public static Mesa[] mesas;
    public static Cubiculo[] cubiculos;
    public static final int cantidadPersonas = OptionsController.startThreadsInt;

    // Definimos todos los elementos visuales que vamos a utilizar
    // dentro de la ejecución.
    @FXML
    public ImageView t1S1, t1S2, t1S3, t2S1, t2S2, t2S3, t3S1, t3S2, t3S3;
    @FXML
    public ImageView c1S1, c1S2, c2S1, c2S2;
    @FXML
    public Label firstTable, secondTable, thirdTable;
    @FXML
    public Label firstCubicle, secondCubicle;
    @FXML
    public Button newThreadButton;
    @FXML
    public TextField threadNameField;

    @FXML
    public void exitApp(ActionEvent event) throws IOException {
        // Si se presiona el botón de salir, salimos de la aplicación.
        Platform.exit();
    }

    // Función para ejecutar procesos una vez que se haya presionado el botón correspondiente.
    @FXML
    public void initialize() {
        mesas = new Mesa[3];
        cubiculos = new Cubiculo[2];

        // Definimos arreglos de información para poder inicializarlos de forma
        // más fácil en su respectiva instancia.
        ImageView[][] tableSeats = {{t1S1, t1S2, t1S3},{t2S1, t2S2, t2S3},{t3S1, t3S2, t3S3}};
        ImageView[][] cubicleSeats = {{c1S1, c1S2},{c2S1, c2S2}};
        Label[] cubicleInfo = {firstCubicle, secondCubicle};
        Label[] tableInfo = {firstTable, secondTable, thirdTable};

        // Definimos todas las instancias necesitadas para el programa.
        for (int i = 0; i < mesas.length; i++) {
            mesas[i] = new Mesa(i + 1, tableColours[i], tableSeats[i][0], tableSeats[i][1], tableSeats[i][2], tableInfo[i]);
        }
        for (int i = 0; i < cubiculos.length; i++) {
            cubiculos[i] = new Cubiculo(i + 1, cubicleSeats[i][0], cubicleSeats[i][1], cubicleInfo[i]);
        }

        String[] nombresFemeninos = {
                "Ana", "Luisa", "Sofía", "Camila", "Valeria", "Mariana",
                "Fernanda", "Isabella", "Daniela", "Gabriela", "Renata", "Andrea"
        };

        Platform.runLater(() -> {
            // Ponemos un sleep para permitir que la información no pegue demasiado rápido.
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
            // Generamos una cierta cantidad de personas, y las inicializamos
            // de manera que tengan un recurso aleatorio qué acceder.
            for (int i = 0; i < cantidadPersonas; i++) {
                String nombre = nombresFemeninos[i % nombresFemeninos.length];
                boolean quiereCubiculo = new Random().nextBoolean();
                Object recurso = quiereCubiculo ? cubiculos[0] : mesas[0]; // Se asigna alguno para arrancar

                Thread persona = new Thread(new Persona(nombre, recurso));
                persona.start();
            }

        });
    }

    // Función que nos permitirá crear un nuevo hilo, de así ser deseado.
    @FXML
    public void createNewThread(ActionEvent event){
        Platform.runLater(() -> {
            String nombre;
            // Si el campo de texto en el que se pone el nombre de la nueva
            // persona (hilo) a generar tiene texto, se genera el nuevo hilo.
            if(!threadNameField.getText().isEmpty()){
                nombre = threadNameField.getText();
                // Ponemos un valor aleatorio.
                boolean quiereCubiculo = new Random().nextBoolean();
                Object recurso = quiereCubiculo ? cubiculos[randomizer.nextInt(2)] : mesas[randomizer.nextInt(3)]; // Se asigna alguno para arrancar

                Thread persona = new Thread(new Persona(nombre, recurso));
                persona.start();
                // Limpiamos el campo para permitir nuevas entradas de nombres.
                threadNameField.clear();
            }
        });
    }


}
