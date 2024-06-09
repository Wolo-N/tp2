import json
import networkx as nx
import matplotlib.pyplot as plt
from main_alu import construir_grafo, plotear, flujo_maximo_corte_minimo
# Función para construir el grafo a partir de los datos proporcionados

# Función principal
def main():
    archivos = ["instances/new_instance.json", "instances/toy_instance.json", "instances/retiro-tigre-semana.json"]
    archivos = ["instances/toy_instance.json"]
    for filename in archivos: 
        with open(filename) as json_file:
            data = json.load(json_file)
        

        estacion_reparacion = "Tigre" #debe ir Retiro o Tigre.si es para otra instancia como new_instance poner estaciones bien 
        capacidad_limitada = 1
        # Construye el grafo
        G = construir_grafo(data)

        aristas_trasnoche = []
        for u,v, in G.edges():
            if G.edges[u,v]["tipo"] == "trasnoche":
                aristas_trasnoche.append(((u,v), G.nodes[u]["station"])) #agrego la arista y de donde sale 
        if estacion_reparacion == G.nodes[aristas_trasnoche[1][0][0]]["station"]: #si la estacion rota es la segunda, agrego aristas de tipo trenR como corresponda
            G.edges[aristas_trasnoche[1][0][0],aristas_trasnoche[1][0][1]]["capacidad"] = capacidad_limitada
            G.add_edge(aristas_trasnoche[1][0][0],aristas_trasnoche[0][0][0], tipo="trenR",capacidad=float("inf"),costo=0)
            G.add_edge(aristas_trasnoche[0][0][1],aristas_trasnoche[1][0][1], tipo="trenR", capacidad=float("inf"), costo=0)
        else: #si la estacion rota es la primera, entonces poner aristas con el otro sentido que las de arriba
            G.edges[aristas_trasnoche[0][0][0],aristas_trasnoche[0][0][1]]["capacidad"] = capacidad_limitada
            G.add_edge(aristas_trasnoche[0][0][0],aristas_trasnoche[1][0][0], tipo="trenR",capacidad=float("inf"),costo=0)
            G.add_edge(aristas_trasnoche[1][0][1],aristas_trasnoche[0][0][1], tipo="trenR", capacidad=float("inf"), costo=0)
        # Calcula el flujo máximo y el corte mínimo
        flowDict = flujo_maximo_corte_minimo(G)
        #flowDict = {}
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
        for u, v in G.edges():
            print(u,v)

if __name__ == "__main__":
    main()
