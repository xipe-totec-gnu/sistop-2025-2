
#Trolebus
# Una situación cotidiana con concurrencia y sincronización

Un problema para abordar la concurrencia y la sincronización en primera instancia fue el uso del pumabus, ya que, siempre hay bastantes usuarios queriendo abordar, pero además de que solo en el metro CU se respetan las líneas y estar formados, no encontramos alguna otra regla, más que subir en las paradas establecidas, por lo que, pensamos que en el día a día también usamos el transporte público, específicamente un trolebús, este camión azul tiene algunas características (restricciones): 

- **Espacio mixto**  
- **Asientos comunes**  
- **Asientos reservados**  
- **Espacio personas paradas**  
- **Espacio exclusivo para mujeres**  
  - Asientos para mujeres  
  - Espacio mujeres paradas  

Además también encontramos y establecimos que suben personas de distintos perfiles:

- Mujeres  
- Mujeres de la tercera edad, embarazadas o con alguna comorbilidad  
- Hombres de la tercera edad, embarazadas o con alguna comorbilidad  
- Hombres  

Estos perfiles ejecutan acciones como: **buscar asiento, pararse, bajarse**.  
En la simulación se tendrá en cuenta que el camión comienza vacío y realiza paradas para subir y bajar pasajeros.

## Reglas de la simulación concurrente

- **Asientos reservados**:  
  Solo pueden ser ocupados por mujeres y hombres de la tercera edad, embarazadas o con alguna comorbilidad. Pero ambos perfiles pueden ocupar cualquier asiento.

- **Espacio mixto**:  
  Persona de la tercera edad, embarazadas o con alguna comorbilidad: si no encuentra asiento libre o reservado no se sube.  
  Las mujeres y los hombres pueden ocupar cualquier lugar, excepto asientos reservados.

- **Espacio exclusivo**:  
  Los hombres no pueden ocupar la zona exclusiva de mujeres.
