import json
import time
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from core_functions import construir_grafo

def medir_tiempo_construccion_calculo(data):
    start_time = time.time()
    G = construir_grafo(data)
    tiempo_construccion = time.time() - start_time

    return tiempo_construccion

def experimentar_con_instancias(archivos_instancias):
    resultados = {}

    for archivo in archivos_instancias:
        with open(archivo, 'r') as f:
            data = json.load(f)
        nombre_instancia = archivo.split("/")[-1]
        resultados[nombre_instancia] = {
            "tiempo_construccion": []
        }

        tiempo_construccion = medir_tiempo_construccion_calculo(data)
        resultados[nombre_instancia]["tiempo_construccion"].append(tiempo_construccion)

    return resultados

def graficar_resultados(resultados):
    instancias = list(resultados.keys())
    tiempos_construccion = [resultados[instancia]["tiempo_construccion"][0] for instancia in instancias]

    fig, ax = plt.subplots()

    ax.barh(instancias, tiempos_construccion, color='skyblue')
    ax.set_xlabel('Tiempo de Construcción (s)')
    ax.set_ylabel('Instancia')
    ax.set_title('Tiempo de Construcción del Grafo por Instancia')

    plt.show()

# Parámetros de la experimentación
archivos_instancias = ["instances/toy_instance.json", "instances/retiro-tigre-semana.json", "instances/new_instance.json"]

# Ejecutar experimentación
resultados = experimentar_con_instancias(archivos_instancias)

# Graficar resultados
graficar_resultados(resultados)

# Imprimir tiempos de graficación
for instancia, datos in resultados.items():
    tiempo_graficacion = sum(datos["tiempo_construccion"])
    print(f"Tiempo de graficación para la instancia {instancia}: {tiempo_graficacion} segundos")
