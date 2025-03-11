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

signal.signal(signal.SIGCHLD, manejador)

print(f'El PID de este proceso es: {os.getpid()}')
pid = os.fork()

if pid > 0:
    print(f'Este es el proceso padre. Mi PID sigue siendo {os.getpid()}. El hijo es {pid}')
    time.sleep(60)
elif pid == 0:
    print(f'Este es el proceso hijo. Mi PID es {os.getpid()}')
    #os.execl('/bin/ls', 'listador', '-l')
else:
    print(f'¡¡¡¡¡AUUUUUUGGGGHHHHH!!!!! ¿Y qué hago con un {pid}?')

