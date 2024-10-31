import numpy as np
from math import atan2, asin, sqrt, degrees, radians
import pandas as pd

def generate_flight_path(duration=300, sampling_rate=1):
    """
    Generate a simple flight path with basic maneuvers.
    Duration in seconds, sampling_rate in Hz
    """
    # Generate time points
    t = np.linspace(0, duration, int(duration * sampling_rate))
    
    # Create a simple flight path
    # Aircraft starts at (0,0,1000), flies in a slight ascending spiral
    x = 100 * np.sin(t/30)  # Horizontal motion
    y = 100 * np.cos(t/30)  # Horizontal motion
    z = 1000 + t/2         # Gradual climb
    
    return pd.DataFrame({
        'time': t,
        'x': x,
        'y': y,
        'z': z
    })

def calculate_radar_measurements(flight_data, radar_position):
    """
    Calculate radar measurements (azimuth, elevation, range) from a given position
    """
    x_r, y_r, z_r = radar_position
    
    # Calculate relative positions
    dx = flight_data['x'] - x_r
    dy = flight_data['y'] - y_r
    dz = flight_data['z'] - z_r
    
    # Calculate range
    range_data = np.sqrt(dx**2 + dy**2 + dz**2)
    
    # Calculate azimuth (horizontal angle)
    azimuth = np.degrees(np.arctan2(dy, dx))
    
    # Calculate elevation (vertical angle)
    elevation = np.degrees(np.arcsin(dz/range_data))
    
    return pd.DataFrame({
        'time': flight_data['time'],
        'azimuth': azimuth,
        'elevation': elevation,
        'range': range_data
    })

def main():
    # Generate flight path
    flight_data = generate_flight_path(duration=300, sampling_rate=1)
    
    # Define radar positions (x, y, z in meters)
    radar1_pos = (-200, -200, 0)
    radar2_pos = (200, 200, 0)
    
    # Calculate radar measurements
    radar1_data = calculate_radar_measurements(flight_data, radar1_pos)
    radar2_data = calculate_radar_measurements(flight_data, radar2_pos)
    
    # Save to CSV files
    flight_data.to_csv('flight_path.csv', index=False)
    radar1_data.to_csv('radar1_measurements.csv', index=False)
    radar2_data.to_csv('radar2_measurements.csv', index=False)

if __name__ == "__main__":
    main()
