import networkx as nx
import matplotlib.pyplot as plt
import math

def construir_grafo(data):
	"""
	Función para construir el grafo a partir de los datos proporcionados.

	Args:
		data (.json): archivo en formato json de donde extraeremos los datos.

	Returns:
		G (networkx DiGraph): Grafo dirigido creado a partir de los datos proporcionados.
		Cada nodo representa una parada de tren con atributos como tiempo, estación, tipo y demanda.
		Las aristas representan las conexiones entre las paradas con atributos como tipo, capacidad y costo.
	"""

	G = nx.DiGraph()

	# Extraemos la informacion de los datasets
	for viaje_id, viaje_data in data["services"].items():
		nodo1_time = viaje_data["stops"][0]["time"]
		nodo1_station = viaje_data["stops"][0]["station"]
		nodo2_time = viaje_data["stops"][1]["time"]
		nodo2_station = viaje_data["stops"][1]["station"]
		nodo1_type = viaje_data["stops"][0]["type"]
		nodo2_type = viaje_data["stops"][1]["type"]
		max_capacidad = data["rs_info"]["max_rs"]

		#Fijamos la demanda
		demanda = math.ceil(viaje_data["demand"][0]/data["rs_info"]["capacity"])

		# Agregamos nodos con demanda positiva o negativa según el tipo de estación
		if nodo1_type == "A":
			G.add_node(f"{nodo1_time}_{nodo1_station}_{nodo1_type}", time=nodo1_time, station=nodo1_station, type=nodo1_type, demanda=-demanda)
			G.add_node(f"{nodo2_time}_{nodo2_station}_{nodo2_type}", time=nodo2_time, station=nodo2_station, type=nodo2_type, demanda=demanda)
		else:
			G.add_node(f"{nodo1_time}_{nodo1_station}_{nodo1_type}", time=nodo1_time, station=nodo1_station, type=nodo1_type, demanda=demanda)
			G.add_node(f"{nodo2_time}_{nodo2_station}_{nodo2_type}", time=nodo2_time, station=nodo2_station, type=nodo2_type, demanda=-demanda)

		# Agregamos aristas con capacidad y costo
		if nodo1_type == "D" and nodo2_type == "A":
			G.add_edge(f"{nodo1_time}_{nodo1_station}_{nodo1_type}", f"{nodo2_time}_{nodo2_station}_{nodo2_type}", tipo="tren", capacidad=max_capacidad - demanda, costo=0)
		elif nodo1_type == "A" and nodo2_type == "D":
			G.add_edge(f"{nodo2_time}_{nodo2_station}_{nodo2_type}", f"{nodo1_time}_{nodo1_station}_{nodo1_type}", tipo="tren", capacidad=max_capacidad - demanda, costo=0)

		# Agregamos las aristas de traspaso a la mañana
		#G.add_edge

	estaciones_nodos = {}
	# Agrupamos los nodos por estación
	for nodo in G.nodes:
		estacion = G.nodes[nodo]["station"]
		if estacion not in estaciones_nodos:
			estaciones_nodos[estacion] = []
		estaciones_nodos[estacion].append(nodo)

	# Ordenamos los nodos por tiempo.
	for estacion, nodos in estaciones_nodos.items():
		nodos_ordenados = sorted(nodos, key=lambda nodo: G.nodes[nodo]["time"])

		# Creamos las aristas de traspaso
		for i in range(len(nodos_ordenados) - 1):
			
			G.add_edge(nodos_ordenados[i], nodos_ordenados[i + 1], tipo="traspaso", capacidad=float("inf"), costo=0)

		# Creamos las aristas de traspaso
		G.add_edge(nodos_ordenados[-1], nodos_ordenados[0], tipo="trasnoche", capacidad=float("inf"), costo=1)
	
	G.add_edge(estaciones_nodos["Retiro"][0],estaciones_nodos["Tigre"][0],tipo="trasnoche", capacidad=float("inf"),costo="1")
	G.add_edge(estaciones_nodos["Tigre"][0],estaciones_nodos["Retiro"][0],tipo="trasnoche",capacidad=float("inf"), costo="1")


	return G



def flujo_maximo_corte_minimo(G):
	"""
	Calcula el flujo máximo y el corte mínimo en un grafo dirigido utilizando el algoritmo de costo mínimo.

	Parámetros:
	- G (networkx.DiGraph): Grafo dirigido creado a partir de instancia.

	Returns:
	- flowDict (dict): Diccionario con claves: (origen y destino), y valores = flujo en cada arista.
	"""
	flowDict = nx.min_cost_flow(G, "demanda", "capacidad", "costo")

	return flowDict


