import os
import pandas as pd
import geopandas as gpd
import numpy as np

def calculate_scores(grid_path, output_path):
    print(f"Loading grid from {grid_path}...")
    grid = gpd.read_file(grid_path)
    
    num_cells = len(grid)
    centroids = grid.geometry.centroid
    
    # Simulate Transport Data (Roads, Bus stops, Metro)
    # Since we lack direct OSM shapefiles in the workspace right now,
    # we generate realistic dense-center proxy values.
    # Hyderabad center approx 17.3850, 78.4867
    center_lat, center_lon = 17.3850, 78.4867
    
    road_density_raw = []
    bus_stop_density_raw = []
    metro_proximity_raw = []
    
    for pt in centroids:
        dist_to_center = np.sqrt((pt.y - center_lat)**2 + (pt.x - center_lon)**2)
        
        # Closer to center = denser roads and buses
        # Max distance is around 0.3 degrees
        base_density = max(0, 1.0 - (dist_to_center / 0.3) * 0.8)
        
        road_density_raw.append(base_density * np.random.uniform(0.7, 1.3))
        bus_stop_density_raw.append(base_density * np.random.uniform(0.5, 1.5))
        
        # Metro roughly follows center to certain suburbs. Let's make it a sharp decline based on dist.
        metro_proximity_raw.append(base_density * np.random.uniform(0.2, 1.0))
        
    def normalize(val_list):
        arr = np.array(val_list)
        return (arr - arr.min()) / (arr.max() - arr.min() + 1e-9)
        
    road_density = normalize(road_density_raw)
    bus_stop_density = normalize(bus_stop_density_raw)
    metro_proximity = normalize(metro_proximity_raw)
    
    traffic_score = 0.4 * road_density + 0.3 * bus_stop_density + 0.3 * metro_proximity
    
    # Simulate Industrial Zones (Score = 1 / (1 + distance))
    # Rough locations of industries around city edges
    industrial_zones = [
        (17.5255, 78.3614), # Jeedimetla
        (17.3833, 78.4011), # Kattedan
        (17.6186, 78.4772), # Medchal
        (17.4262, 78.6475), # Uppal/Cherlapally
    ]
    
    industrial_score_raw = []
    for pt in centroids:
        min_dist = min([np.sqrt((pt.y - iz[0])**2 + (pt.x - iz[1])**2) for iz in industrial_zones])
        score = 1.0 / (1.0 + min_dist * 100) # scale dist slightly so the +1 doesn't wash it out
        industrial_score_raw.append(score)
        
    industrial_score = normalize(industrial_score_raw)
    
    # Emission Index = 0.5 * Traffic + 0.5 * Industrial
    emission_index = 0.5 * traffic_score + 0.5 * industrial_score
    
    df = pd.DataFrame({
        'grid_id': grid['grid_id'],
        'traffic_score': traffic_score,
        'industrial_score': industrial_score,
        'emission_index': emission_index
    })
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Scoring complete. Saved to {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    grid_file = os.path.join(base_dir, "data", "processed", "grid.geojson")
    output_file = os.path.join(base_dir, "data", "processed", "grid_scores.csv")
    
    if os.path.exists(grid_file):
        calculate_scores(grid_file, output_file)
    else:
        print("Please run grid.py first.")
