"""
Synthetic Telematics Data Generator for AuroraSync OS.

Generates realistic vehicle telematics data with failure patterns
for 10 vehicles over time.

Usage:
    python data_generators/generate_telematics.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


# Set random seed for reproducibility
np.random.seed(42)

# Configuration
NUM_VEHICLES = 10
ROWS_PER_VEHICLE = 2000
OUTPUT_PATH = "ml_models/datasets/telematics_logs.csv"

# Vehicle IDs
VEHICLE_IDS = [f"VEH{i:03d}" for i in range(1, NUM_VEHICLES + 1)]

# Failure components
FAILURE_COMPONENTS = ["none", "brake", "engine", "battery", "tyre"]


def generate_normal_data(n_rows: int) -> dict:
    """
    Generate normal operating conditions data.
    
    Args:
        n_rows: Number of rows to generate
    
    Returns:
        Dictionary with normal telematics data
    """
    return {
        "engine_temp": np.random.normal(90, 5, n_rows),  # Mean 90°C, std 5
        "brake_pad_wear": np.random.normal(8.0, 1.0, n_rows),  # Mean 8mm, std 1mm
        "battery_voltage": np.random.normal(12.8, 0.2, n_rows),  # Mean 12.8V
        "vibration": np.random.uniform(0.1, 0.4, n_rows),  # Low vibration
        "tyre_pressure": np.random.normal(32, 1.5, n_rows),  # Mean 32 PSI
        "ambient_temp": np.random.normal(25, 8, n_rows),  # Mean 25°C
    }


def inject_brake_failure_pattern(data: dict, indices: np.ndarray) -> None:
    """
    Inject brake failure pattern into data.
    
    Pattern:
    - Low brake pad wear (< 3mm)
    - Elevated vibration (> 0.8)
    """
    data["brake_pad_wear"][indices] = np.random.uniform(0.5, 2.5, len(indices))
    data["vibration"][indices] = np.random.uniform(0.8, 1.5, len(indices))


def inject_engine_failure_pattern(data: dict, indices: np.ndarray) -> None:
    """
    Inject engine failure pattern into data.
    
    Pattern:
    - High engine temperature (> 105°C)
    - Often correlated with high ambient temp
    """
    data["engine_temp"][indices] = np.random.uniform(105, 120, len(indices))
    # Sometimes high ambient temp contributes
    data["ambient_temp"][indices] += np.random.uniform(5, 15, len(indices))


def inject_battery_failure_pattern(data: dict, indices: np.ndarray) -> None:
    """
    Inject battery failure pattern into data.
    
    Pattern:
    - Low battery voltage (< 12.0V)
    """
    data["battery_voltage"][indices] = np.random.uniform(11.0, 11.9, len(indices))


def inject_tyre_failure_pattern(data: dict, indices: np.ndarray) -> None:
    """
    Inject tyre failure pattern into data.
    
    Pattern:
    - Abnormal tyre pressure (< 26 or > 38 PSI)
    """
    # Half too low, half too high
    half = len(indices) // 2
    data["tyre_pressure"][indices[:half]] = np.random.uniform(22, 26, half)
    data["tyre_pressure"][indices[half:]] = np.random.uniform(38, 42, len(indices) - half)


def generate_vehicle_data(vehicle_id: str, n_rows: int) -> pd.DataFrame:
    """
    Generate telematics data for a single vehicle.
    
    Args:
        vehicle_id: Vehicle identifier
        n_rows: Number of rows to generate
    
    Returns:
        DataFrame with vehicle telematics data
    """
    # Generate timestamps (one reading every 30 minutes over ~40 days)
    start_date = datetime(2025, 11, 1, 0, 0, 0)
    timestamps = [start_date + timedelta(minutes=30*i) for i in range(n_rows)]
    
    # Generate normal data
    data = generate_normal_data(n_rows)
    
    # Generate cumulative odometer (increases over time)
    # Average ~50 km per day
    daily_km = np.random.normal(50, 10, n_rows)
    daily_km = np.maximum(daily_km, 0)  # No negative km
    data["odometer"] = np.cumsum(daily_km / 48)  # 48 readings per day
    
    # Initialize failure flags
    failure_flag = np.zeros(n_rows, dtype=int)
    failure_component = np.array(["none"] * n_rows)
    
    # Inject failures (5-10% of data)
    failure_rate = np.random.uniform(0.05, 0.10)
    n_failures = int(n_rows * failure_rate)
    
    if n_failures > 0:
        # Randomly select failure indices
        failure_indices = np.random.choice(n_rows, n_failures, replace=False)
        
        # Distribute failures across components
        # Brake: 40%, Engine: 25%, Battery: 20%, Tyre: 15%
        component_probs = [0.40, 0.25, 0.20, 0.15]
        components = ["brake", "engine", "battery", "tyre"]
        
        for idx in failure_indices:
            # Select failure component
            component = np.random.choice(components, p=component_probs)
            failure_component[idx] = component
            failure_flag[idx] = 1
        
        # Inject failure patterns
        brake_indices = failure_indices[failure_component[failure_indices] == "brake"]
        engine_indices = failure_indices[failure_component[failure_indices] == "engine"]
        battery_indices = failure_indices[failure_component[failure_indices] == "battery"]
        tyre_indices = failure_indices[failure_component[failure_indices] == "tyre"]
        
        if len(brake_indices) > 0:
            inject_brake_failure_pattern(data, brake_indices)
        if len(engine_indices) > 0:
            inject_engine_failure_pattern(data, engine_indices)
        if len(battery_indices) > 0:
            inject_battery_failure_pattern(data, battery_indices)
        if len(tyre_indices) > 0:
            inject_tyre_failure_pattern(data, tyre_indices)
    
    # Create DataFrame
    df = pd.DataFrame({
        "vehicle_id": vehicle_id,
        "timestamp": [ts.isoformat() + "Z" for ts in timestamps],
        "engine_temp": data["engine_temp"],
        "brake_pad_wear": data["brake_pad_wear"],
        "battery_voltage": data["battery_voltage"],
        "vibration": data["vibration"],
        "tyre_pressure": data["tyre_pressure"],
        "odometer": data["odometer"],
        "ambient_temp": data["ambient_temp"],
        "failure_flag": failure_flag,
        "failure_component": failure_component
    })
    
    # Clip values to realistic ranges
    df["engine_temp"] = df["engine_temp"].clip(60, 130)
    df["brake_pad_wear"] = df["brake_pad_wear"].clip(0, 12)
    df["battery_voltage"] = df["battery_voltage"].clip(10.5, 14.0)
    df["vibration"] = df["vibration"].clip(0, 2.0)
    df["tyre_pressure"] = df["tyre_pressure"].clip(20, 45)
    df["ambient_temp"] = df["ambient_temp"].clip(5, 50)
    
    return df


def main():
    """Generate synthetic telematics data for all vehicles."""
    print("=" * 70)
    print("🚗 AuroraSync OS - Synthetic Telematics Data Generator")
    print("=" * 70)
    print()
    
    print(f"Generating data for {NUM_VEHICLES} vehicles...")
    print(f"Rows per vehicle: {ROWS_PER_VEHICLE}")
    print()
    
    # Generate data for all vehicles
    all_data = []
    for vehicle_id in VEHICLE_IDS:
        print(f"  Generating data for {vehicle_id}...", end=" ")
        df = generate_vehicle_data(vehicle_id, ROWS_PER_VEHICLE)
        all_data.append(df)
        print("✓")
    
    # Combine all data
    print()
    print("Combining data...")
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Save to CSV
    print(f"Saving to {OUTPUT_PATH}...")
    combined_df.to_csv(OUTPUT_PATH, index=False)
    
    # Print statistics
    print()
    print("=" * 70)
    print("📊 Dataset Statistics")
    print("=" * 70)
    print()
    print(f"Total rows: {len(combined_df):,}")
    print(f"Total vehicles: {combined_df['vehicle_id'].nunique()}")
    print()
    
    print("Failure Distribution:")
    print(f"  Normal (no failure): {(combined_df['failure_flag'] == 0).sum():,} ({(combined_df['failure_flag'] == 0).sum() / len(combined_df) * 100:.1f}%)")
    print(f"  Failures: {(combined_df['failure_flag'] == 1).sum():,} ({(combined_df['failure_flag'] == 1).sum() / len(combined_df) * 100:.1f}%)")
    print()
    
    print("Failures by Component:")
    failure_counts = combined_df[combined_df['failure_flag'] == 1]['failure_component'].value_counts()
    for component, count in failure_counts.items():
        print(f"  {component.capitalize()}: {count:,} ({count / (combined_df['failure_flag'] == 1).sum() * 100:.1f}%)")
    print()
    
    print("Feature Statistics:")
    print(combined_df[['engine_temp', 'brake_pad_wear', 'battery_voltage', 
                       'vibration', 'tyre_pressure', 'ambient_temp']].describe())
    print()
    
    print("=" * 70)
    print("✅ Data generation complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Train model: python ml_models/train_simple_model.py")
    print("  2. Test prediction: curl http://localhost:8000/api/v1/predict/test")
    print()


if __name__ == "__main__":
    main()
