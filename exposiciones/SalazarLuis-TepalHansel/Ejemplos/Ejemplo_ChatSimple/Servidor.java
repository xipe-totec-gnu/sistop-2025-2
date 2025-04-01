import java.io.*;
import java.net.*;

public class Servidor
{

    public static void main(String[] args) throws IOException
    {
        ServerSocket serverSocket=new ServerSocket(6666);
        ClientHandler ch=new ClientHandler();
        while (true) 
        {  
            Socket newConection=null;
            try {
                newConection=serverSocket.accept();
                System.out.println("Conección aceptada");
                System.out.println("Nuevo usuario entro al chat");
                ch.addMember(newConection);

            } catch (IOException e) 
            {
                if(newConection!=null)
                    newConection.close();
                serverSocket.close();
                System.out.println(e.getMessage());
            } 
            
        }
        
    }
}