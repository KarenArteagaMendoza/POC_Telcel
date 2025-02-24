import requests
import random
import csv
import numpy as np
import zipf_popularity as zp
import matplotlib.pyplot as plt
import time


BASE_URL = "http://127.0.0.1:5000"



# Función para mandar una consulta a la aplicación e imprimir el resultado
def request_data(key):
    try:
        # Enviar un GET a la app
        response = requests.get(f'{BASE_URL}/get_data/{key}')
        
        # Checar si la consulta fue exitosa
        if response.status_code == 200:
            data = response.json()
            return data # Regresar el dato solicitado
        elif response.status_code == 404:
            print("Data not found.")
            return {"source": -1, "id": 0, "data": 0} 
        else:
            print(f"Error: {response.status_code}")
            return {"source": -1, "id": 0, "data": 0}

    except Exception as e:
        print(f"Failed to retrieve data: {e}")
        return {"source": -1, "id": 0, "data": 0}
    

# Función que genera una muestra de tamaño "sample_size" de distribución Zipf
# N es el tamaño de la base de datos principal
# s es el parámetro de la función de densidad Zipf s > 0
# Regresa un arreglo de tamaño "sample_size" de tasas de aciertos al caché de la prueba
def aciertos(N, s, sample_size):
    ks, pmf, samples = zp.muestra_zipf(N, s, sample_size) # Generar una muestra Zipf
    zp.graficar_muestra(N, s, sample_size, ks, pmf, samples) # Graficar muestra generada
    cache_hits = 0 # Número de aciertos al caché
    hit_rate = 0.0 # Tasa de aciertos al caché
    i = 1
    rates = [] # Arreglo de tasas de acierto
    for key in samples: # necesito 100000 para llenar la base
        start_time = time.time() 
        data = request_data(key) # Consultar la llave 
        if data['source'] == 0: # Si la llave está en caché
            cache_hits += 1
        hit_rate = cache_hits/i # Actualizar tasa de aciertos
        end_time = time.time()
        print(f'Consulta: {i}   |', f'Hit rate: {hit_rate}    |', f'Tiempo ejecución: {end_time - start_time}')
        rates.append(hit_rate)
        i += 1
    
    return rates

# Función para graficar las tasas de acierto contra el número de consultas
# Llama a la función "aciertos()"
def graficar_hitrates(N, s, sample_size):
    rates = aciertos(N, s, sample_size)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, sample_size + 1), rates, label='Tasa de aciertos al caché')
    plt.xlabel('Número de consulta')
    plt.ylabel('Tasa de aciertos')
    plt.title("Tasa de aciertos al caché de 20 TTL")
    plt.grid(True)
    plt.legend()
    plt.savefig('hit_rates.png') # Guardar la gráfica
    plt.show()

# Función para obtener métricas sobre el almacenamiento del caché
# Genera n consultas a la aplicación de llaves nuevas para conocer la cantidad de datos que llenan el caché
# Imprime el tiempo entre una consulta y otra para conocer cuántas consultas se hacen por segundo
def llenar_cache():
    arr = []
    for key in range(10_000):
        start_time = time.time()
        data = request_data(key)
        end_time = time.time()
        t = end_time - start_time
        arr.append(t)
        print(f'{key} | Tiempo entre consultas: {t}')
    m = np.mean(arr)
    print(f"Tiempo entre consultas promedio: {m}")
    print(f"Tasa de consultas por segundo: {1/m}")



if __name__ == "__main__":
    #llenar_cache() # Descomentar para hacer pruebas al caché
    # Tiempo característico: 
    N =  69_000      # Tamaño de la base de datos principal (proporcional al caché)
    s = 0.8           # Parámetro de la distribución Zipf entre (0.8, 1.1)
    sample_size = 500_000  # Tamaño de la muestra que se va a generar, 200,000 para 100% y 80% 
    graficar_hitrates(N, s, sample_size)


'''
Para TTL
C = 13_800
Valores de N (tamaño de base de datos principal):
    13_800 - caché 100%
    17_250 - caché 80%
    27_600 - caché 50%
    69_000 - caché 20%
    138_000 - caché 10%
'''

'''
Para LRU
C = 13_861
Valores de N (tamaño de base de datos principal):
    13_861 - caché 100%
    17_327 - caché 80%
    27_722 - caché 50%
    69_305 - caché 20%
    138_610 - caché 10%
'''

'''
Tamaños de muestras
    300_000 - caché 100%
    300_000 - caché 80%
    400_000 - caché 50%
    500_000 - caché 20%
    500_000 - caché 10%
'''

