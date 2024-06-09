import json
from core_functions import *

# Función principal
def main():
	archivos = ["instances/new_instance.json", "instances/toy_instance.json", "instances/retiro-tigre-semana.json", "instances/test_instance_ward.json"]
	archivos = ["instances/retiro-tigre-semana.json"]
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
				flowDict[u][v] += G.nodes[u]["demanda"]
				G.edges[u,v]["capacidad"] = G.edges[u,v]["capacidad"] + G.nodes[u]["demanda"]
				# Sumar la demanda del nodo receptor al flujo existente.

		# Plotteo con la representación medida en vagones.
		plotear(G, flowDict, 1, filename)

if __name__ == "__main__":
	main()
