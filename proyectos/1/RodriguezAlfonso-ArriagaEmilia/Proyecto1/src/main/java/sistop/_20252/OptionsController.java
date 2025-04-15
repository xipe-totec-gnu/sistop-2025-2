// Autores: Emilia Macarena y Alfonso D'Hernán
package sistop._20252;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.TextField;
import javafx.stage.Stage;

import java.io.IOException;

public class OptionsController {
    // Definimos los elementos visuales que le permitirán al usuario
    // decidir las variables de cambio.
    @FXML
    TextField startThreads, absenceField, maxWaitTime, minWaitTime;

    // Definimos las variables que serán cambiadas para nuestra ejecución.
    static int startThreadsInt, absence, maxTime, minTime;

    @FXML
    // Cuando el usuario haya (o no) introducido sus datos,
    // asignamos valores para la ejecución.
    protected void onClickExecButton(ActionEvent event) throws IOException {
        // try catch en caso de que el usuario ponga una entrada incorrecta.
        try{
            // si el texto no está vacio, verificamos si el valor es
            // mayor a 12. Si es verdadero, se deja en 12. Si no,
            // el valor es dejado como está en el texto.
            if(!startThreads.getText().isEmpty()){
                if(Integer.parseInt(startThreads.getText()) > 12){
                    startThreadsInt = 12;
                }else{
                    startThreadsInt = Integer.parseInt(startThreads.getText());
                }
            // Se deja un valor por default si no se introduce nada.
            }else{
                startThreadsInt = 10;
            }

            // La misma lógica es aplicable para los demás campos.
            if(!absenceField.getText().isEmpty()){
                absence = Integer.parseInt(absenceField.getText());
            }else{
                absence = 10000;
            }

            if(!maxWaitTime.getText().isEmpty()){
                maxTime = Integer.parseInt(maxWaitTime.getText());
            }else{
                maxTime = 5000;
            }

            if(!minWaitTime.getText().isEmpty()){
                minTime = Integer.parseInt(minWaitTime.getText());
            }else{
                maxTime = 3000;
            }

        } catch (Exception e) {
            startThreads.clear();
            absenceField.clear();
            maxWaitTime.clear();
            minWaitTime.clear();
        }

        // Una vez cargados los valores, pasamos a la ejecución del programa.
        FXMLLoader fxmlLoader = new FXMLLoader(ProjectStart.class.getResource("threadExecution.fxml"));
        Stage stage = (Stage)((Node)event.getSource()).getScene().getWindow();
        Scene scene = new Scene(fxmlLoader.load());
        stage.setTitle("Simulación de la Santuaria.");
        stage.setScene(scene);
        stage.show();
    }
}
