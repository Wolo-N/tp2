import networkx as nx
import matplotlib.pyplot as plt


def plotear(G:nx.graph):
    colores_estaciones = {
    "Retiro": "blue",
    "Tigre": "red",
    # Agrega más estaciones y colores según tus datos
    }

    colores_aristas = {
    "Trasnoche": "red",
    "Traspaso": "blue",
    "Tren": "green",
    # Otros tipos de aristas y sus colores aquí
    }

    aristas_colores = [colores_aristas[G.edges[arista]["tipo"]] for arista in G.edges]
    # Crear una lista de colores para los nodos
    nodos_colores = [colores_estaciones[G.nodes[nodo]["station"]] for nodo in G.nodes]
    # Agregar leyenda para las estaciones
    for estacion, color in colores_estaciones.items():
        plt.scatter([], [], c=color, label=estacion)
    # Dibujar el grafo
    pos = nx.spring_layout(G)  # Posiciones de los nodos

    nx.draw(G, pos, node_color=nodos_colores, edge_color=aristas_colores, with_labels=True, node_size=500)

    # Agregar leyenda para los tipos de aristas
    for tipo, color in colores_aristas.items():
        plt.scatter([], [], c=color, label=tipo)

    plt.legend()

    # Mostrar el gráfico
    plt.show()