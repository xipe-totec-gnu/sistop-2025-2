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
    @FXML
    TextField startThreads, absenceField, maxWaitTime, minWaitTime;

    static int startThreadsInt, absence, maxTime, minTime;

    @FXML
    protected void onClickExecButton(ActionEvent event) throws IOException {
        try{
            if(!startThreads.getText().isEmpty()){
                if(Integer.parseInt(startThreads.getText()) > 12){
                    startThreadsInt = 12;
                }else{
                    startThreadsInt = Integer.parseInt(startThreads.getText());
                }
            }else{
                startThreadsInt = 10;
            }

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

        FXMLLoader fxmlLoader = new FXMLLoader(ProjectStart.class.getResource("threadExecution.fxml"));
        Stage stage = (Stage)((Node)event.getSource()).getScene().getWindow();
        Scene scene = new Scene(fxmlLoader.load());
        stage.setTitle("Simulación de la Santuaria.");
        stage.setScene(scene);
        stage.show();
    }
}