def cambios_por_reparaciones (estacion_reparacion, capacidad_limitada, G):
	"""
	Modifica el grafo G  y su flujo para corregir por reparaciones en una estación específica,
	limitando la capacidad de traspaso nocturno y añadiendo aristas de trenR para redirigir el flujo de trenes.

	Parámetros:
	- estacion_en_reparacion (str): Nombre de la estación donde se están realizando reparaciones.
	- capacidad_limitada (int): Capacidad máxima permitida para las aristas de traspaso nocturno en la estación en reparación.
	- G (networkx.DiGraph): Grafo dirigido que representa la red de transporte.

	Retorna:
	- G (networkx.DiGraph): El grafo adaptado a las nuevas restricciones.
	"""

	aristas_trasnoche = []
	for u,v, in G.edges():
		if G.edges[u,v]["tipo"] == "trasnoche":
			aristas_trasnoche.append(((u,v), G.nodes[u]["station"])) #agrego la arista y de donde sale 

	# Verifica si la estación en reparación es la segunda estación de traspaso nocturno
	if estacion_reparacion == G.nodes[aristas_trasnoche[1][0][0]]["station"]:
		# Limitamos la capacidad de la arista de traspaso nocturno
		G.edges[aristas_trasnoche[1][0][0],aristas_trasnoche[1][0][1]]["capacidad"] = capacidad_limitada
		# Aliviamos el flujo redirigiendolo con TrenesR
		G.add_edge(aristas_trasnoche[1][0][0],aristas_trasnoche[0][0][0], tipo="trenR",capacidad=float("inf"),costo=0)
		G.add_edge(aristas_trasnoche[0][0][1],aristas_trasnoche[1][0][1], tipo="trenR", capacidad=float("inf"), costo=0)
	else:
		# Si la estación en reparación es la primera, limita la capacidad y añade aristas en sentido contrario
		G.edges[aristas_trasnoche[0][0][0],aristas_trasnoche[0][0][1]]["capacidad"] = capacidad_limitada
		G.add_edge(aristas_trasnoche[0][0][0],aristas_trasnoche[1][0][0], tipo="trenR",capacidad=float("inf"),costo=0)
		G.add_edge(aristas_trasnoche[1][0][1],aristas_trasnoche[0][0][1], tipo="trenR", capacidad=float("inf"), costo=0)
	return G

def interpretacion_vagones(G,flowDict):
	# Para la interpretacion, cambio los flujos para que representen los vagones.
	for u, v in G.edges:
		if G.edges[u, v]["tipo"] == "tren":
			flowDict[u][v] += G.nodes[u]["demanda"]
		G.edges[u,v]["capacidad"] = G.edges[u,v]["capacidad"] + G.nodes[u]["demanda"]
	# Sumar la demanda del nodo receptor al flujo existente.
	return G


def plot(G: nx.Graph, flowDict: dict, title, filename):
	"""
	Genera y muestra un gráfico del grafo G con los flujos calculados en flowDict.

	Parámetros:
	- G (networkx.Graph): Grafo dirigido de la red de transporte.
	- flowDict (dict): Diccionario con los flujos en cada arista del grafo.
	- title (int): Indicador para cambiar el título del gráfico (0 para el resultado del algoritmo, 1 para la interpretación en vagones).
	- filename (str): Nombre del archivo de instancia utilizado.

	"""
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
		"trenR": "orange",
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

	nx.draw(G, pos, node_color=nodos_colores, edge_color=aristas_colores, with_labels=False, node_size=1000)

	for tipo, color in colores_aristas.items():
		plt.scatter([], [], c=color, label=tipo)

	plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.05), ncol=6)

	# Etiquetas de las aristas
	edge_labels = {}
	for u, v, d in G.edges(data=True):
		flujo = flowDict[u][v] if u in flowDict and v in flowDict[u] else 0
		capacidad = G.edges[(u,v)]["capacidad"]
		edge_labels[(u, v)] = f"{flujo}/{capacidad}"

	node_labels = {nodo: f"{nodo} ({G.nodes[nodo]['demanda']})" for nodo in G.nodes}
	nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

	nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
	if title == 0:
		plt.title("Devolución del algoritmo min_cost_flow")
		plt.text(0.5, -0.1, f'Archivo: {filename}\nCon adaptación y reducción de las cotas inferiores a 0 para que el algoritmo funcione.', fontsize=10, color='gray', style='italic', ha='center', transform=plt.gca().transAxes)
	else:
		plt.title("Interpretación de los vagones")
		plt.text(0.5, -0.1, f'Archivo: {filename}', fontsize=10, color='gray', style='italic', ha='center', transform=plt.gca().transAxes)

	plt.show()