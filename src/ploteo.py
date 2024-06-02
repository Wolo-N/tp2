import networkx as nx
import matplotlib.pyplot as plt


def plotear(G:nx.graph):
    colores_estaciones = {
    "Retiro": "blue",
    "Tigre": "red",
    # Agrega más estaciones y colores según tus datos
    }

    colores_aristas = {
    "trasnoche": "red",
    "traspaso": "blue",
    "tren": "green",
    # Otros tipos de aristas y sus colores aquí
    }

    aristas_colores = [colores_aristas[G.edges[arista]["tipo"]] for arista in G.edges]
    # Crear una lista de colores para los nodos
    nodos_colores = [colores_estaciones[G.nodes[nodo]["station"]] for nodo in G.nodes]
    # Agregar leyenda para las estaciones
    for estacion, color in colores_estaciones.items():
        plt.scatter([], [], c=color, label=estacion)
    # Dibujar el grafo
    #pos = nx.spring_layout(G)  # Posiciones de los nodos
    # Position nodes using a layered layout to avoid compactness and to show trips going down
    pos = {}
    """
    y_positions = {
        'Retiro': [0, -5, -10, -15],
        'Tigre': [-2.5, -7.5, -12.5, -17.5]
    }
    i_retiro = 0
    i_tigre = 0
    for node in G.nodes:
        if G.nodes[node]["station"] == "Retiro":
            pos[node] = (0, y_positions['Retiro'][i_retiro])
            i_retiro += 1
        else:
            pos[node] = (5, y_positions['Tigre'][i_tigre])
            i_tigre += 1
    """
    estaciones_nodos = {}
    for nodo in G.nodes:
        estacion = G.nodes[nodo]["station"]
        if estacion not in estaciones_nodos:
            estaciones_nodos[estacion] = []
        estaciones_nodos[estacion].append(nodo)

    # Ordenar nodos dentro de cada estación por tiempo
    for estacion, nodos in estaciones_nodos.items():
        nodos_ordenados = sorted(nodos)
        
        # Agregar aristas dirigidas entre nodos adyacentes
        for i in range(len(nodos)):
            
            if estacion == "Retiro":
                if nodos_ordenados[i] == min(nodos_ordenados) or nodos_ordenados[i] == max(nodos_ordenados):
                    pos[nodos_ordenados[i]]= (0, nodos_ordenados[i]* -1/10)
                else:
                    pos[nodos_ordenados[i]]= (1, nodos_ordenados[i]* -1/10)
            else:
                if nodos_ordenados[i] == min(nodos_ordenados) or nodos_ordenados[i] == max(nodos_ordenados):
                    pos[nodos_ordenados[i]]= (6, nodos_ordenados[i]* -1/10)
                else:
                    pos[nodos_ordenados[i]]= (5, nodos_ordenados[i]* -1/10)

        



    nx.draw(G, pos, node_color=nodos_colores, edge_color=aristas_colores, with_labels=True, node_size=500)

    # Agregar leyenda para los tipos de aristas
    for tipo, color in colores_aristas.items():
        plt.scatter([], [], c=color, label=tipo)

    plt.legend()

    # Mostrar el gráfico
    plt.show()