import json
import networkx as nx
import matplotlib.pyplot as plt
from ploteo import plotear
import math

def main():
	filename = "instances/toy_instance.json"
	#filename = "instances/retiro-tigre-semana.json"

	with open(filename) as json_file:
		data = json.load(json_file)
	#print(data)
	# test file reading
	G = nx.DiGraph()
	
	for viaje_id, viaje_data in data["services"].items():
		# Accede a los datos de cada viaje
		nodo1_time = viaje_data["stops"][0]["time"]
		nodo1_station = viaje_data["stops"][0]["station"]
		nodo2_time = viaje_data["stops"][1]["time"]
		nodo2_station = viaje_data["stops"][1]["station"]
		nodo1_type = viaje_data["stops"][0]["type"]
		nodo2_type = viaje_data["stops"][1]["type"]
		# Agrega los nodos al grafo con sus atributos
		
		if nodo1_type == "D" and nodo2_type == "A":
			# Crea la arista de tipo "tren" desde nodo1 a nodo2
			G.add_edge(nodo1_time, nodo2_time, tipo="tren",  capacidad= 25,costo=1, demanda=math.ceil(viaje_data["demand"][0]/100))
		elif nodo1_type == "A" and nodo2_type == "D":
			# Crea la arista de tipo "tren" desde nodo2 a nodo1
			G.add_edge(nodo2_time, nodo1_time, tipo="tren", capacidad= float("inf"),costo=0, demanda=math.ceil(viaje_data["demand"][0]/100))
		if nodo1_type == "A":
			G.add_node(nodo1_time, station=nodo1_station, type=nodo1_type, demanda= math.ceil(viaje_data["demand"][0]/100))
			G.add_node(nodo2_time, station=nodo2_station, type=nodo2_type, demanda= -math.ceil(viaje_data["demand"][0]/100))
		else:
			G.add_node(nodo1_time, station=nodo1_station, type=nodo1_type, demanda= -math.ceil(viaje_data["demand"][0]/100))
			G.add_node(nodo2_time, station=nodo2_station, type=nodo2_type, demanda= math.ceil(viaje_data["demand"][0]/100))
		

	# Crear un diccionario para agrupar nodos por estación
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
		for i in range(len(nodos_ordenados) - 1):
			G.add_edge(nodos_ordenados[i], nodos_ordenados[i + 1], tipo="traspaso", capacidad= float("inf"), costo=0)
		G.add_edge(nodos_ordenados[-1], nodos_ordenados[0], tipo="trasnoche", capacidad= float("inf"), costo=1)

	flowDict = nx.min_cost_flow(G,"demanda", "capacidad", "costo")
	plotear(G,flowDict)

    # Imprimir el resultado
	print(flowDict)



	#for service in data["services"]:
		#print(service, data["services"][service]["stops"])

	for arista in G.edges:
		if G.edges[arista]["tipo"] == "tren":
			print(arista)


if __name__ == "__main__":
	main()