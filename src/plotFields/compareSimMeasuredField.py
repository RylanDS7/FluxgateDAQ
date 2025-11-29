"""
Script to plot COMSOL simulated data against measured fluxgate data
Rylan Stutters
Nov 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from io import StringIO


def extract_field(file1, file2,):
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

def get_dfcol(df, i):
     return df.iloc[:, int(i)]

def reverse_field(df):
    for i in np.linspace(1, 3, 3):
            col = get_dfcol(df, i)
            df.iloc[:, int(i)] = col[::-1]
    return df

def plot_field(df, field_comp="B_y (uT)"):
    df.plot(0, field_comp, kind="scatter")
    plt.show(block=False)

def measured_residuals(df1, df2):
    df = df1 - df2
    df["Position (cm)"] = df1["Position (cm)"]
    return df


field = extract_field("fluxgate_2025-11-28_16.08.07.csv", "fluxgate_2025-11-28_16.12.26.csv")
field_sim = clean_COMSOL_field("innerV2AxialField.txt", -11, 100, -20, 100)

fig, ax = plt.subplots()

ax.scatter(get_dfcol(field, 0), get_dfcol(field, 2), label='Measured', s=20)
ax.scatter(get_dfcol(field_sim, 0), get_dfcol(field_sim, 1), label='Simulated', s=3)

ax.set_xlabel('Position (cm)', fontsize=18)
ax.set_ylabel('B_y (uT)', fontsize=18)
ax.legend(fontsize=15)

plt.grid()
plt.show()
