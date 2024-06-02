import json
import networkx as nx
import matplotlib.pyplot as plt
from ploteo import plotear
import math

def main():
    filename = "instances/toy_instance.json"
    #filename = "instances/retiro-tigre-semana.json"

    with open(filename) as json_file:
        data = json.load(json_file)

    G = nx.DiGraph()
    
    for viaje_id, viaje_data in data["services"].items():
        nodo1_time = viaje_data["stops"][0]["time"]
        nodo1_station = viaje_data["stops"][0]["station"]
        nodo2_time = viaje_data["stops"][1]["time"]
        nodo2_station = viaje_data["stops"][1]["station"]
        nodo1_type = viaje_data["stops"][0]["type"]
        nodo2_type = viaje_data["stops"][1]["type"]

        if nodo1_type == "D" and nodo2_type == "A":
            G.add_edge(nodo1_time, nodo2_time, tipo="tren", cost=0, capacidad=float("inf"), demanda=math.ceil(viaje_data["demand"][0]/100))
        elif nodo1_type == "A" and nodo2_type == "D":
            G.add_edge(nodo2_time, nodo1_time, tipo="tren", cost=0, capacidad=float("inf"), demanda=math.ceil(viaje_data["demand"][0]/100))
        
        if nodo1_type == "A":
            G.add_node(nodo1_time, station=nodo1_station, type=nodo1_type, demanda=math.ceil(viaje_data["demand"][0]/100))
            G.add_node(nodo2_time, station=nodo2_station, type=nodo2_type, demanda=-math.ceil(viaje_data["demand"][0]/100))
        else:
            G.add_node(nodo1_time, station=nodo1_station, type=nodo1_type, demanda=-math.ceil(viaje_data["demand"][0]/100))
            G.add_node(nodo2_time, station=nodo2_station, type=nodo2_type, demanda=math.ceil(viaje_data["demand"][0]/100))

    estaciones_nodos = {}
    for nodo in G.nodes:
        estacion = G.nodes[nodo]["station"]
        if estacion not in estaciones_nodos:
            estaciones_nodos[estacion] = []
        estaciones_nodos[estacion].append(nodo)

    for estacion, nodos in estaciones_nodos.items():
        nodos_ordenados = sorted(nodos)
        for x in range(len(nodos_ordenados)):
            if G.nodes[nodos_ordenados[x]]["type"] == "D":
                primer_nodo_tipo_D = nodos_ordenados[x]
                break

        for i in range(len(nodos_ordenados)):
            nodo_conectado = False
            for j in range(len(nodos_ordenados)-i-1):
                if G.nodes[nodos_ordenados[i+j+1]]["type"] == "D":
                    G.add_edge(nodos_ordenados[i], nodos_ordenados[i+j+1], tipo="traspaso", cost=0, capacidad=float("inf"))
                    nodo_conectado = True
                    break
            if not nodo_conectado:
                G.add_edge(nodos_ordenados[i], primer_nodo_tipo_D, tipo="trasnoche", cost=1, capacidad=float("inf"))

    # Calcular flujo mínimo de costo
    flowDict = nx.min_cost_flow(G, "demanda", "capacidad", "cost")
    
    # Imprimir el resultado del flujo
    print(flowDict)

    plotear(G, flowDict)

    for arista in G.edges:
        if G.edges[arista]["tipo"] == "tren":
            print(arista)


if __name__ == "__main__":
    main()
