import json
import networkx as nx
import matplotlib.pyplot as plt



def main():
	filename = "instances/toy_instance.json"
	# filename = "instances/retiro-tigre-semana.json"

	with open(filename) as json_file:
		data = json.load(json_file)

	# test file reading

	for service in data["services"]:
		print(service, data["services"][service]["stops"])

	# Initialize directed graph
	G = nx.DiGraph()


	# Add nodes and edges based on services
	for service_id, service_data in data["services"].items():
		stops = service_data["stops"]
		demand = service_data["demand"][0]
		capacity = data["rs_info"]["capacity"]
		units_needed = demand // capacity
		
		# Add nodes and edges for each service
		for i in range(len(stops) - 1):
			departure_event = stops[i]
			arrival_event = stops[i + 1]
			
			dep_node = (service_id, departure_event["time"], departure_event["station"], departure_event["type"])
			arr_node = (service_id, arrival_event["time"], arrival_event["station"], arrival_event["type"])
			
			G.add_node(dep_node)
			G.add_node(arr_node)
			
			# Edge representing the service trip
			G.add_edge(dep_node, arr_node, lower_bound=units_needed, upper_bound=data["rs_info"]["max_rs"], cost=0)
			
	# Add transfer edges within stations
	for station in data["stations"]:
		station_nodes = sorted([n for n in G.nodes if n[2] == station], key=lambda x: x[1])
		for i in range(len(station_nodes) - 1):
			G.add_edge(station_nodes[i], station_nodes[i + 1], lower_bound=0, upper_bound=float('inf'), cost=0)

	# Add overnight edges
	for station in data["stations"]:
		first_event = min([n for n in G.nodes if n[2] == station], key=lambda x: x[1])
		last_event = max([n for n in G.nodes if n[2] == station], key=lambda x: x[1])
		G.add_edge(last_event, first_event, lower_bound=0, upper_bound=float('inf'), cost=data["cost_per_unit"][station])

	# Draw the directed graph with node labels using networkx draw method
	plt.figure(figsize=(12, 8))

	# Position nodes using a layered layout to avoid compactness and to show trips going down
	pos = {}
	y_positions = {
		'Retiro': [0, -5, -10, -15],
		'Tigre': [-2.5, -7.5, -12.5, -17.5]
	}
	i_retiro = 0
	i_tigre = 0
	for node in G.nodes:
		if node[2] == "Retiro":
			pos[node] = (0, y_positions['Retiro'][i_retiro])
			i_retiro += 1
		else:
			pos[node] = (5, y_positions['Tigre'][i_tigre])
			i_tigre += 1

	# Draw the nodes and edges
	nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", arrowsize=20)

	# Draw edge labels
	edge_labels = {(u, v): f"lb={d['lower_bound']}, ub={d['upper_bound']}, cost={d['cost']}" for u, v, d in G.edges(data=True)}
	nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

	# Show the plot
	plt.title("Directed Graph of Railway Services")
	plt.show()

if __name__ == "__main__":
	main()