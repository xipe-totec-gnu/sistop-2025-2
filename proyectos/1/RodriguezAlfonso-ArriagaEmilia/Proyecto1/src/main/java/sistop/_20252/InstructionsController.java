package sistop._20252;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.stage.Stage;

import java.io.IOException;

public class InstructionsController {
    @FXML
    protected void onClickMainButton(ActionEvent event) throws IOException {
        // Conseguimos los recursos necesarios para poder cargar la próxima escena
        // a ejecutar.
        FXMLLoader fxmlLoader = new FXMLLoader(ProjectStart.class.getResource("projectStart.fxml"));
        Stage stage = (Stage)((Node)event.getSource()).getScene().getWindow();
        Scene scene = new Scene(fxmlLoader.load());
        stage.setTitle("Simulación de la Santuaria.");
        stage.setScene(scene);
        stage.show();
    }
}
