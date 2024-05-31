import networkx as nx
import matplotlib.pyplot as plt
print("Libreria networkx importada correctamente")

G = nx.Graph()
DiG = nx.DiGraph()
'''
def grafo_a_mano():
    G.add_node(1)
    G.add_nodes_from([2,3,4])

    G.add_edge(1,2)
    G.add_edges_from([(2,3), (3,4)])

    print("Numero de nodos: ", G.number_of_nodes)
    print("Numero de aristas: ", G.number_of_edges)

    print("Nodos: ", G.nodes())
    print("Aristas: ", G.edges())

    neighbors = list(G.neighbors(1))
    print(neighbors)

nx.draw(G, with_labels=True, node_color= 'lightblue', node_size= 500, edge_color='#909090')
#plt.show()
'''
def grafo_completo(n):
    G = nx.complete_graph(n)
    nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, edge_color='#909090')
    plt.show()

# Solicitar el valor de n al usuario
#n = int(input("Introduce el número de nodos para el grafo completo: "))
#grafo_completo(n)
'''
def grafo_bipartito(n1, n2):
    B = nx.complete_bipartite_graph(n1, n2)
    pos = {node: (1, i) for i, node in enumerate(range(n1))}
    pos.update({node: (2, i) for i, node in enumerate(range(n1, n1 + n2))})
    nx.draw(B, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='#909090')
    plt.show()

# Solicitar el valor de n1 y n2 al usuario
#n1 = int(input("Introduce el número de nodos para el primer conjunto: "))
#n2 = int(input("Introduce el número de nodos para el segundo conjunto: "))
#grafo_bipartito(n1, n2)


# Crear un grafo no dirigido
G = nx.Graph()

# Añadir nodos
G.add_node('A')
G.add_node('B')
G.add_node('C')

# Añadir aristas con pesos
G.add_edge('A', 'B', weight=4.7)
G.add_edge('B', 'C', weight=1.2)
G.add_edge('B', 'C', weight=5.0)  # Esta línea sobrescribe el peso anterior

# Obtener el peso de la arista A-B
peso_AB = G['A']['B']['weight']
#print("Peso de la arista A-B:", peso_AB)

# Encontrar el camino más corto teniendo en cuenta los pesos
camino_minimo = nx.shortest_path(G, source='A', target='C', weight='weight')
#print("Camino mínimo de A a C:", camino_minimo)

# Si deseas graficar el grafo para visualizarlo
pos = nx.spring_layout(G)  # Posicionamiento automático de los nodos
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=16, font_color="darkred")
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Grafo No Dirigido con Pesos")
plt.show()


# Clase práctica:
# Ejercicio 1: Dado un digrafo D y dos vértices s y t, se busca encontrar la máxima cantidad de caminos que vayan de s a t sin repetir aristas. 
def max_caminos(DiG, s, t):
    # Creo la red residual
    residual = nx.DiGraph(DiG)
    
    # Añadir capacidad 1 a todas las aristas
    for u, v in residual.edges():
        residual[u][v]['capacity'] = 1
    
    flujo_maximo = nx.maximum_flow_value(residual, s, t, capacity='capacity')
    
    return flujo_maximo

# Ejemplo de uso
DiG = nx.DiGraph()
DiG.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)])

s = 1  # Nodo de inicio
t = 4  # Nodo de destino

max_caminos_resultado = max_caminos(DiG, s, t)
print("Máxima cantidad de caminos de s a t sin repetir aristas:", max_caminos_resultado)

def visualizar_grafo(DiG, s, t):
    pos = nx.spring_layout(DiG)
    nx.draw(DiG, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='#909090')
    plt.title("Dígrafo con caminos de {} a {}".format(s, t))
    plt.show()

visualizar_grafo(DiG, s, t)
'''
# Ejercicio 2: ahora queremos la máxima cantidad de caminos que no pasen dos veces por el mismo nodo.
# Debería agregar una arista entre cada nodo:
'''
def max_caminos(DiG, s, t):
    # Creo la red residual
    residual = nx.DiGraph(DiG)
    
    # Añadir capacidad 1 a todas las aristas
    for u, v in residual.edges():
        residual.add_edges_from()
        residual[u][v]['capacity'] = 1
    
    flujo_maximo = nx.maximum_flow_value(residual, s, t, capacity='capacity')
    
    return flujo_maximo
'''

# Ejercicio extra: flujo de costo mínimo: 
def min_cost_flow(DiG, s, t):
    # Crear la red residual
    residual = nx.DiGraph(DiG)
    
    # Calcular el flujo de costo mínimo
    flow_cost = nx.algorithms.flow.min_cost_flow_cost(residual, s, t, weight='weight')
    
    return flow_cost


# Crear el grafo dirigido
G = nx.DiGraph()
G.add_edge('s', 'a', capacity=1, weight=3)  # Arista de s a a con capacidad 1 y costo 3
G.add_edge('s', 'b', capacity=1, weight=2)  # Arista de s a b con capacidad 1 y costo 2
G.add_edge('a', 't', capacity=1, weight=1)  # Arista de a a t con capacidad 1 y costo 1
G.add_edge('b', 't', capacity=1, weight=2)  # Arista de b a t con capacidad 1 y costo 2

# Resolver el flujo de costo mínimo
min_cost = min_cost_flow(G, 's', 't')
print("Flujo de costo mínimo:", min_cost)

# Dibujar el grafo
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=12, font_weight='bold', arrowsize=20)

# Agregar etiquetas de peso a las aristas
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.title("Grafo de Flujo de Costo Mínimo")
plt.show()
