import json
import networkx as nx
import matplotlib.pyplot as plt
import math
from ploteo import plotear

def plotear(G: nx.Graph, flowDict: dict):
    colores_estaciones = {
        "Retiro": "blue",
        "Tigre": "red",
    }

    colores_aristas = {
        "trasnoche": "red",
        "traspaso": "blue",
        "tren": "green",
        "garaje_trasnoche": "purple"
    }

    aristas_colores = [colores_aristas[G.edges[arista]["tipo"]] for arista in G.edges]
    
    # Manejar el caso en el que el nodo no tiene el atributo "station"
    nodos_colores = []
    for nodo in G.nodes:
        if "station" in G.nodes[nodo]:
            nodos_colores.append(colores_estaciones[G.nodes[nodo]["station"]])
        else:
            nodos_colores.append("gray")  # Color gris para nodos sin atributo "station"

    for estacion, color in colores_estaciones.items():
        plt.scatter([], [], c=color, label=estacion)

    pos = {}
    estaciones_nodos = {}
    for nodo in G.nodes:
        estacion = G.nodes[nodo].get("station")  # Usamos get para manejar el caso en el que el atributo "station" no exista
        if estacion not in estaciones_nodos:
            estaciones_nodos[estacion] = []
        estaciones_nodos[estacion].append(nodo)

    for estacion, nodos in estaciones_nodos.items():
        nodos_ordenados = sorted(nodos)
        separacion_vertical = 0.5

        for i, nodo in enumerate(nodos_ordenados):
            if estacion == "Retiro":
                if i == 0 or i == len(nodos_ordenados) - 1:
                    pos[nodo] = (0, i * -separacion_vertical)
                else:
                    pos[nodo] = (1, i * -separacion_vertical)
            else:
                if i == 0 or i == len(nodos_ordenados) - 1:
                    pos[nodo] = (6, i * -separacion_vertical)
                else:
                    pos[nodo] = (5, i * -separacion_vertical)

    nx.draw(G, pos, node_color=nodos_colores, edge_color=aristas_colores, with_labels=True, node_size=500)

    for tipo, color in colores_aristas.items():
        plt.scatter([], [], c=color, label=tipo)

    plt.legend()

    # Etiquetas de las aristas
    edge_labels = {}
    for u, v, d in G.edges(data=True):
        flujo = flowDict[u][v] if u in flowDict and v in flowDict[u] else 0
        edge_labels[(u, v)] = f"Flow={flujo}"

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.show()




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
            G.add_edge(nodo1_time, nodo2_time, tipo="tren", lower_bound=0, upper_bound=float("inf"), cost=0, capacidad=float("inf"), demanda=math.ceil(viaje_data["demand"][0]/100))
        elif nodo1_type == "A" and nodo2_type == "D":
            G.add_edge(nodo2_time, nodo1_time, tipo="tren", lower_bound=0, upper_bound=float("inf"), cost=0, capacidad=float("inf"), demanda=math.ceil(viaje_data["demand"][0]/100))
        
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
                    G.add_edge(nodos_ordenados[i], nodos_ordenados[i+j+1], tipo="traspaso", lower_bound=0, upper_bound=float("inf"), cost=0, capacidad=float("inf"))
                    nodo_conectado = True
                    break
            if not nodo_conectado:
                G.add_edge(nodos_ordenados[i], primer_nodo_tipo_D, tipo="trasnoche", lower_bound=0, upper_bound=float("inf"), cost=0, capacidad=float("inf"))

    # Crear nodo de "garaje de trasnoche"
    garaje_trasnoche = "GarajeTrasnoche"
    G.add_node(garaje_trasnoche)

    # Conectar nodo de "garaje de trasnoche" a los nodos finales con aristas dirigidas
    for nodo in G.nodes:
        if G.out_degree(nodo) == 0:
            G.add_edge(garaje_trasnoche, nodo, tipo="garaje_trasnoche", lower_bound=0, upper_bound=float("inf"), cost=0, capacidad=float("inf"))
        if G.in_degree(nodo) == 0:
            G.add_edge(nodo, garaje_trasnoche, tipo="garaje_trasnoche", lower_bound=0, upper_bound=float("inf"), cost=0, capacidad=float("inf"))

    # Resolver el problema de flujo y obtener los resultados
    flowDict = nx.min_cost_flow(G, "demanda", "capacidad", "cost")

    # Ajustar los flujos para equilibrar el flujo en el nodo de "garaje de trasnoche"
    for nodo, flujo_dict in flowDict.items():
        for vecino, flujo in flujo_dict.items():
            if nodo == garaje_trasnoche:
                G.edges[nodo, vecino]["lower_bound"] = -flujo
                G.edges[nodo, vecino]["upper_bound"] = float("inf")
            elif vecino == garaje_trasnoche:
                G.edges[nodo, vecino]["lower_bound"] = 0
                G.edges[nodo, vecino]["upper_bound"] = flujo

    # Resolver nuevamente el problema de flujo con los ajustes
    flowDict = nx.min_cost_flow(G, "demanda", "capacidad", "cost")

    # Imprimir el resultado del flujo
    print(flowDict)

    # Plotear el grafo
    plotear(G, flowDict)

if __name__ == "__main__":
    main()
