import time
import json
import networkx as nx
from core_functions import construir_grafo, flujo_maximo_corte_minimo, cambios_por_reparaciones, interpretacion_vagones, plot

def medir_tiempo_construccion_calculo(G):
    """
    Mide el tiempo de construcción del grafo y el tiempo de cálculo del flujo para el grafo dado.

    Args:
        G (networkx.DiGraph): Grafo dirigido.

    Returns:
        tiempo_construccion (float): Tiempo de construcción del grafo en segundos.
        tiempo_calculo (float): Tiempo de cálculo del flujo en segundos.
    """
    start_time_construccion = time.time()
    construir_grafo(G)
    tiempo_construccion = time.time() - start_time_construccion

    start_time_calculo = time.time()
    flujo_maximo_corte_minimo(G)
    tiempo_calculo = time.time() - start_time_calculo

    return tiempo_construccion, tiempo_calculo

def dos_trenes_mismo_nodo(data):
    """
    Realiza la experimentación sobre dos trenes que salen del mismo nodo.

    Args:
        data (dict): Datos en formato JSON.

    Returns:
        tiempo_construccion (float): Tiempo de construcción del grafo en segundos.
        tiempo_calculo (float): Tiempo de cálculo del flujo en segundos.
        G_dos_trenes_mismo_nodo (networkx.DiGraph): Grafo dirigido con dos trenes saliendo del mismo nodo.
    """
    # Construir el grafo para dos trenes saliendo del mismo nodo
    G_dos_trenes_mismo_nodo = construir_grafo(data)

    # Medir el tiempo de construcción y cálculo
    tiempo_construccion, tiempo_calculo = medir_tiempo_construccion_calculo(G_dos_trenes_mismo_nodo)

    return tiempo_construccion, tiempo_calculo, G_dos_trenes_mismo_nodo


def experimentacion(data):
    """
    Realiza experimentaciones sobre diferentes casos utilizando los datos proporcionados.

    Args:
        data (dict): Datos en formato JSON.

    Returns:
        resultados (dict): Resultados de las experimentaciones.
    """
    resultados = {}

    # Experimentación sobre dos trenes que salen del mismo nodo
    tiempo_construccion, tiempo_calculo, G_dos_trenes_mismo_nodo = dos_trenes_mismo_nodo(data)
    resultados["dos_trenes_mismo_nodo"] = {"tiempo_construccion": tiempo_construccion, "tiempo_calculo": tiempo_calculo}

    return resultados


if __name__ == "__main__":
    # Cargar datos desde el archivo JSON
    with open("instances/toy_instance.json", "r") as file:
        data = json.load(file)

    # Ejecutar experimentaciones
    resultados = experimentacion(data)

    # Imprimir resultados
    for caso, resultado in resultados.items():
        print(f"--- {caso.capitalize()} ---")
        print(f"Tiempo de construcción del grafo: {resultado['tiempo_construccion']} segundos")
        print(f"Tiempo de cálculo del flujo: {resultado['tiempo_calculo']} segundos")
        print()

