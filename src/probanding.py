import json
import networkx as nx
import matplotlib.pyplot as plt

def main():
    # Archivo de ejemplo (puedes cambiarlo a "instances/retiro-tigre-semana.json")
    filename = "instances/toy_instance.json"

    with open(filename) as json_file:
        data = json.load(json_file)

    # Crear el grafo dirigido
    G = nx.DiGraph()

    # Inicializar conjuntos de nodos para Retiro y Tigre
    retiro_nodes = {"A": [], "D": []}
    tigre_nodes = {"A": [], "D": []}

    # Procesar los datos del archivo
    for service in data["services"]:
        stops = data["services"][service]["stops"]
        for stop in stops:
            node = f"{stop['station']}_{stop['type']}_{stop['time']}"
            if stop['station'] == "Retiro":
                retiro_nodes[stop['type']].append((stop['time'], node))
            elif stop['station'] == "Tigre":
                tigre_nodes[stop['type']].append((stop['time'], node))
            G.add_node(node, station=stop['station'], type=stop['type'], time=stop['time'])

    # Ordenar los nodos por tiempo
    for node_type in ["A", "D"]:
        retiro_nodes[node_type].sort()
        tigre_nodes[node_type].sort()

    # Crear aristas entre nodos de diferentes subregiones
    def create_edges_between_subregions(retiro_nodes, tigre_nodes):
        for retiro_node in retiro_nodes:
            for tigre_node in tigre_nodes:
                if retiro_node[0] < tigre_node[0]:  # Solo conectar si el nodo de Retiro es anterior al de Tigre
                    # Añadir arista solo si el nodo de Retiro es de tipo 'D' y el nodo de Tigre es nuevo
                    if retiro_node[1].split('_')[1] == 'D' and not G.has_node(tigre_node[1]):
                        G.add_edge(retiro_node[1], tigre_node[1], weight=0)

    # Conectar Retiro a Tigre
    create_edges_between_subregions(retiro_nodes["D"], tigre_nodes["A"])


    # Conectar Retiro a Tigre
    create_edges_between_subregions(retiro_nodes["D"], tigre_nodes["A"])
    create_edges_between_subregions(retiro_nodes["A"], tigre_nodes["D"])

    # Mostrar los nodos y aristas del grafo
    print("Nodos del grafo:")
    print(G.nodes(data=True))
    print("\nAristas del grafo:")
    print(G.edges(data=True))

    # Visualizar el grafo
    pos = {}
    pos.update((node[1], (1, i)) for i, node in enumerate(retiro_nodes["A"] + retiro_nodes["D"]))
    pos.update((node[1], (2, i)) for i, node in enumerate(tigre_nodes["A"] + tigre_nodes["D"]))
    
    edge_labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Grafo con Aristas Dentro de la Misma Subregión (Ordenado por Tiempo)")
    plt.show()

if __name__ == "__main__":
    main()
