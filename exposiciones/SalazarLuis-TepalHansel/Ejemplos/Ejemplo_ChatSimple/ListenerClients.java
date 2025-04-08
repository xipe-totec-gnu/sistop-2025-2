import java.io.*;
import java.net.Socket;
import java.util.ArrayList;

public class ListenerClients extends Thread
{
    DataInputStream ear;
    DataOutputStream talk;
    ArrayList<Socket> participantes;
    Socket socket;
    public ListenerClients(Socket socket,ArrayList<Socket> participantes)
    {
        try {
            this.socket=socket;
            this.participantes=participantes;
            this.ear=new DataInputStream(socket.getInputStream());
            this.talk=null;
        } catch (IOException e) {
        }
    }
    @Override
    public void run()
    {
        while (true) 
        { 
            try{
                String received=this.ear.readUTF();
                for(Socket s:participantes)
                {
                    talk=new DataOutputStream(s.getOutputStream());
                    if(s!=this.socket)
                    {
                        talk.writeUTF(received);
                    }
                }

            } catch (IOException e) 
            {
                System.out.println("Señal perdida");
                try {
                    socket.close();
                } catch (IOException ex) {
                    System.out.println("Error al cerrar el socket");
                }
                participantes.remove(socket);
                System.out.println("Se ha desconectado un cliente");
                break;
            }
        }

    }
}

