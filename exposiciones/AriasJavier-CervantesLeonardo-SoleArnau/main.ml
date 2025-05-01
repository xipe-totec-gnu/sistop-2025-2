let num_filosofos = 5

(* Creamos los palillos como canales de eventos *)
let palillos = Array.init num_filosofos (fun _ -> Event.new_channel ())

(* Inicializar cada palillo con un mensaje (disponible) *)
let () =
  Array.iter (fun ch ->
    ignore (Thread.create (fun () -> Event.sync (Event.send ch ())) ())
  ) palillos

(* Función del filósofo con flushes *)
let filosofo id =
  while true do
    Printf.printf "Filósofo %d está pensando.\n%!" id;
    Thread.delay (Random.float 2.0);
    
    Printf.printf "Filósofo %d tiene hambre.\n%!" id;
    
    let primero, segundo = 
      if id mod 2 = 0 then (id, (id + 1) mod num_filosofos)
      else ((id + 1) mod num_filosofos, id)
    in

    Printf.printf "Filósofo %d intenta tomar el palillo %d.\n%!" id primero;
    Event.sync (Event.receive palillos.(primero));
    Printf.printf "Filósofo %d toma el palillo %d.\n%!" id primero;

    Printf.printf "Filósofo %d intenta tomar el palillo %d.\n%!" id segundo;
    Event.sync (Event.receive palillos.(segundo));
    Printf.printf "Filósofo %d toma el palillo %d.\n%!" id segundo;

    Printf.printf "Filósofo %d está comiendo.\n%!" id;
    Thread.delay (Random.float 2.0);

    Printf.printf "Filósofo %d libera los palillos.\n%!" id;
    Event.sync (Event.send palillos.(primero) ());
    Event.sync (Event.send palillos.(segundo) ())
  done

(* Lanzar filósofos *)
let () =
  let rec lanzar_filosofos = function
    | 5 -> ()
    | n -> 
        ignore (Thread.create filosofo n);
        lanzar_filosofos (n + 1)
  in
  lanzar_filosofos 0;
  
  (* Mantener el programa activo *)
  while true do
    Thread.delay 1.0
  done