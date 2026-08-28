import pandas as pd
import numpy as np
import datetime
from datetime import timedelta

def generate_prototype_dataset(end_date=None, num_days=90):
    """
    Generates a realistic prototype dataset for domestic Indian airfares.
    Includes data patterns based on route, airline, booking window, and time trends,
    as well as simulated data quality issues (duplicates, missing values, outliers).
    """
    if end_date is None:
        # Use an anchored date for demonstration so it's consistent with 2026-08-29
        end_date = datetime.date(2026, 8, 29)
    
    start_date = end_date - timedelta(days=num_days - 1)
    
    # Core lists
    routes = [
        {"route": "DEL → BOM", "origin": "DEL", "destination": "BOM", "base_fare": 4600},
        {"route": "DEL → BLR", "origin": "DEL", "destination": "BLR", "base_fare": 5400},
        {"route": "DEL → HYD", "origin": "DEL", "destination": "HYD", "base_fare": 4100},
        {"route": "BOM → DEL", "origin": "BOM", "destination": "DEL", "base_fare": 4700},
        {"route": "MAA → DEL", "origin": "MAA", "destination": "DEL", "base_fare": 5100},
        {"route": "BLR → HYD", "origin": "BLR", "destination": "HYD", "base_fare": 2600}
    ]
    
    airlines = [
        {"name": "IndiGo", "multiplier": 1.00, "share": 0.50},
        {"name": "Air India", "multiplier": 1.15, "share": 0.25},
        {"name": "SpiceJet", "multiplier": 0.92, "share": 0.15},
        {"name": "Akasa Air", "multiplier": 0.95, "share": 0.10}
    ]
    
    booking_windows = [1, 3, 7, 15, 30, 45]
    
    window_multipliers = {
        1: 2.20,   # 1 day advance (very high last-minute pricing)
        3: 1.65,   # 3 days advance
        7: 1.30,   # 7 days advance
        15: 1.10,  # 15 days advance
        30: 0.95,  # 30 days advance
        45: 0.90   # 45 days advance
    }
    
    ota_sources = ["MakeMyTrip", "Yatra", "EaseMyTrip", "Cleartrip", "Ixigo", "Goibibo"]
    
    np.random.seed(42) # Set seed for reproducibility
    
    data = []
    
    # Generate daily price quotes
    for day_idx in range(num_days):
        current_date = start_date + timedelta(days=day_idx)
        
        # Define a macro price trend over time (e.g., fuel price surge + seasonal variation)
        # We model a cosine-shaped fluctuation with a slight upward trend
        time_factor = 1.0 + 0.05 * np.cos(day_idx / 10.0) + (day_idx / num_days) * 0.04
        
        for route_info in routes:
            for airline_info in airlines:
                # Determine how many quotes to generate based on airline market share
                # budget/smaller airlines might not have quotes for every single window/route combination every day
                num_quotes_to_gen = 1 if np.random.rand() > (1.0 - airline_info["share"] * 1.5) else 0
                if num_quotes_to_gen == 0:
                    continue
                
                for window in booking_windows:
                    # Construct base fare for this observation
                    base = route_info["base_fare"]
                    win_mult = window_multipliers[window]
                    air_mult = airline_info["multiplier"]
                    
                    # Calculate deterministic price
                    calculated_fare = base * win_mult * air_mult * time_factor
                    
                    # Add random variation (e.g., standard deviation of 4%)
                    noise = np.random.normal(0, 0.04)
                    fare = round(calculated_fare * (1.0 + noise))
                    
                    # Determine source (OTA or Airline direct)
                    is_ota = np.random.rand() > 0.3
                    source = np.random.choice(ota_sources) if is_ota else f"{airline_info['name']} Portal"
                    
                    travel_date = current_date + timedelta(days=window)
                    
                    data.append({
                        "date": current_date,
                        "origin": route_info["origin"],
                        "destination": route_info["destination"],
                        "route": route_info["route"],
                        "airline": airline_info["name"],
                        "travel_date": travel_date,
                        "booking_window": window,
                        "fare": float(fare),
                        "source": source,
                        "cabin_class": "Economy"
                    })
                    
    df = pd.DataFrame(data)
    
    # --- Inject Simulated Data Quality Issues ---
    total_records = len(df)
    
    # 1. Duplicates (~2% of records)
    dup_indices = np.random.choice(df.index, size=int(total_records * 0.02), replace=False)
    dup_rows = df.loc[dup_indices].copy()
    # Add random timestamp tweak or just insert them directly
    df = pd.concat([df, dup_rows], ignore_index=True)
    
    # 2. Missing Values (~1.5% overall)
    # 0.8% missing fares
    missing_fare_indices = np.random.choice(df.index, size=int(len(df) * 0.008), replace=False)
    df.loc[missing_fare_indices, "fare"] = np.nan
    # 0.7% missing airlines
    missing_airline_indices = np.random.choice(df.index, size=int(len(df) * 0.007), replace=False)
    df.loc[missing_airline_indices, "airline"] = None
    
    # 3. Outliers (~1% of records)
    # High outliers (e.g., multiplied by 4 to 5)
    outlier_indices_high = np.random.choice(df.index, size=int(len(df) * 0.006), replace=False)
    df.loc[outlier_indices_high, "fare"] = df.loc[outlier_indices_high, "fare"] * np.random.uniform(4.0, 5.0)
    # Low outliers (e.g., flat fare of 150-250 INR)
    outlier_indices_low = np.random.choice(df.index, size=int(len(df) * 0.004), replace=False)
    df.loc[outlier_indices_low, "fare"] = np.random.uniform(150.0, 250.0)
    
    # Round outlier fares
    df["fare"] = df["fare"].round(2)
    
    # Reset index and sort
    # Convert 'date' to datetime.date to avoid pandas timestamp issues later
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["travel_date"] = pd.to_datetime(df["travel_date"]).dt.date
    
    df = df.sort_values(by="date").reset_index(drop=True)
    
    return df
