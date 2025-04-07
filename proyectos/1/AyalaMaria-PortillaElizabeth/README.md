`Integrantes:`<br> 
 1. Ayala Hernandez Maria Fernanda
 2. Portilla Hermenegildo Elizabeth

# 🔍 PROBLEMA: ENTRADA PARA LABORATORIO (Laboratorio de Ingeniería)

- El laboratorio tiene un número limitado de mesas (N) definidas por el usuario.
- Puede que cierta cantidad de mesas no este disponibles un dia debido a fallas en su equipo. 
- Cada mesa permite hasta 3 alumnos simultáneamente.
- Si todas las mesas están ocupadas, hasta 6 alumnos pueden esperar en la sala de espera.
- Un jefe de laboratorio administra la entrada y asigna mesas.
- Si el jefe se va a comer, nadie puede entrar al laboratorio, aunque haya mesas libres. Sin embargo, los alumnos que ya están pueden salir.
- Cuando el jefe regresa, autoriza el ingreso de los alumnos que estaban esperando.
- Al finalizar se necesita un reporte del total de alumnos que estubo en cada mesa

## 🔄 Mecanismos de sincronización detectados
__Eventos concurrentes__:
- Llegada de alumnos.
- Asignación de mesas.
- Salida de alumnos.
- Disponibilidad del jefe.

__Problemas a controlar__:

- Evitar que más de 3 alumnos se sienten en una mesa.
- Asignas mesas funcionales del dia.
- Evitar que más de 6 alumnos esperen en la sala de espera.
- Bloquear la entrada cuando el jefe no está.
- Permitir que los alumnos puedan salir aunque el jefe no este. 

__Eventos sin orden relativo importante__:

- Salida de alumnos.
- Llegada de alumnos (si hay disponibilidad).
