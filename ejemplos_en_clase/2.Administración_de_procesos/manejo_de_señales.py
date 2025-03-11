#!/usr/bin/python3
import os
import time
import signal

def manejador(signum, frame):
    signame = signal.Signals(signum).name
    print(f'Signal handler called with signal {signame} ({signum})')
    if signum == 17:
        # Recibí un SIGCHLD
        res = os.wait()
        print(f'Resultado de wait(): {res}')
    elif signum == 2:
        print('¿En serio quieres matarme? ¡Mira que tengo sentimientos!')
    elif signum == 15:
        print('OK, OK, ya me voy 🙁')
        exit(1)

def descongela(signum, frame):
    if signum == 18:
        print('Stayin\' alive!')

def interfaz(signum, frame):
    if signum == 28:
        print('¡He ahí un WINCH!')

signal.signal(signal.SIGTERM, manejador)
signal.signal(signal.SIGINT, manejador)
signal.signal(signal.SIGCONT, descongela)
signal.signal(signal.SIGWINCH, interfaz)


print(f'El PID de este proceso es: {os.getpid()}')

time.sleep(60)

