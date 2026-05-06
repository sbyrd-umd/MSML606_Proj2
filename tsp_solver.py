# Sawyer Byrd
# MSML606 Project 2: TSP Solver


# AI Usage Statement:
# The only use of AI in this code is comment auto-filling and docstring generation.
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


