import json
import networkx as nx
import matplotlib.pyplot as plt
from ploteo import plotear
import math

def main():
	filename = "instances/toy_instance.json"
	filename = "instances/retiro-tigre-semana.json"

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
		max_capacidad = data["rs_info"]["max_rs"]
		# Agrega los nodos al grafo con sus atributos
		demanda = math.ceil(viaje_data["demand"][0]/100)
		#print(demanda)
	
		
		
		if nodo1_type == "A":
			
			G.add_node(f"{nodo1_time}_{nodo1_station}_{nodo1_type}" , time = nodo1_time, station=nodo1_station, type=nodo1_type, demanda= -demanda)
			G.add_node(f"{nodo2_time}_{nodo2_station}_{nodo2_type}" , time = nodo2_time, station=nodo2_station, type=nodo2_type, demanda= demanda)
		else:
			
			G.add_node(f"{nodo1_time}_{nodo1_station}_{nodo1_type}", time = nodo1_time, station=nodo1_station, type=nodo1_type, demanda= demanda)
			G.add_node(f"{nodo2_time}_{nodo2_station}_{nodo2_type}", time = nodo2_time, station=nodo2_station, type=nodo2_type, demanda= -demanda)
		if nodo1_type == "D" and nodo2_type == "A":
			# Crea la arista de tipo "tren" desde nodo1 a nodo2
			G.add_edge(f"{nodo1_time}_{nodo1_station}_{nodo1_type}", f"{nodo2_time}_{nodo2_station}_{nodo2_type}", tipo="tren",  capacidad = max_capacidad - demanda, costo=0)
		elif nodo1_type == "A" and nodo2_type == "D":
			# Crea la arista de tipo "tren" desde nodo2 a nodo1
			G.add_edge(f"{nodo2_time}_{nodo2_station}_{nodo2_type}", f"{nodo1_time}_{nodo1_station}_{nodo1_type}", tipo="tren", capacidad = max_capacidad - demanda, costo = 0)
		
	
	#for nodo in G.nodes():
	#	if "705" in nodo:	
	#		print(nodo)
	# Crear un diccionario para agrupar nodos por estación

	i = 0
	for x in G.nodes():
		i = i + 1
		print(x)
	print("la cantidad de nodos es: " ,i)

	estaciones_nodos = {}
	for nodo in G.nodes:
		estacion = G.nodes[nodo]["station"]
		if estacion not in estaciones_nodos:
			estaciones_nodos[estacion] = []
		estaciones_nodos[estacion].append(nodo)

	# Ordenar nodos dentro de cada estación por tiempo
	for estacion, nodos in estaciones_nodos.items():
		nodos_ordenados = sorted(nodos, key=lambda nodo: G.nodes[nodo]["time"])

		# Agregar aristas dirigidas entre nodos adyacentes
		for i in range(len(nodos_ordenados) - 1):
			G.add_edge(nodos_ordenados[i], nodos_ordenados[i + 1], tipo="traspaso", capacidad= float("inf"), costo=0)
		G.add_edge(nodos_ordenados[-1], nodos_ordenados[0], tipo="trasnoche", capacidad= float("inf"), costo=1)



	for u,v in G.edges():
		if G.edges[(u,v)]["tipo"] == "tren":
			if G.nodes[u]["demanda"]+G.nodes[v]["demanda"] != 0:
				print("aca esta la verguita que no da cero: ", u,", ",v)
				print (G.nodes[u]["demanda"]+G.nodes[v]["demanda"])







	
	flowDict = nx.min_cost_flow(G,"demanda", "capacidad", "costo")
	plotear(G, flowDict)
    # Imprimir el resultado
	print(flowDict) #Plotteo exacto lo que tira min_cost_flow

	#para la interpretacion, cambio los flujos para que representen los vagones
	for u, v in G.edges:
		if G.edges[u, v]["tipo"] == "tren":
			# Sumar la demanda del nodo receptor al flujo existente
			flowDict[u][v] += G.nodes[u]["demanda"]
	plotear(G, flowDict)


	#for service in data["services"]:
		#print(service, data["services"][service]["stops"])

	for arista in G.edges:
		if G.edges[arista]["tipo"] == "tren":
			print(arista)



if __name__ == "__main__":
	main()