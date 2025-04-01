import java.io.*;
import java.net.*;

public class Cliente
{
    public static void main(String[] args) 
    {
        Socket socket = null;
        ListenerHandler hear = null;
        try 
        {
            String name = args[0];
            InetAddress ip = InetAddress.getByName("localhost");
            socket = new Socket(ip, 6666);
            //DataInputStream dataIn = new DataInputStream(socket.getInputStream());
            DataOutputStream dataOut = new DataOutputStream(socket.getOutputStream());
            hear = new ListenerHandler(socket);
            hear.start();
            while (true) 
            {   
                dataOut.writeUTF("hola " + name);
            }
        } catch (IOException ex) 
        {
            if (socket != null) {
                try {
                    socket.close();
                } catch (IOException closeEx) {
                    System.out.println(closeEx.getMessage());
                }
            }
            if (hear != null) {
                hear.interrupt();
            }
            System.out.println(ex.getMessage());
        }        
    }

}
