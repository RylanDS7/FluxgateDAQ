"""
Script to interpolate a COMSOL field to find the residuals between
simulated and measured field
Rylan Stutters
Aug 2025
"""

import numpy as np
import pandas as pd
import os
from io import StringIO

def clean_COMSOL_field(input, offset, scale):
    path = os.path.join("src", "residual_analysis", "simFields", input)

    data = []
    with open(path, "r") as f:
        for line in f:
            # Remove whitespace
            stripped = line.strip()
            if stripped[0] != "%":
                data.append(stripped)
            if not stripped:
                continue

    data = "\n".join(data)
    df = pd.read_csv(StringIO(data), delim_whitespace=True, header=None)
    df[0] = df[0] * scale
    df[0] = df[0] - offset
    df.drop_duplicates(subset=0)
    
    return df
            
def clean_fluxgate_field(input_up, input_down):
    path_up = os.path.join("data", input_up)
    path_down = os.path.join("data", input_down)
    df_u = pd.read_csv(path_up, header=1)
    df_d = pd.read_csv(path_down, header=1)

    df = pd.DataFrame()
    df["Pos"] = df_u["Position (cm)"] - 12.5
    df["B"] = (df_u["B_y (uT)"] - df_d["B_y (uT)"]) / 2
    
    return df

def interp_field(df, x):
    for i in range(len(df)):
        if df[0][i] > x:
            m = (df[1][i] - df[1][i-1]) / (df[0][i] - df[0][i-1])
            return m * (x - df[0][i - 1]) + df[1][i-1]


df_c = clean_COMSOL_field("testCoilBz.txt", 24.33, 100)
df_f = clean_fluxgate_field("fluxgate_2025-08-25_12.16.05.csv", "fluxgate_2025-08-25_12.12.27.csv")

residuals = []
for i in range(len(df_f)):
    residual = interp_field(df_c, df_f["Pos"][i]) - df_f["B"][i]
    residuals.append(residual)

print(max(abs(np.array(residuals))))