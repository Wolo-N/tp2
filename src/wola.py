import json
import networkx as nx
import matplotlib.pyplot as plt

def main():
    data_json = '''
    {"services": {"1": {"stops": [{"time": 289, "station": "Retiro", "type": "D"}, {"time": 343, "station": "Tigre", "type": "A"}], "demand": [500]}, "2": {"stops": [{"time": 304, "station": "Retiro", "type": "D"}, {"time": 358, "station": "Tigre", "type": "A"}], "demand": [500]}, "3": {"stops": [{"time": 245, "station": "Tigre", "type": "D"}, {"time": 299, "station": "Retiro", "type": "A"}], "demand": [500]}, "4": {"stops": [{"time": 260, "station": "Tigre", "type": "D"}, {"time": 314, "station": "Retiro", "type": "A"}], "demand": [500]}}, "stations": ["Tigre", "Retiro"], "cost_per_unit": {"Tigre": 1.0, "Retiro": 1.0}, "rs_info": {"capacity": 100, "max_rs": 25}}
    '''

    data = json.loads(data_json)

    # Ordenar los servicios según su tiempo de forma ascendente
    sorted_services = sorted(data["services"].items(), key=lambda x: min(stop["time"] for stop in x[1]["stops"]))

    # Crear el grafo dirigido
    G = nx.DiGraph()

    # Conjunto para mantener un registro de los nodos ya agregados
    added_nodes = set()

    # Add nodes and edges based on services
    for service_id, service_data in sorted_services:
        stops = service_data["stops"]
        demand = service_data["demand"][0]
        capacity = data["rs_info"]["capacity"]
        units_needed = demand // capacity
        
        # Agregar nodos según el orden de tiempo
        for stop in sorted(stops, key=lambda x: x["time"]):
            node = (service_id, stop["time"], stop["station"], stop["type"])
            if node not in added_nodes:
                G.add_node(node)
                added_nodes.add(node)

        # Add edges
        for i in range(len(stops) - 1):
            dep_node = (service_id, stops[i]["time"], stops[i]["station"], stops[i]["type"])
            arr_node = (service_id, stops[i+1]["time"], stops[i+1]["station"], stops[i+1]["type"])
            G.add_edge(dep_node, arr_node, lower_bound=units_needed, upper_bound=data["rs_info"]["max_rs"], cost=0)

    # Add transfer edges within stations
    for station in data["stations"]:
        station_nodes = sorted([n for n in G.nodes if n[2] == station], key=lambda x: x[1])
        for i in range(len(station_nodes) - 1):
            G.add_edge(station_nodes[i], station_nodes[i + 1], lower_bound=0, upper_bound=float('inf'), cost=0)

    # Add overnight edges
    for station in data["stations"]:
        station_nodes = [n for n in G.nodes if n[2] == station]
        first_event = min(station_nodes, key=lambda x: x[1])
        last_event = max(station_nodes, key=lambda x: x[1])
        is_arrival = first_event[3] == "A"
        is_departure = last_event[3] == "D"
        if is_arrival and is_departure:
            G.add_edge(last_event, first_event, lower_bound=0, upper_bound=float('inf'), cost=data["cost_per_unit"][station])

    # Visualización
    plt.figure(figsize=(12, 8))

    # Posicionamiento de nodos
    pos = {}
    for node in G.nodes:
        if node[2] == "Retiro":  # Si es un nodo de Retiro
            pos[node] = (0, node[1])  # Colocar en el lado izquierdo
        elif node[2] == "Tigre":  # Si es un nodo de Tigre
            pos[node] = (5, node[1])  # Colocar en el lado derecho

    # Dibujar los nodos y aristas
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=10, font_weight="bold", arrowsize=20)

    # Etiquetas de las aristas
    edge_labels = {(u, v): f"lb={d['lower_bound']}, ub={d['upper_bound']}, cost={d['cost']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Mostrar el grafo
    plt.title("Directed Graph of Railway Services")
    plt.show()

if __name__ == "__main__":
    main()
