import numpy as np

# -----------------------------
# (1) Define the graph distances
# -----------------------------
graph = {
    1: {2: 12, 3: 10, 7: 12},
    2: {1: 12, 3: 8, 4: 12},
    3: {1: 10, 2: 8, 4: 11, 5: 3, 7: 9},
    4: {2: 12, 3: 11, 5: 11, 6: 10},
    5: {3: 3, 4: 11, 6: 6, 7: 7},
    6: {4: 10, 5: 6, 7: 9},
    7: {1: 12, 3: 9, 5: 7, 6: 9}
}

# -----------------------------
# (2) Define city coordinates
# -----------------------------
cities = {
    1: np.array([0.0, 0.0]),
    3: np.array([10.0, 0.0]),
    5: np.array([10.0, 3.0]),
    7: np.array([10.0, 10.0]),
    6: np.array([19.0, 10.0]),
    4: np.array([19.0, 0.0]),
    2: np.array([31.0, 0.0])
}

# -----------------------------
# (3) Initialize the SOM (neurons in a ring)
# -----------------------------
num_neurons = 20
angles = np.linspace(0, 2 * np.pi, num_neurons, endpoint=False)
radius = 15
neurons = np.array([[radius * np.cos(a), radius * np.sin(a)] for a in angles])

# -----------------------------
# (4) SOM Training Parameters
# -----------------------------
num_iterations = 1000
initial_learning_rate = 0.8
initial_radius = num_neurons / 2

def decay_learning_rate(iteration):
    return initial_learning_rate * np.exp(-iteration / num_iterations)

def decay_radius(iteration):
    return initial_radius * np.exp(-iteration / num_iterations)

# -----------------------------
# (5) SOM Training Loop
# -----------------------------
city_ids = list(cities.keys())

for iteration in range(num_iterations):
    city_id = np.random.choice(city_ids)
    city = cities[city_id]

    distances = np.linalg.norm(neurons - city, axis=1)
    winner_idx = np.argmin(distances)

    lr = decay_learning_rate(iteration)
    radius_decay = decay_radius(iteration)

    for i in range(num_neurons):
        distance_on_ring = min(abs(i - winner_idx), num_neurons - abs(i - winner_idx))
        if distance_on_ring <= radius_decay:
            influence = np.exp(-(distance_on_ring ** 2) / (2 * (radius_decay ** 2)))
            neurons[i] += lr * influence * (city - neurons[i])

# -----------------------------
# (6) Extract the Route
# -----------------------------
city_positions = [(np.argmin(np.linalg.norm(neurons - cities[c], axis=1)), c) for c in cities]
city_positions.sort()
final_route = [c for _, c in city_positions]

# Ensure route starts at city 1
while final_route[0] != 1:
    final_route = final_route[1:] + final_route[:1]

# -----------------------------
# (7) Compute Total Distance
# -----------------------------
def compute_total_distance(route, graph):
    total = 0
    for i in range(len(route)):
        a = route[i]
        b = route[(i + 1) % len(route)]
        total += graph[a][b] if b in graph[a] else 0
    return total

total_distance = compute_total_distance(final_route, graph)


print("Final Route:", " > ".join(map(str, final_route + [final_route[0]])))
print("Total Distance:", total_distance)
