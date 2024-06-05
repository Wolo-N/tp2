import networkx as nx
import matplotlib.pyplot as plt


def plotear(G: nx.Graph, flowDict: dict, a):
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
    nodos_colores = [colores_estaciones[G.nodes[nodo]["station"]] for nodo in G.nodes]

    for estacion, color in colores_estaciones.items():
        plt.scatter([], [], c=color, label=estacion)

    pos = {}
    estaciones_nodos = {}
    for nodo in G.nodes:
        estacion = G.nodes[nodo]["station"]
        if estacion not in estaciones_nodos:
            estaciones_nodos[estacion] = []
        estaciones_nodos[estacion].append(nodo)

    for estacion, nodos in estaciones_nodos.items():
        nodos_ordenados = sorted(nodos, key=lambda nodo: G.nodes[nodo]["time"])        
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

    nx.draw(G, pos, node_color=nodos_colores, edge_color=aristas_colores, with_labels=False, node_size=500)

    for tipo, color in colores_aristas.items():
        plt.scatter([], [], c=color, label=tipo)

    plt.legend(loc="lower center")

    # Etiquetas de las aristas
    edge_labels = {}
    for u, v, d in G.edges(data=True):
        flujo = flowDict[u][v] if u in flowDict and v in flowDict[u] else 0
        capacidad = G.edges[(u,v)]["capacidad"]
        edge_labels[(u, v)] = f"{flujo}/{capacidad}"
    
    node_labels = {nodo: f"{nodo} ({G.nodes[nodo]['demanda']})" for nodo in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    if a == 0:
        plt.title("Devolución del algoritmo min_cost_flow")
        # Con adaptación y reducción de las cotas inferiores a 0 para que el algoritmo funcione.
    
    else:
        plt.title("Interpretación de los vagones")
    plt.show()