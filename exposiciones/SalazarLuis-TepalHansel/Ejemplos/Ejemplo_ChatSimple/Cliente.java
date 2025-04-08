import java.io.*;
import java.net.*;
import java.util.*;

public class Cliente
{
    public static void main(String[] args) 
    {
        try 
        {
            Scanner reader = new Scanner(System.in);
            String name=args[0];
            InetAddress ip = InetAddress.getByName("localhost");
            Socket socket = new Socket(ip, 6666);
            //DataInputStream dataIn = new DataInputStream(socket.getInputStream());
            DataOutputStream dataOut = new DataOutputStream(socket.getOutputStream());
            ListenerHandler hear=new ListenerHandler(socket);
            hear.start();
            while (true) 
            {   
                if(!hear.isAlive()) return;
                dataOut.writeUTF(reader.nextLine());
                //dataOut.writeUTF(name + ": " + reader.nextLine());
            }
        } catch (IOException e) 
        {
            System.out.println(e.getMessage());
        }        
    }

}
