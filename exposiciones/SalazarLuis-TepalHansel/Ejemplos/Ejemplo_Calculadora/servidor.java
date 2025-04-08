import java.io.*;
import java.net.*;

public class servidor {
    public static void main(String[] args) throws IOException{
        ServerSocket serverSocket = new ServerSocket(1234);

        while(true){
            Socket socket = null;
            try{
                socket = serverSocket.accept();
                System.out.println("HOLA BB " + socket);
                DataInputStream in = new DataInputStream(socket.getInputStream());
                DataOutputStream out = new DataOutputStream(socket.getOutputStream());
                System.out.println("Añadiendo un hilo al cliente");
                Thread newThread = new clienteHeadler(socket, in, out);
                newThread.start();
            }catch (Exception e){
                socket.close();
                System.out.println(e);
            }
        }
    }
}

class clienteHeadler extends Thread{
    DataInputStream dataIn;
    DataOutputStream dataOut;
    Socket socket;

    public clienteHeadler(Socket socket, DataInputStream dataIn, DataOutputStream dataOut){
        this.socket = socket;
        this.dataIn = dataIn;
        this.dataOut = dataOut;
    }
        @Override
        public void run(){
            String received;
            while (true) {
                try{
                    dataOut.writeUTF("¿Qué deseas hacer? \n1. Sumar \n2. Restar \n3. Multiplicar \n4. Dividir \n5. Salir");
                    received = dataIn.readUTF();
                    if(received.equals("5")){
                        System.out.println("Cliente " + this.socket + " envió un mensaje de cierre");
                        System.out.println("Cerrando esta conexión");
                        this.socket.close();
                        System.out.println("Conexión cerrada");
                        break;
                    }
                    switch(received){
                        case "1":
                            dataOut.writeUTF("Ingresa el primer número: ");
                            int a = Integer.parseInt(dataIn.readUTF());
                            dataOut.writeUTF("Ingresa el segundo número: ");
                            int b = Integer.parseInt(dataIn.readUTF());
                            int sum = a + b;
                            dataOut.writeUTF("La suma es: " + sum);
                            break;
                        case "2":
                            dataOut.writeUTF("Ingresa el primer número: ");
                            int c = Integer.parseInt(dataIn.readUTF());
                            dataOut.writeUTF("Ingresa el segundo número: ");
                            int d = Integer.parseInt(dataIn.readUTF());
                            int res = c - d;
                            dataOut.writeUTF("La resta es: " + res);
                            break;
                        case "3":
                            dataOut.writeUTF("Ingresa el primer número: ");
                            int e = Integer.parseInt(dataIn.readUTF());
                            dataOut.writeUTF("Ingresa el segundo número: ");
                            int f = Integer.parseInt(dataIn.readUTF());
                            int mul = e * f;
                            dataOut.writeUTF("La multiplicación es: " + mul);
                            break;
                        case "4":
                            dataOut.writeUTF("Ingresa el primer número: ");
                            int g = Integer.parseInt(dataIn.readUTF());
                            dataOut.writeUTF("Ingresa el segundo número: ");
                            int h = Integer.parseInt(dataIn.readUTF());
                            int div = g / h;
                            dataOut.writeUTF("La división es: " + div);
                            break;
                        case "5":
                            System.out.println("El cliente" + this.socket + "salio");
                            this.socket.close();
                            System.out.println("Conexión cerrada");
                            break;
                        default:
                            dataOut.writeUTF("Opción inválida");
                            break;
                    
                    }
                }catch (IOException e){
                    e.printStackTrace();
                    return;
            }
        }
        try{
            this.dataIn.close();
            this.dataOut.close();
        }catch(IOException e){
            e.printStackTrace();
        }
    }
}
