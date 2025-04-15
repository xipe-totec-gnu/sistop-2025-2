package sistop._20252;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.stage.Stage;

import java.io.IOException;

public class MainMenuController {

    @FXML
    protected void onClickSimButton(ActionEvent event) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(ProjectStart.class.getResource("options.fxml"));
        Stage stage = (Stage)((Node)event.getSource()).getScene().getWindow();
        Scene scene = new Scene(fxmlLoader.load());
        stage.setTitle("Simulación de la Santuaria.");
        stage.setScene(scene);
        stage.show();
    }
}