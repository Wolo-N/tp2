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
    # filename = "instances/retiro-tigre-semana.json"

    with open(filename) as json_file:
        data = json.load(json_file)

    G = nx.DiGraph()

    # Process each service in the data
    for viaje_id, viaje_data in data["services"].items():
        nodo1_time = viaje_data["stops"][0]["time"]
        nodo1_station = viaje_data["stops"][0]["station"]
        nodo2_time = viaje_data["stops"][1]["time"]
        nodo2_station = viaje_data["stops"][1]["station"]
        nodo1_type = viaje_data["stops"][0]["type"]
        nodo2_type = viaje_data["stops"][1]["type"]

        demand = math.ceil(viaje_data["demand"][0] / 100)
        
        # Add train edges with appropriate demand
        if nodo1_type == "D" and nodo2_type == "A":
            G.add_edge((nodo1_station, nodo1_time), (nodo2_station, nodo2_time), tipo="tren", capacidad=float("inf"), costo=0, demanda=demand)
        elif nodo1_type == "A" and nodo2_type == "D":
            G.add_edge((nodo2_station, nodo2_time), (nodo1_station, nodo1_time), tipo="tren", capacidad=float("inf"), costo=0, demanda=demand)

        # Add nodes with demand attribute
        if nodo1_type == "A":
            G.add_node((nodo1_station, nodo1_time), station=nodo1_station, demanda=demand)
            G.add_node((nodo2_station, nodo2_time), station=nodo2_station, demanda=-demand)
        else:
            G.add_node((nodo1_station, nodo1_time), station=nodo1_station, demanda=-demand)
            G.add_node((nodo2_station, nodo2_time), station=nodo2_station, demanda=demand)

    # Group nodes by station and sort by time
    estaciones_nodos = {}
    for nodo in G.nodes:
        estacion = nodo[0]
        if estacion not in estaciones_nodos:
            estaciones_nodos[estacion] = []
        estaciones_nodos[estacion].append(nodo)

    # Add transfer and overnight edges
    for estacion, nodos in estaciones_nodos.items():
        nodos_ordenados = sorted(nodos, key=lambda x: x[1])

        for i in range(len(nodos_ordenados) - 1):
            G.add_edge(nodos_ordenados[i], nodos_ordenados[i + 1], tipo="traspaso", capacidad=float("inf"), costo=0)
        
        # Add overnight edge
        if len(nodos_ordenados) > 1:
            G.add_edge(nodos_ordenados[-1], nodos_ordenados[0], tipo="trasnoche", capacidad=float("inf"), costo=1)

    # Convert demand node attributes to imbalance for min_cost_flow
    demand_dict = {nodo: G.nodes[nodo].get("demanda", 0) for nodo in G.nodes}

    # Ensure the demand attribute is correctly referenced in the nodes
    nx.set_node_attributes(G, demand_dict, 'demand')

    # Compute minimum cost flow
    flowDict = nx.min_cost_flow(G, demand='demand', capacity='capacidad', weight='costo')
    
    # Plot the graph with flows
    plotear(G, flowDict)  # Ensure plotear is defined or imported if used

    # Print the result
    print(flowDict)

if __name__ == "__main__":
    main()
