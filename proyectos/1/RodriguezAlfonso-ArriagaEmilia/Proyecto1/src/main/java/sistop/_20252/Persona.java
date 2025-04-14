package sistop._20252;

import java.util.Random;
import java.util.concurrent.Semaphore;

class Persona implements Runnable {
    private final String nombre;
    private final Random random = new Random();
    private Object recurso;

    public Persona(String nombre, Object recursoInicial) {
        this.nombre = nombre;
        this.recurso = recursoInicial;
    }

    @Override
    public void run() {
        while (true) {
            boolean prioridad = random.nextBoolean();
            boolean quiereCubiculo = random.nextBoolean();

            if (quiereCubiculo) {
                recurso = ExecutionController.cubiculos[random.nextInt(ExecutionController.cubiculos.length)];
                ((Cubiculo) recurso).usar(nombre, prioridad);
            } else {
                recurso = ExecutionController.mesas[random.nextInt(ExecutionController.mesas.length)];
                ((Mesa) recurso).usar(nombre, prioridad);
            }


            boolean seguir = random.nextBoolean();
            if (!seguir) {
                System.out.println(nombre + " ha decidido irse por ahora.");
                try {
                    Thread.sleep(10000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }


            try {
                Thread.sleep(1000 + random.nextInt(3000));
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}