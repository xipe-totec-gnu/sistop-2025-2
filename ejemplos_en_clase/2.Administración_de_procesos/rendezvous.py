#!/usr/bin/python3
import threading
import time
import random

def f1(s1,s2):
    print('f1 inicia')
    time.sleep(random.random())
    print('f1 señaliza...')
    s1.release()
    s2.acquire()
    print('f1 tiene todo para terminar.')

def f2(s1,s2):
    print('f2 inicia')
    time.sleep(random.random())
    print('f2 señaliza...')
    s2.release()
    s1.acquire()
    print('f2 tiene todo para terminar.')

s1=threading.Semaphore(0)
s2=threading.Semaphore(0)
threading.Thread(target=f1, args=[s1,s2]).start()
threading.Thread(target=f2, args=[s1,s2]).start()
