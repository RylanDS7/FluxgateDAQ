"""
Script to interpolate a COMSOL field to find the residuals between
simulated and measured field
Inner coil V2 application
Rylan Stutters
Dec 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import StringIO

def extract_field(file1, file2):
    path1 = os.path.join("data", file1)
    path2 = os.path.join("data", file2)
    df_1 = pd.read_csv(path1, header=1)
    df_2 = pd.read_csv(path2, header=1)

    df = (df_1 - df_2) / 2
    df["Position (cm)"] = df_1["Position (cm)"]

    if df.iloc[:, 1:4].mean().mean() < 0:
        df.iloc[:, 1:4] = -df.iloc[:, 1:4]

    return df

def clean_COMSOL_field(input, offset, scale, cutL, cutR):
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

    df = df[(df[0] >= cutL) & (df[0] <= cutR)]
    
    return df

def interp_field(df, x):
    for i in range(len(df)):
        if df[0][i] == x:
            return df[1][i]
        if df[0][i] > x:
            m = (df[1][i] - df[1][i-1]) / (df[0][i] - df[0][i-1])
            return m * (x - df[0][i - 1]) + df[1][i-1]
        
def get_dfcol(df, i):
     return df.iloc[:, int(i)]



field = extract_field("fluxgate_2025-11-28_16.08.07.csv", "fluxgate_2025-11-28_16.12.26.csv")
field_sim = clean_COMSOL_field("innerV2AxialField.txt", -11, 100, -20, 100)

residuals = []
for i in range(len(field)):
    residual = interp_field(field_sim, get_dfcol(field, 0)[i]) - get_dfcol(field, 2)[i]
    residuals.append(residual)

fig, ax = plt.subplots(figsize=(10,10))

ax.errorbar(get_dfcol(field, 0), get_dfcol(field, 2), xerr=0.5, yerr=0.15, label='Measured', fmt='o', color="orange")
ax.scatter(get_dfcol(field_sim, 0), get_dfcol(field_sim, 1), label='Simulated', s=2)
ax.errorbar(get_dfcol(field, 0), residuals, yerr =0.15, label='Residuals', fmt='o', color="purple")

ax.set_xlabel('Axial Position (cm)', fontsize=24)
ax.set_ylabel('Vertical Magnetic Field (uT)', fontsize=24)
ax.legend(fontsize=20)

plt.grid()
plt.show()
