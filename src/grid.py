import os
import geopandas as gpd
from shapely.geometry import box
import numpy as np

def create_grid(ghmc_path, output_path):
    print(f"Loading GHMC boundary from {ghmc_path}...")
    ghmc = gpd.read_file(ghmc_path)
    
    xmin, ymin, xmax, ymax = ghmc.total_bounds
    cell_size = 0.01  # ~1km roughly in degrees
    
    print(f"Generating grid cells with size {cell_size} degrees...")
    grid_cells = []
    
    for x in np.arange(xmin, xmax, cell_size):
        for y in np.arange(ymin, ymax, cell_size):
            grid_cells.append(box(x, y, x+cell_size, y+cell_size))
            
    grid = gpd.GeoDataFrame(grid_cells, columns=['geometry'], crs=ghmc.crs)
    print(f"Generated {len(grid)} raw grid cells.")
    
    print("Clipping to GHMC boundary...")
    # use overlay to intersect with GHMC boundary
    # Fix potential topology errors before overlay
    ghmc['geometry'] = ghmc.geometry.buffer(0)
    grid = gpd.overlay(grid, ghmc, how='intersection')
    
    # Assign a unique grid_id
    grid['grid_id'] = range(1, len(grid) + 1)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    grid.to_file(output_path, driver='GeoJSON')
    print(f"Saved {len(grid)} intersecting grid cells to {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    boundary_file = os.path.join(base_dir, "01_GHMC_Boundary", "ghmc_boundary.geojson")
    output_file = os.path.join(base_dir, "data", "processed", "grid.geojson")
    
    if not os.path.exists(boundary_file):
        print(f"Error: Could not find GHMC boundary file at {boundary_file}")
    else:
        create_grid(boundary_file, output_file)
