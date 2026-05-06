# Sawyer Byrd
# MSML606 Project 2: TSP Solver


# AI Usage Statement:
# The only use of AI in this code is comment auto-filling, docstring generation, 
#   google search AI responses to figure out the best distance measurment for TSP..
# Other than that, all code was written by hand without any AI assistance.


# imports
import math
import random
import csv
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ---------------------
# 1.) Loading The Data |
# ---------------------

def load_cities(filepath: str, sample_size: int=12) -> list[dict]:
    """
        Load the SimpleMaps US Cities CSV and return a random sample of cities.
        
        Each city dict contains:
            name  - "City, ST" label
            lat   - latitude  (float)
            lon   - longitude (float)
    Args:
        filepath (str): path to the simplemaps uscities.csv file
        sample_size (int, optional): number of cities to sample. Defaults to 12.

    Returns:
        list[dict]: list of sampled city dictionaries
    """

    cities = []
    
    with open(filepath, newline="", encoding="utf-8") as f:
        
        # read csv and build city dicts
        reader = csv.DictReader(f)
        for row in reader:
            # skip rows with missing coordinates
            if not row["lat"] or not row["lng"]:
                continue
            cities.append({
                "name": f"{row['city']}, {row['state_id']}",
                "lat":  float(row["lat"]),
                "lon":  float(row["lng"]),
            })
        
        # get random sample of cities    
        if sample_size > len(cities):
            raise ValueError(f"Sample size {sample_size} exceeds dataset size {len(cities)}.")
        
        # return random sample of cities
        return random.sample(cities, sample_size)



# -------------------------
# 2.) Distance Calculation |
# -------------------------
#        - Since we are using real world data, we need to calculate distances around a globe.
#        - Use the Haversine formula to calculate the great-circle distance between two cities.
#        - Haversine formula: https://en.wikipedia.org/wiki/Haversine_formula

def haversine(city1: dict, city2: dict) -> float:
    """
        Calculates the great-circle distance from city1 to city2
        using the Haversine formula.  Returns distance in kilometres.

    Args:
        city1 (dict): city 1
        city2 (dict): city 2

    Returns:
        float: Distance in kilometres from city1 to city2
    """

    # convert lat and long from deg to rad
    lat1, lat2 = math.radians(city1["lat"]), math.radians(city2["lat"])
    lon1, lon2 = math.radians(city1["lon"]), math.radians(city2["lon"])

    # haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return 6371 * c  # earth's radius in kilometres

# build distance matrix
def build_distance_matrix(cities: list[dict]) -> list[list[float]]:
    """
        Builds a distance matrix representation of the cities.
        Matrix[i][j] = haversine distance between cities[i] and cities[j]
    Args:
        cities (list[dict]): list of city dicts

    Returns:
        list[list[float]]: distance matrix
    """
    
    n = len(cities)
    matrix = [[0.0] * n for _ in range(n)]  # initialize n x n matrix with zeros

    for i in range(n):
        for j in range(i + 1, n):
            dist = haversine(cities[i], cities[j])
            matrix[i][j] = dist
            matrix[j][i] = dist  # symmetric

    return matrix


# ---------------------------
# 3.) Nearest Neighbor Algorithm |
# ---------------------------

def nearest_neighbor(cities: list[dict], dist_matrix: list[list[float]], start_index: int=0) -> tuple[list[int], float]:
    """
        Solves TSP with the Nearest Neighbor greedy heuristic.

    Args:
        cities (list[dict]): list of city dicts
        dist_matrix (list[list[float]]): precomputed distance matrix
        start_index (int, optional): index of starting city. Defaults to 0.

    Returns:
        tuple[list[int], float]: (tour, tour_length)
            tour: list of city indices in the order they are visited
            tour_length: total length of the tour in kilometres
    """

    n = len(cities)
    visited = [False] * n
    tour = [start_index]
    tour_length = 0.0
    visited[start_index] = True

    for _ in range(1, n):
        last_city = tour[-1]
        next_city = None
        min_dist = float("inf")
        
        for j in range(n):
            if not visited[j] and dist_matrix[last_city][j] < min_dist:
                min_dist = dist_matrix[last_city][j]
                next_city = j

        tour.append(next_city)
        tour_length += min_dist
        visited[next_city] = True

    # return to start
    tour.append(start_index)
    tour_length += dist_matrix[next_city][start_index]

    return tour, tour_length


# ------------------
# 4.) Visualization |
# ------------------

def plot_tour(cities: list[dict], tour: list[int]) -> None:
    """
        Plot the TSP tour route on a simple map using matplotlib
            Starting city is marked with green dot,
            other cities marked with blue dots,
            rout edges are shown as arrows.

    Args:
        cities (list[dict]): list of city dicts
        tour (list[int]): tour route as list of city indices
    """
    
    # extract latitudes and longitudes in tour order
    lats = [cities[i]["lat"] for i in tour]
    lons = [cities[i]["lon"] for i in tour]

    plt.figure(figsize=(10, 6))
    
    # highlight starting city
    plt.scatter(cities[tour[0]]["lon"], cities[tour[0]]["lat"], color="green", s=100, label="Start/End")
    
    # plot other cities
    for i in tour[1:-1]:
        plt.scatter(cities[i]["lon"], cities[i]["lat"], color="blue", s=50)
        
    # plot tour edges
    for i in range(len(tour) - 1):
        plt.arrow(cities[tour[i]]["lon"], cities[tour[i]]["lat"],
                  cities[tour[i + 1]]["lon"] - cities[tour[i]]["lon"],
                  cities[tour[i + 1]]["lat"] - cities[tour[i]]["lat"],
                  length_includes_head=True, head_width=0.2, alpha=0.5)
    
    # annotate city names
    for i in tour:
        plt.text(cities[i]["lon"], cities[i]["lat"], cities[i]["name"], fontsize=8)

    plt.title("TSP Tour Route")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid()
    plt.legend()
    plt.show()
    

# ------------------------------------
# Main function to run the TSP solver |
# ------------------------------------

def solve_tsp(filepath: str, sample_size: int=12) -> None:
    # Step 1: Load cities
    cities = load_cities(filepath, sample_size)

    # Step 2: Build distance matrix
    dist_matrix = build_distance_matrix(cities)

    # Step 3: Solve TSP with nearest neighbor heuristic
    route, total_dist = nearest_neighbor(cities, dist_matrix)

    print("Tour route (city indices):")
    for idx in route:
        print(f"  {cities[idx]['name']}, ({cities[idx]['lat']:.2f}, {cities[idx]['lon']:.2f})")
    print("Total tour distance (km):", total_dist)

    # Step 4: Visualize the tour
    plot_tour(cities, route)
    
    
# ------------
# Entry point |
# ------------

if __name__ == "__main__":
    """
        Usage: python tsp_solver.py <path_to_cities_csv>
    """
    if len(sys.argv) != 2:
        print("Usage: python tsp_solver.py <path_to_cities_csv>")
        sys.exit(1)

    filepath = sys.argv[1]
    solve_tsp(filepath, sample_size=12)
