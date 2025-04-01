import java.io.*;
import java.net.*;
import java.util.*;

public class cliente{
    public static void main(String [] args){
        try{
            Scanner reader = new Scanner(System.in);
            InetAddress ip = InetAddress.getByName("localhost");
            Socket socket = new Socket(ip, 1234);
            DataInputStream dataIn = new DataInputStream(socket.getInputStream());
            DataOutputStream dataOut = new DataOutputStream(socket.getOutputStream());

            while (true) {
                System.out.println(dataIn.readUTF());
                String tosend = reader.nextLine();
                dataOut.writeUTF(tosend);
                if(tosend.equals("5")){
                    System.out.println("La conexión se cierra" + socket);
                    socket.close();
                    System.out.println("ADIOS");
                    break;
                }
                //Impresion de ingresa el primer numero
                String received = dataIn.readUTF();
                System.out.println(received);
                //Ingreso del primer numero
                String firstN=reader.nextLine();
                dataOut.writeUTF(firstN);
                System.out.println(dataIn.readUTF());
                String secondN=reader.nextLine();
                dataOut.writeUTF(secondN);
                System.out.println(dataIn.readUTF());

            }
            reader.close();
            dataIn.close();
            dataOut.close();
        }catch(Exception e){
            
            System.out.println(e);
        }
    }
}