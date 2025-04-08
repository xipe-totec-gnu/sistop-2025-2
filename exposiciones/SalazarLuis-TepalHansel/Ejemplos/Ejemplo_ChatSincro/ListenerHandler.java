import java.io.*;
import java.net.Socket;

public class ListenerHandler extends Thread {
    private DataInputStream ear;
    private final Socket socket;

    public ListenerHandler(Socket socket) {
        this.socket = socket;
        try {
            this.ear = new DataInputStream(socket.getInputStream());
        } catch (IOException e) {
            System.out.println("Error al inicializar ListenerHandler: " + e.getMessage());
        }
    }

    @Override
    public void run() {
        try {
            while (true) {
                String received = this.ear.readUTF();
                System.out.println(received);
            }
        } catch (IOException e) {
            System.out.println("Señal perdida listenerH");
        } finally {
            try {
                if (ear != null) ear.close();
                if (socket != null && !socket.isClosed()) socket.close();
            } catch (IOException ex) {
                System.out.println("Error al cerrar recursos: " + ex.getMessage());
            }
        }
    }
}