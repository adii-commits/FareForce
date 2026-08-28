import pandas as pd
import numpy as np
import datetime

def clean_data(df):
    """
    Cleans the raw prototype dataset and returns:
    1. A cleaned DataFrame (no duplicates, no missing critical values, no outliers).
    2. A dictionary containing quality statistics.
    """
    # Create a copy to avoid modifications to original
    df_raw = df.copy()
    
    total_records = len(df_raw)
    
    # 1. Duplicates
    duplicate_count = df_raw.duplicated().sum()
    df_dedup = df_raw.drop_duplicates()
    
    # 2. Missing values
    missing_fare = df_dedup["fare"].isnull().sum()
    missing_airline = df_dedup["airline"].isnull().sum()
    
    # Drop rows with missing critical information (fare or airline)
    df_no_missing = df_dedup.dropna(subset=["fare", "airline"])
    
    # 3. Outliers (using 1.5x IQR method per Route and Booking Window)
    # We group by route and booking window because fares naturally differ drastically
    # by route distance and booking advance window.
    outlier_mask = pd.Series(False, index=df_no_missing.index)
    
    grouped = df_no_missing.groupby(["route", "booking_window"])
    for name, group in grouped:
        q1 = group["fare"].quantile(0.25)
        q3 = group["fare"].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        # Identify outliers in this group
        group_outliers = (group["fare"] < lower_bound) | (group["fare"] > upper_bound)
        outlier_mask.loc[group.index] = group_outliers
        
    outliers_count = outlier_mask.sum()
    df_clean = df_no_missing[~outlier_mask].copy()
    
    # Ensure sorted by date
    df_clean = df_clean.sort_values(by="date").reset_index(drop=True)
    
    # Metrics dictionary
    metrics = {
        "total_records": total_records,
        "duplicate_count": int(duplicate_count),
        "missing_fare": int(missing_fare),
        "missing_airline": int(missing_airline),
        "outliers_count": int(outliers_count),
        "valid_records": len(df_clean),
        "completeness_pct": round((len(df_clean) / total_records) * 100, 2) if total_records > 0 else 0.0
    }
    
    return df_clean, metrics

def calculate_chained_jevons_index(df):
    """
    Calculates the Chained Jevons Geometric Mean Index from a cleaned DataFrame.
    Returns a DataFrame with columns: ['date', 'index_value']
    
    Methodology:
    1. Define representative item categories as (route, airline, booking_window).
    2. Aggregate fares to find the mean price for each category per day.
    3. For each day t (t > 0), find categories present in both day t and day t-1.
    4. Compute price relatives for matched categories: R_c,t = P_c,t / P_c,t-1
    5. Calculate link relative for day t: G_t = exp( mean( ln(R_c,t) ) )
    6. Chain link relatives starting from base day 0 (Index = 100): I_t = I_t-1 * G_t
    """
    if len(df) == 0:
        return pd.DataFrame(columns=["date", "index_value"])
        
    # Aggregate to daily representatives to ensure unique cells
    agg = df.groupby(["date", "route", "airline", "booking_window"])["fare"].mean().reset_index()
    
    # Unique sorted dates
    dates = sorted(agg["date"].unique())
    if not dates:
        return pd.DataFrame(columns=["date", "index_value"])
        
    # Pivot so each column represents a matched item (route, airline, booking_window)
    # and each row is a date.
    pivot = agg.pivot(index="date", columns=["route", "airline", "booking_window"], values="fare")
    
    index_values = [100.0]  # Base index is 100
    
    # Loop over dates and calculate link relatives
    for idx in range(1, len(dates)):
        prev_date = dates[idx - 1]
        curr_date = dates[idx]
        
        # Get prices for both days
        prev_prices = pivot.loc[prev_date]
        curr_prices = pivot.loc[curr_date]
        
        # Find matched categories (non-null on both days)
        matched_mask = prev_prices.notnull() & curr_prices.notnull()
        
        if not matched_mask.any():
            # If no matched categories, chain relative is 1.0 (no change)
            link_relative = 1.0
        else:
            p_prev = prev_prices[matched_mask]
            p_curr = curr_prices[matched_mask]
            
            # Compute price relatives
            relatives = p_curr / p_prev
            
            # Prevent log(0) or negative price errors
            relatives = relatives[relatives > 0]
            
            if len(relatives) == 0:
                link_relative = 1.0
            else:
                # Geometric mean using exponential of mean of logs
                link_relative = np.exp(np.mean(np.log(relatives)))
                
        # Chain the index
        new_index = index_values[-1] * link_relative
        index_values.append(new_index)
        
    index_df = pd.DataFrame({
        "date": dates,
        "index_value": index_values
    })
    
    # Clean index value representations to be round and readable (e.g. 2 decimals)
    index_df["index_value"] = index_df["index_value"].round(2)
    
    return index_df

def get_route_level_indices(df):
    """
    Calculates the current index and percentage change for each route.
    Returns a DataFrame with columns: ['route', 'current_index', 'change_pct']
    """
    results = []
    routes = df["route"].unique()
    
    for route in routes:
        route_df = df[df["route"] == route]
        idx_df = calculate_chained_jevons_index(route_df)
        
        if len(idx_df) >= 2:
            current_idx = idx_df.iloc[-1]["index_value"]
            # Look back 30 days or start of index if shorter
            lookback_idx = max(0, len(idx_df) - 30)
            base_idx = idx_df.iloc[lookback_idx]["index_value"]
            change_pct = ((current_idx - base_idx) / base_idx) * 100
            
            results.append({
                "route": route,
                "current_index": round(current_idx, 2),
                "change_pct": round(change_pct, 2)
            })
        elif len(idx_df) == 1:
            results.append({
                "route": route,
                "current_index": 100.0,
                "change_pct": 0.0
            })
            
    return pd.DataFrame(results)
