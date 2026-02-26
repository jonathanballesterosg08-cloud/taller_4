import time

def obtener_elemento(lista):
    return lista[0]

def algoritmo_2(n):
    for i in range(n):
        pass 

def algoritmo_3(n):
    for i in range(n):
        for j in range(n):
            pass 


# Algoritmo 1
lista = list(range(20000))

inicio = time.perf_counter()
obtener_elemento(lista)
fin = time.perf_counter()
print("Tiempo algoritmo 1:", fin - inicio, "segundos")


# Algoritmo 2
inicio = time.perf_counter()
algoritmo_2(20000)
fin = time.perf_counter()
print("Tiempo algoritmo 2:", fin - inicio, "segundos")


# Algoritmo 3
inicio = time.perf_counter()
algoritmo_3(20000) 
fin = time.perf_counter()
print("Tiempo algoritmo 3:", fin - inicio, "segundos")


