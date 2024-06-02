import json
import networkx as nx
import matplotlib.pyplot as plt
import math
from ploteo import plotear

def main():
    filename = "instances/toy_instance.json"
    # filename = "instances/retiro-tigre-semana.json"

    with open(filename) as json_file:
        data = json.load(json_file)

    G = nx.DiGraph()

    for viaje_id, viaje_data in data["services"].items():
        # Accede a los datos de cada viaje
        nodo1_time = viaje_data["stops"][0]["time"]
        nodo1_station = viaje_data["stops"][0]["station"]
        nodo2_time = viaje_data["stops"][1]["time"]
        nodo2_station = viaje_data["stops"][1]["station"]
        nodo1_type = viaje_data["stops"][0]["type"]
        nodo2_type = viaje_data["stops"][1]["type"]
        demanda = math.ceil(viaje_data["demand"][0] / 100)

        if nodo1_type == "D" and nodo2_type == "A":
            # Crea la arista de tipo "tren" desde nodo1 a nodo2
            G.add_edge(nodo1_time, nodo2_time, tipo="tren", demanda=demanda, capacidad=float("inf"), costo=0)
        elif nodo1_type == "A" and nodo2_type == "D":
            # Crea la arista de tipo "tren" desde nodo2 a nodo1
            G.add_edge(nodo2_time, nodo1_time, tipo="tren", demanda=demanda, capacidad=float("inf"), costo=0)

        G.add_node(nodo1_time, station=nodo1_station, type=nodo1_type)
        G.add_node(nodo2_time, station=nodo2_station, type=nodo2_type)

    # Crear un diccionario para agrupar nodos por estación
    estaciones_nodos = {}
    for nodo in G.nodes:
        estacion = G.nodes[nodo]["station"]
        if estacion not in estaciones_nodos:
            estaciones_nodos[estacion] = []
        estaciones_nodos[estacion].append(nodo)

    # Ordenar nodos dentro de cada estación por tiempo
    for estacion, nodos in estaciones_nodos.items():
        nodos_ordenados = sorted(nodos)

        # Encontrar el primer nodo de tipo "D" para la arista "trasnoche"
        primer_nodo_tipo_D = None
        for nodo in nodos_ordenados:
            if G.nodes[nodo]["type"] == "D":
                primer_nodo_tipo_D = nodo
                break

        # Agregar aristas dirigidas entre nodos adyacentes
        for i in range(len(nodos_ordenados)):
            nodo_actual = nodos_ordenados[i]
            if G.nodes[nodo_actual]["type"] == "D":
                nodo_siguiente = None
                for j in range(i + 1, len(nodos_ordenados)):
                    if G.nodes[nodos_ordenados[j]]["type"] == "D":
                        nodo_siguiente = nodos_ordenados[j]
                        break

                if nodo_siguiente:
                    G.add_edge(nodo_actual, nodo_siguiente, tipo="traspaso", capacidad=float("inf"), costo=0)
                else:
                    if primer_nodo_tipo_D and nodo_actual != primer_nodo_tipo_D and nodo_actual != nodos_ordenados[-1]:
                        G.add_edge(nodo_actual, primer_nodo_tipo_D, tipo="trasnoche", capacidad=float("inf"), costo=1)

    plotear(G)

    flowDict = nx.min_cost_flow(G, "demanda", "capacidad", "costo")
    print("Flujo óptimo:")
    for u in flowDict:
        for v in flowDict[u]:
            if flowDict[u][v] > 0:
                print(f"De {u} a {v}: {flowDict[u][v]}")

if __name__ == "__main__":
    main()
