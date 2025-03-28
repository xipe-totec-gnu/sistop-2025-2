import java.util.concurrent.Semaphore;         // Concurrencia
import java.util.concurrent.atomic.AtomicInteger; // Controles en hilos

public class CruceRio {
    // Semáforos
    private static final Semaphore mutex = new Semaphore(1);       // Mutex para la seccion critica
    private static final Semaphore filaHackers = new Semaphore(0); // Hackers esperando turno
    private static final Semaphore filaSerfs = new Semaphore(0);   // Serfs esperando turno
    
    // Contar personas en la balsa
    private static final AtomicInteger hackersEnBalsa = new AtomicInteger(0); // Cantidad actual de hackers en balsa
    private static final AtomicInteger serfsEnBalsa = new AtomicInteger(0);   // Cantidad actual de serfs en balsa
    
    // Definimos cuanta gente asistira a la reunion, en este caso definimos 20 serfs y 20 hackers
    private static final AtomicInteger hackersRestantes = new AtomicInteger(20); // Total hackers por cruzar
    private static final AtomicInteger serfsRestantes = new AtomicInteger(20);   // Total serfs por cruzar
    
    public static void main(String[] args) {
        
        for (int i = 1; i <= 20; i++) {
            new Thread(new Desarrollador("Hacker", i)).start(); 
            new Thread(new Desarrollador("Serf", i)).start();   
            try {
                Thread.sleep(100); 
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt(); 
            }
        }
        
        // Verifica que todos crucen
        new Thread(() -> {
            while (hackersRestantes.get() > 0 || serfsRestantes.get() > 0) {
                try {
                    Thread.sleep(2000); 
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
            System.out.println("Todos han cruzado el rio :D"); 
        }).start();
    }

    // Definimos clase desarrollador
    static class Desarrollador implements Runnable {
        private final String tipo; // Un desarrollador puede ser "Hacker" o "Serf"
        private final int id;    

        public Desarrollador(String tipo, int id) {
            this.tipo = tipo;
            this.id = id;
        }

        // Método que ejecuta cada hilo
        public void run() {
            try {
                mutex.acquire(); // Adquiere acceso exclusivo
                
                // Actualiza contadores según el tipo
                if (tipo.equals("Hacker")) {
                    hackersEnBalsa.incrementAndGet();  // +1 hacker en balsa
                    hackersRestantes.decrementAndGet(); // -1 hacker por cruzar
                } else {
                    serfsEnBalsa.incrementAndGet();    // +1 serf en balsa
                    serfsRestantes.decrementAndGet();   // -1 serf por cruzar
                }
                
                // Muestra estado actual
                System.out.println("Un " + tipo + " se ha subido a la balsa. H=" + 
                                 hackersEnBalsa.get() + " S=" + serfsEnBalsa.get());
                Thread.sleep(1000); 
                
                verificarGrupoValido(); // Verifica si puede cruzar
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        // Verifica las condiciones para cruzar
        private void verificarGrupoValido() throws InterruptedException {
            int h = hackersEnBalsa.get(); // Hackers actuales
            int s = serfsEnBalsa.get();   // Serfs actuales
            
            // Caso 1: 4 hackers 
            if (h == 4) {
                cruzarBalsa(4, 0);
            } 
            // Caso 2: 4 serfs 
            else if (s == 4) {
                cruzarBalsa(0, 4);
            } 
            // Caso 3: 2 hackers + 2 serfs
            else if (h >= 2 && s >= 2) {
                cruzarBalsa(2, 2);
            }
            // Caso 4: Grupo inválido pero con 4+ personas (para evitar bloqueo)
            else if ((h + s) >= 4 && (h == 1 || s == 1)) {
                cruzarBalsa(h, s); // Fuerza el cruce
            }
            // Si no se cumple ningún caso, espera
            else {
                mutex.release(); // Libera el mutex
                if (tipo.equals("Hacker")) {
                    filaHackers.acquire(); // Espera en fila de hackers
                } else {
                    filaSerfs.acquire();   // Espera en fila de serfs
                }
            }
        }
    }

    // Método para manejar el cruce de la balsa
    private static void cruzarBalsa(int h, int s) throws InterruptedException {
        // Actualiza contadores: resta los que cruzan
        hackersEnBalsa.addAndGet(-h);
        serfsEnBalsa.addAndGet(-s);
        
        // Muestra mensaje del cruce
        System.out.println("La balsa ha cruzado el rio con " + h + " hackers y " + s + " serfs.");
        System.out.println("Faltan por cruzar: Hackers=" + hackersRestantes.get() + 
                         " Serfs=" + serfsRestantes.get());
        Thread.sleep(1000); 
        // Libera permisos para desarrolladores esperando
        for (int i = 0; i < h; i++) filaHackers.release(); // Notifica a hackers
        for (int i = 0; i < s; i++) filaSerfs.release();   // Notifica a serfs
        
        mutex.release(); // Libera el mutex para nuevos accesos
    }
}