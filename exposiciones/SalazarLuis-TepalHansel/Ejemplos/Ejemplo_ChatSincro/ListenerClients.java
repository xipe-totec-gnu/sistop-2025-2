import java.io.*;
import java.net.Socket;
import java.util.ArrayList;
import java.util.concurrent.Semaphore;
public class ListenerClients extends Thread
{
    DataInputStream ear;
    DataOutputStream talk;
    ArrayList<Socket> participantes;
    Socket socket;
    private final Semaphore mutex=new Semaphore(1);
    public ListenerClients(Socket socket,ArrayList<Socket> participantes)
    {
        try {
            this.socket=socket;
            this.participantes=participantes;
            mutex.acquire();
            participantes.add(socket);
            mutex.release();
            this.ear=new DataInputStream(socket.getInputStream());
            this.talk=null;
        } catch (Exception e) {
        }
    }
    @Override
    public void run()
    {
        while (true) 
        { 
            try{
                String received=this.ear.readUTF();
                int i=0;
                mutex.acquire();
                while(i<participantes.size()){
                    Socket s=participantes.get(i);
                    talk=new DataOutputStream(s.getOutputStream());
                    if(s!=this.socket)
                    {
                        if(!s.isClosed())
                            talk.writeUTF(received);
                    }
                    i++;
                }
                mutex.release();

            } catch (Exception e) 
            {
                System.out.println("Señal perdido listenerC");
                try {
                    socket.close();
                    participantes.remove(socket);
                } catch (IOException ex) {
                    System.out.println("Error al cerrar el socket");
                }   
                System.out.println("Se ha desconectado un cliente");
                break;
            }
        }

    }
}

// @Override
// public void run() {
//     while (true) {
//         try {
//             String received = this.ear.readUTF();
//             synchronized (participantes) { // Sincroniza el acceso a la lista
//                 for (Socket s : participantes) {
//                     if (s != this.socket && !s.isClosed()) {
//                         DataOutputStream talk = new DataOutputStream(s.getOutputStream());
//                         talk.writeUTF(received);
//                     }
//                 }
//             }
//         } catch (IOException e) {
//             System.out.println("Señal perdida listenerC");
//             synchronized (participantes) { // Sincroniza la eliminación del cliente
//                 participantes.remove(socket);
//             }
//             try {
//                 socket.close();
//             } catch (IOException ex) {
//                 System.out.println("Error al cerrar el socket");
//             }
//             System.out.println("Se ha desconectado un cliente");
//             break;
//         }
//     }
// }

