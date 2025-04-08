import java.io.*;
import java.net.Socket;

public class ListenerHandler extends Thread
{
    DataInputStream ear;

    public ListenerHandler(Socket socket)
    {
        try {
            this.ear=new DataInputStream(socket.getInputStream());
        } catch (IOException e) 
        {
            System.out.println(e.getMessage());
        }
    }
    @Override
    public void run()
    {
        while (true) 
        { 
            try{
                String received=this.ear.readUTF();
                System.out.println(received);

            } catch (IOException e) 
            {
                System.out.println("Señal perdida");
                return;
            }
        }

    }
}