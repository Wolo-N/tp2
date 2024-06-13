import json
from core_functions import *

def main():
    archivos = ["instances/new_instance.json"]#["instances/short_instance_2.json", "instances/short_instance.json","instances/new_instance.json", "instances/toy_instance.json",
                #"instances/retiro-tigre-semana.json", "instances/test_instance_ward.json"]

    # Si hay arreglos en progreso setear variable a TRUE,
    # especifricar que estacione esta en reparacion y su limte de capacidad.
    hay_arreglos_en_progreso = True
    estacion_en_reparacion = 'Tigre'
    capacidad_limitada = 2


    for filename in archivos:
        with open(filename) as json_file:
            data = json.load(json_file)

        # Construye el grafo
        G = construir_grafo(data)

        if hay_arreglos_en_progreso:
            cambios_por_reparaciones(estacion_en_reparacion, capacidad_limitada, G)

        # Calcula el flujo máximo y el corte mínimo
        flowDict = flujo_maximo_corte_minimo(G)

        # Plotteo exacto lo que tira min_cost_flow.
        # El 0 o el 1 pasado como parámetro solamente cambia los títulos.
        plot(G, flowDict, 0, filename, 0)

        # Preparamos y plotteamos la representación medida en vagones.
        interpretacion_vagones(G,flowDict, hay_arreglos_en_progreso)
        plot(G, flowDict, 1, filename, True)

if __name__ == "__main__":
    main()