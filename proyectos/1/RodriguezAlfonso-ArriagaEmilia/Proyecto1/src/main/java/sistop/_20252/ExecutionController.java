package sistop._20252;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.stage.Stage;

import java.io.IOException;

import java.util.Random;
import java.util.Scanner;
import java.util.concurrent.CountDownLatch;

public class ExecutionController {
    FXMLLoader fxmlLoader;

    public static Mesa[] mesas;
    public static Cubiculo[] cubiculos;
    public static final int cantidadPersonas = 10;
    // Control de sincronización
    public static CountDownLatch latch = new CountDownLatch(cantidadPersonas);
    public static volatile boolean continuar = true;

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
    public void initialize(){
        mesas = new Mesa[3];
        cubiculos = new Cubiculo[2];

        for (int i = 0; i < mesas.length; i++) {
            mesas[i] = new Mesa(i + 1);
        }

        for (int i = 0; i < cubiculos.length; i++) {
            cubiculos[i] = new Cubiculo(i + 1);
        }

        String[] nombresFemeninos = {
                "Ana", "Luisa", "Sofía", "Camila", "Valeria", "Mariana",
                "Fernanda", "Isabella", "Daniela", "Gabriela", "Renata", "Andrea"
        };

        for (int i = 0; i < cantidadPersonas; i++) {
            String nombre = nombresFemeninos[i % nombresFemeninos.length];
            boolean quiereCubiculo = new Random().nextBoolean();
            Object recurso = quiereCubiculo ? cubiculos[0] : mesas[0]; // Se asigna alguno para arrancar

            Thread persona = new Thread(new Persona(nombre, recurso));
            persona.start();
        }

        Scanner scanner = new Scanner(System.in);
        while (continuar) {
            try {
                latch.await(); // Espera a que todas las personas terminen su ciclo

                System.out.println("\n¿Deseas cerrar la santuaria? (s/n)");
                String respuesta = scanner.nextLine().trim().toLowerCase();

                if (respuesta.equals("s")) {
                    continuar = false;
                    System.exit(0);
                } else {
                    latch = new CountDownLatch(cantidadPersonas); // Reinicia latch
                }

            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        scanner.close();
    }


}
