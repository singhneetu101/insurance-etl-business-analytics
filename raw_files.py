import pandas as pd
import numpy as np
import random
from pathlib import Path

# ======================================================
# Project Paths
# ======================================================

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

random.seed(42)
np.random.seed(42)

# ======================================================
# Read Master Data
# ======================================================

policies = pd.read_csv(RAW_DIR / "policies.csv")
customers = pd.read_csv(RAW_DIR / "customers.csv")

print("Policies :", len(policies))
print("Customers:", len(customers))

# ======================================================
# Merge Customer Information
# ======================================================

df = policies.merge(
    customers[
        [
            "Customer_ID",
            "Customer_Name",
            "City",
            "State"
        ]
    ],
    on="Customer_ID",
    how="left"
)

# ======================================================
# Introduce Data Quality Issues
# ======================================================

# 5% Missing Premium
missing = df.sample(frac=0.05, random_state=42).index
df.loc[missing, "Premium"] = np.nan

# 3% Missing Customer Name
missing = df.sample(frac=0.03, random_state=7).index
df.loc[missing, "Customer_Name"] = np.nan

# Extra Spaces
rows = df.sample(frac=0.04, random_state=12).index
df.loc[rows, "Customer_Name"] = (
    " " +
    df.loc[rows, "Customer_Name"].fillna("") +
    " "
)

# Mixed Product Names
mapping = {

    "Motor": "motor",

    "Home": "HOME",

    "Travel": "Travel Insurance",

    "Marine": "Marine Insurance",

    "Commercial Property": "Commercial"

}

rows = df.sample(frac=0.15, random_state=21).index

for i in rows:

    product = df.loc[i, "Product"]

    if product in mapping:

        df.loc[i, "Product"] = mapping[product]

# Negative Premium
rows = df.sample(frac=0.01, random_state=33).index
df.loc[rows, "Premium"] *= -1

# Duplicate Records
duplicates = df.sample(200, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

print("Rows after duplicates:", len(df))

# ======================================================
# Split by Branch
# ======================================================

north = df[df["Branch"] == "North"].copy()
south = df[df["Branch"] == "South"].copy()
east = df[df["Branch"] == "East"].copy()
west = df[df["Branch"] == "West"].copy()

# ======================================================
# Different Column Names
# ======================================================

north.rename(columns={
    "Policy_ID": "Policy Number",
    "Customer_Name": "Client Name",
    "Premium": "Premium Amount"
}, inplace=True)

south.rename(columns={
    "Policy_ID": "Policy_No",
    "Customer_Name": "Customer",
    "Premium": "Premium"
}, inplace=True)

east.rename(columns={
    "Policy_ID": "PolicyID",
    "Customer_Name": "Insured Name"
}, inplace=True)

west.rename(columns={
    "Policy_ID": "Policy Ref",
    "Premium": "Premium_Value"
}, inplace=True)

# ======================================================
# Create Branch Folders
# ======================================================

(RAW_DIR / "North").mkdir(exist_ok=True)
(RAW_DIR / "South").mkdir(exist_ok=True)
(RAW_DIR / "East").mkdir(exist_ok=True)
(RAW_DIR / "West").mkdir(exist_ok=True)

# ======================================================
# Save Files
# ======================================================

north.to_excel(
    RAW_DIR / "North" / "North_Motor.xlsx",
    index=False
)

south.to_csv(
    RAW_DIR / "South" / "South_Marine.csv",
    index=False
)

east.to_excel(
    RAW_DIR / "East" / "East_Travel.xlsx",
    index=False
)

west.to_csv(
    RAW_DIR / "West" / "West_Commercial.csv",
    index=False
)

# ======================================================
# Summary
# ======================================================

print("\n========== SUMMARY ==========")

print("North :", len(north))
print("South :", len(south))
print("East  :", len(east))
print("West  :", len(west))

print("\nFiles saved successfully!")

print(RAW_DIR)