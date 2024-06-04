import json
import networkx as nx
import matplotlib.pyplot as plt
import math

def plotear(G, flowDict):
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
    nodos_colores = [colores_estaciones.get(G.nodes[nodo].get("station", ""), "gray") for nodo in G.nodes]

    pos = {}
    estaciones_nodos = {}
    for nodo in G.nodes:
        estacion = G.nodes[nodo].get("station")
        if estacion:
            if estacion not in estaciones_nodos:
                estaciones_nodos[estacion] = []
            estaciones_nodos[estacion].append(nodo)
        else:
            pos[nodo] = (2, 0)  # Posición fija para nodos sin estación

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

    # Ajustar la posición del nodo "GarajeTrasnoche"
    max_x = max(pos[node][0] for node in pos)
    garaje_trasnoche_x = max_x + 3
    pos["GarajeTrasnoche"] = (garaje_trasnoche_x, 0)

    nx.draw(G, pos, node_color=nodos_colores, edge_color=aristas_colores, with_labels=True, node_size=500, font_size=8)

    for tipo, color in colores_aristas.items():
        plt.scatter([], [], c=color, label=tipo)

    plt.legend()

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
        
        demanda = math.ceil(viaje_data["demand"][0] / 100)

        if nodo1_type == "D" and nodo2_type == "A":
            G.add_edge(nodo1_time, nodo2_time, tipo="tren", capacidad=demanda, costo=0, demanda=demanda)
        elif nodo1_type == "A" and nodo2_type == "D":
            G.add_edge(nodo2_time, nodo1_time, tipo="tren", capacidad=demanda, costo=0, demanda=demanda)
        if nodo1_type == "A":
            G.add_node(nodo1_time, station=nodo1_station, type=nodo1_type, demanda=demanda)
            G.add_node(nodo2_time, station=nodo2_station, type=nodo2_type, demanda=-demanda)
        else:
            G.add_node(nodo1_time, station=nodo1_station, type=nodo1_type, demanda=-demanda)
            G.add_node(nodo2_time, station=nodo2_station, type=nodo2_type, demanda=demanda)

    estaciones_nodos = {}
    for nodo in G.nodes:
        estacion = G.nodes[nodo]["station"]
        if estacion not in estaciones_nodos:
            estaciones_nodos[estacion] = []
        estaciones_nodos[estacion].append(nodo)

    for estacion, nodos in estaciones_nodos.items():
        nodos_ordenados = sorted(nodos)
        flujo_entrante = sum(G[nodo_prev][nodo]["demanda"] for nodo_prev, nodo in G.in_edges(nodos))
        flujo_saliente = sum(G[nodo][nodo_next]["demanda"] for nodo, nodo_next in G.out_edges(nodos))
        flujo_net = flujo_entrante - flujo_saliente

        for i in range(len(nodos_ordenados)):
            if i < len(nodos_ordenados) - 1:
                nodo_actual = nodos_ordenados[i]
                nodo_siguiente = nodos_ordenados[i+1]
                if G.nodes[nodo_actual]["type"] == "A" and G.nodes[nodo_siguiente]["type"] == "D":
                    if not G.has_edge(nodo_actual, nodo_siguiente):
                        flujo_transferir = min(flujo_net, demanda)
                        G.add_edge(nodo_actual, nodo_siguiente, tipo="traspaso", capacidad=float("inf"), costo=1, demanda=flujo_transferir)
                        flujo_net -= flujo_transferir
                elif G.nodes[nodo_actual]["type"] == "D" and G.nodes[nodo_siguiente]["type"] == "A":
                    if not G.has_edge(nodo_siguiente, nodo_actual):
                        flujo_transferir = min(flujo_net, demanda)
                        G.add_edge(nodo_siguiente, nodo_actual, tipo="traspaso", capacidad=float("inf"), costo=1, demanda=flujo_transferir)
                        flujo_net -= flujo_transferir

        if len(nodos_ordenados) > 1:
            nodo_final = nodos_ordenados[-1]
            nodo_inicial = nodos_ordenados[0]
            if not G.has_edge(nodo_final, nodo_inicial):
                flujo_transferir = min(flujo_net, demanda)
                G.add_edge(nodo_final, nodo_inicial, tipo="trasnoche", capacidad=float("inf"), costo=2, demanda=flujo_transferir)
                flujo_net -= flujo_transferir

    flowDict = nx.min_cost_flow(G, "demanda", "capacidad", "costo")
    plotear(G, flowDict)

    print(flowDict)

    for arista in G.edges:
        if G.edges[arista]["tipo"] == "tren":
            print(arista)

if __name__ == "__main__":
    main()
