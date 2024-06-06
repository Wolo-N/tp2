import json
import networkx as nx
import matplotlib.pyplot as plt
import math

# Función para construir el grafo a partir de los datos proporcionados
def construir_grafo(data):
    G = nx.DiGraph()
    for viaje_id, viaje_data in data["services"].items():
        nodo1_time = viaje_data["stops"][0]["time"]
        nodo1_station = viaje_data["stops"][0]["station"]
        nodo2_time = viaje_data["stops"][1]["time"]
        nodo2_station = viaje_data["stops"][1]["station"]
        nodo1_type = viaje_data["stops"][0]["type"]
        nodo2_type = viaje_data["stops"][1]["type"]
        max_capacidad = data["rs_info"]["max_rs"]
        
        demanda = math.ceil(viaje_data["demand"][0]/100)
        
        if nodo1_type == "A":
            # Agregar nodos con demanda positiva o negativa según el tipo de estación
            G.add_node(f"{nodo1_time}_{nodo1_station}_{nodo1_type}", time=nodo1_time, station=nodo1_station, type=nodo1_type, demanda=-demanda)
            G.add_node(f"{nodo2_time}_{nodo2_station}_{nodo2_type}", time=nodo2_time, station=nodo2_station, type=nodo2_type, demanda=demanda)
        else:
            G.add_node(f"{nodo1_time}_{nodo1_station}_{nodo1_type}", time=nodo1_time, station=nodo1_station, type=nodo1_type, demanda=demanda)
            G.add_node(f"{nodo2_time}_{nodo2_station}_{nodo2_type}", time=nodo2_time, station=nodo2_station, type=nodo2_type, demanda=-demanda)
        
        if nodo1_type == "D" and nodo2_type == "A":
            # Agregar aristas con capacidad y costo
            G.add_edge(f"{nodo1_time}_{nodo1_station}_{nodo1_type}", f"{nodo2_time}_{nodo2_station}_{nodo2_type}", tipo="tren", capacidad=max_capacidad - demanda, costo=0)
        elif nodo1_type == "A" and nodo2_type == "D":
            G.add_edge(f"{nodo2_time}_{nodo2_station}_{nodo2_type}", f"{nodo1_time}_{nodo1_station}_{nodo1_type}", tipo="tren", capacidad=max_capacidad - demanda, costo=0)
    
    estaciones_nodos = {}
    for nodo in G.nodes:
        estacion = G.nodes[nodo]["station"]
        if estacion not in estaciones_nodos:
            estaciones_nodos[estacion] = []
        estaciones_nodos[estacion].append(nodo)

    for estacion, nodos in estaciones_nodos.items():
        nodos_ordenados = sorted(nodos, key=lambda nodo: G.nodes[nodo]["time"])

        for i in range(len(nodos_ordenados) - 1):
            G.add_edge(nodos_ordenados[i], nodos_ordenados[i + 1], tipo="traspaso", capacidad=float("inf"), costo=0)
        G.add_edge(nodos_ordenados[-1], nodos_ordenados[0], tipo="trasnoche", capacidad=float("inf"), costo=1)
    
    return G

# Función para calcular el flujo máximo y el corte mínimo
def flujo_maximo_corte_minimo(G):
    flowDict = nx.min_cost_flow(G, "demanda", "capacidad", "costo")
    
    for u, v in G.edges:
        if G.edges[u, v]["tipo"] == "tren":
            flowDict[u][v] += G.nodes[u]["demanda"]
    
    return flowDict


def plotear(G: nx.Graph, flowDict: dict, a, filename):
    estaciones = set(nx.get_node_attributes(G, 'station').values())

    if estaciones == {"Retiro", "Tigre"}:
        colores_estaciones = {
            "Retiro": "blue",
            "Tigre": "red",
        }
    else: 
        colores_estaciones = {
            "La Plata": "blue", 
            "Hospital San Juan de Dios": "red",
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
            if estacion == "Retiro" or estacion == "La Plata":
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
        plt.text(0.5, -0.1, f'Archivo: {filename}\nCon adaptación y reducción de las cotas inferiores a 0 para que el algoritmo funcione.', fontsize=10, color='gray', style='italic', ha='center', transform=plt.gca().transAxes)
    else:
        plt.title("Interpretación de los vagones")
        plt.text(0.5, -0.1, f'Archivo: {filename}', fontsize=10, color='gray', style='italic', ha='center', transform=plt.gca().transAxes)
    
    plt.show()


# Función principal
def main():
    archivos = ["instances/new_instance.json", "instances/toy_instance.json", "instances/retiro-tigre-semana.json", "instances/test_instance_ward.json"]
    for filename in archivos: 
        with open(filename) as json_file:
            data = json.load(json_file)
        
        # Construye el grafo
        G = construir_grafo(data)
        
        # Calcula el flujo máximo y el corte mínimo
        flowDict = flujo_maximo_corte_minimo(G)

        # Plotteo exacto lo que tira min_cost_flow.
        # El 0 o el 1 pasado como parámetro solamente cambia los títulos.
        plotear(G, flowDict, 0, filename) 

        # Para la interpretacion, cambio los flujos para que representen los vagones.
        for u, v in G.edges:
            if G.edges[u, v]["tipo"] == "tren":
                # Sumar la demanda del nodo receptor al flujo existente.
                flowDict[u][v] += G.nodes[u]["demanda"]
        # Plotteo con la representación medida en vagones.
        plotear(G, flowDict, 1, filename)

if __name__ == "__main__":
    main()
