import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math as m


def load_data_22_4():
    
    # Distances data
    df_distances = pd.read_excel('data/distances.xlsx', sheet_name=0, header=None)
    distances = df_distances.iloc[2:, 2:].to_numpy()
    
    # Workload data
    df_workloads = pd.read_csv('data/bricks_index_values.csv')
    workloads = df_workloads['index_value'].to_numpy()
    
    # Current assignment data (c_ij)
    # 1 if brick_i is assigned to SR_j else 0
    current_assignment = np.zeros((22, 4))
    current_assignment[[0, 1, 2, 3, 4], 0] = 1
    current_assignment[[5, 6, 7, 8], 1] = 1
    current_assignment[[9, 10, 11, 12, 13], 2] = 1
    current_assignment[[14, 15, 16, 17, 18, 19, 20, 21], 3] = 1
    
    bricks_distances = pd.read_excel('data/distances.xlsx', sheet_name=1, skiprows=1, usecols="C:X")
    bricks_distances.columns = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
                                "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"]
    
    return distances, workloads, current_assignment, bricks_distances


def load_data_100_10():
    
    # Preprocessing 100 bricks 10 SRs data
    data = pd.read_csv('data\Pfitzer10-100.csv', delimiter=';', skiprows=2)
    data.columns = [
        "zone", "x", "y", "workload_index", "current_office",
        "1", "2", "3", "4", "5", "6", "7", 
        "8", "9", "10"]

    data = data.dropna(how="all", axis=1)
    data[['x', 'y', 'workload_index']] = data[['x', 'y', 'workload_index']].replace(',', '.', regex=True)
    data[['x', 'y', 'workload_index']] = data[['x', 'y', 'workload_index']].apply(pd.to_numeric)
    
    
    # Distance data
    df_distances = pd.DataFrame(columns=[str(i) for i in range(1, 11)])
    
    for sr in range(1, 11):
        sr_col = str(sr)
        office_row = data[(data['current_office'] == 1) & (data[sr_col] == 1)]
        x_office, y_office = office_row.iloc[0]['x'], office_row.iloc[0]['y']
        df_distances[sr_col] = np.sqrt((data['x'] - x_office)**2 + (data['y'] - y_office)**2)
        
    distances = df_distances.to_numpy()
    
    # Workload data
    workloads = data["workload_index"].to_numpy()
    
    # Current assignment data
    current_assignment = data[["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]].to_numpy()
    
    # Brick locations data
    brick_locations = data.set_index('zone')[['x', 'y']].to_dict(orient='index')
    
    return distances, workloads, current_assignment, brick_locations
    
