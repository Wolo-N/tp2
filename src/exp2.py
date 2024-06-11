import time
import json
import networkx as nx
import matplotlib.pyplot as plt
from core_functions import construir_grafo, flujo_maximo_corte_minimo, cambios_por_reparaciones, interpretacion_vagones, plot

def medir_tiempo_construccion_calculo(data):
    """
    Mide el tiempo de construcción del grafo y el tiempo de cálculo del flujo para los datos dados.

    Args:
        data (dict): Datos en formato JSON.

    Returns:
        tiempo_construccion (float): Tiempo de construcción del grafo en segundos.
        tiempo_calculo (float): Tiempo de cálculo del flujo en segundos.
        G (networkx.DiGraph): Grafo dirigido creado a partir de los datos proporcionados.
    """
    start_time_construccion = time.time()
    G = construir_grafo(data)
    tiempo_construccion = time.time() - start_time_construccion

    start_time_calculo = time.time()
    flujo_maximo_corte_minimo(G)
    tiempo_calculo = time.time() - start_time_calculo

    return tiempo_construccion, tiempo_calculo, G

def aumentar_demanda(data, factor):
    """
    Aumenta la demanda proporcionalmente en el dataset.

    Args:
        data (dict): Datos en formato JSON.
        factor (float): Factor de aumento de la demanda.

    Returns:
        dict: Datos con la demanda aumentada.
    """
    data_aumentada = data.copy()
    for servicio in data_aumentada["services"].values():
        servicio["demand"] = [d * factor for d in servicio["demand"]]
    return data_aumentada

def experimentacion_demanda(data, factores_demanda):
    """
    Realiza experimentaciones sobre diferentes variaciones de demanda utilizando los datos proporcionados.

    Args:
        data (dict): Datos en formato JSON.
        factores_demanda (list): Lista de factores de aumento de la demanda.

    Returns:
        resultados (dict): Resultados de las experimentaciones.
    """
    resultados = {}

    for factor in factores_demanda:
        data_aumentada = aumentar_demanda(data, factor)
        tiempo_construccion, tiempo_calculo, _ = medir_tiempo_construccion_calculo(data_aumentada)
        resultados[factor] = {"tiempo_construccion": tiempo_construccion, "tiempo_calculo": tiempo_calculo}

    return resultados

def graficar_resultados(resultados, factores_demanda):
    """
    Genera gráficos para visualizar los resultados de la experimentación.

    Args:
        resultados (dict): Resultados de las experimentaciones.
        factores_demanda (list): Lista de factores de aumento de la demanda.
    """
    tiempos_construccion = [resultados[factor]["tiempo_construccion"] for factor in factores_demanda]
    tiempos_calculo = [resultados[factor]["tiempo_calculo"] for factor in factores_demanda]

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(factores_demanda, tiempos_construccion, marker='o')
    plt.xlabel('Factor de Demanda')
    plt.ylabel('Tiempo de Construcción (s)')
    plt.title('Tiempo de Construcción del Grafo vs Factor de Demanda')

    plt.subplot(1, 2, 2)
    plt.plot(factores_demanda, tiempos_calculo, marker='o', color='r')
    plt.xlabel('Factor de Demanda')
    plt.ylabel('Tiempo de Cálculo del Flujo (s)')
    plt.title('Tiempo de Cálculo del Flujo vs Factor de Demanda')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Cargar datos desde el archivo JSON
    with open("instances/toy_instance.json", "r") as file:
        data = json.load(file)

    # Factores de aumento de la demanda
    factores_demanda = [1, 1.5, 2, 2.5, 3]

    # Ejecutar experimentaciones
    resultados = experimentacion_demanda(data, factores_demanda)

    # Imprimir resultados
    for factor, resultado in resultados.items():
        print(f"--- Factor de Demanda: {factor} ---")
        print(f"Tiempo de construcción del grafo: {resultado['tiempo_construccion']} segundos")
        print(f"Tiempo de cálculo del flujo: {resultado['tiempo_calculo']} segundos")
        print()

    # Graficar resultados
    graficar_resultados(resultados, factores_demanda)
