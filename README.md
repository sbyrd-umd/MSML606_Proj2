# MSML606 Project 2: TSP Solver

A Python implementation of the Travelling Salesman Problem (TSP) using the **Nearest Neighbor greedy heuristic** on real US city data. Cities are randomly sampled from the SimpleMaps US Cities dataset, distances are calculated using the Haversine formula (great-circle distance), and the resulting tour is visualized on a map with matplotlib.

## How It Works

1. Loads a random sample of US cities from a CSV file
2. Builds a distance matrix using the Haversine formula
3. Solves the TSP using the Nearest Neighbor algorithm (always visit the closest unvisited city)
4. Plots the resulting tour with arrows showing the route

## Requirements

- Python 3.10+
- `matplotlib`

Install dependencies:

```bash
pip install matplotlib
```

## How to Run

```bash
python tsp_solver.py <path_to_cities_csv>
```

**Example:**

```bash
python tsp_solver.py simplemaps_uscities_basicv1.93/uscities.csv
```

The script samples 12 random US cities by default, prints the tour order and total distance (in km) to the console, and opens a matplotlib window with the route visualized.
