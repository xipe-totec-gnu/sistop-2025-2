import java.net.*;
import java.util.ArrayList;



public class ClientHandler 
{
    ArrayList<Socket> participantes;
    public ClientHandler()
    {
        participantes=new ArrayList<>();
    }

    public void addMember(Socket con)
    {
        participantes.add(con);
        ListenerClients member=new ListenerClients(con,participantes);
        member.start();
    }
}