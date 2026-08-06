import pandas as pd
import numpy as np
from pathlib import Path

# ======================================================
# PROJECT PATHS
# ======================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
FINAL_DIR = BASE_DIR / "data" / "final"

PROCESSED_DIR.mkdir(exist_ok=True)
FINAL_DIR.mkdir(exist_ok=True)

# ======================================================
# READ ALL BRANCH FILES
# ======================================================

branch_files = []

for file in RAW_DIR.rglob("*"):

    if file.suffix.lower() in [".csv", ".xlsx"]:

        if file.parent.name in ["North", "South", "East", "West"]:

            branch_files.append(file)

print("=" * 50)
print("Branch Files Found")
print("=" * 50)

for file in branch_files:
    print(file.name)

print()

# ======================================================
# EXTRACT
# ======================================================

dfs = []

for file in branch_files:

    if file.suffix == ".csv":
        temp = pd.read_csv(file)

    else:
        temp = pd.read_excel(file)

    temp["Source_File"] = file.name

    dfs.append(temp)

master = pd.concat(dfs, ignore_index=True)

print("Rows Read :", len(master))
print()

# ======================================================
# STANDARDIZE COLUMN NAMES
# ======================================================

column_mapping = {

    "Policy Number": "Policy_ID",
    "Policy_No": "Policy_ID",
    "PolicyID": "Policy_ID",
    "Policy Ref": "Policy_ID",

    "Client Name": "Customer_Name",
    "Customer": "Customer_Name",
    "Insured Name": "Customer_Name",

    "Premium Amount": "Premium",
    "Premium_Value": "Premium"

}

master.rename(columns=column_mapping, inplace=True)

# ======================================================
# REMOVE DUPLICATE COLUMNS
# ======================================================

master = master.loc[:, ~master.columns.duplicated()]

# ======================================================
# STANDARDIZE PRODUCT NAMES
# ======================================================

master["Product"] = master["Product"].replace({

    "motor": "Motor",

    "HOME": "Home",

    "Travel Insurance": "Travel",

    "Marine Insurance": "Marine",

    "Commercial": "Commercial Property"

})

# ======================================================
# REMOVE EXTRA SPACES
# ======================================================

object_columns = master.select_dtypes(include="object").columns

for col in object_columns:

    master[col] = master[col].astype(str).str.strip()

# ======================================================
# HANDLE MISSING CUSTOMER NAMES
# ======================================================

master["Customer_Name"] = master["Customer_Name"].replace("nan", np.nan)

master["Customer_Name"] = master["Customer_Name"].fillna("Unknown")

# ======================================================
# HANDLE PREMIUM
# ======================================================

master["Premium"] = pd.to_numeric(
    master["Premium"],
    errors="coerce"
)

# Missing Premium

master["Premium"] = master["Premium"].fillna(
    master["Premium"].median()
)

# Negative Premium

master.loc[
    master["Premium"] < 0,
    "Premium"
] = abs(master["Premium"])

# ======================================================
# REMOVE DUPLICATE POLICIES
# ======================================================

before = len(master)

master.drop_duplicates(
    subset="Policy_ID",
    inplace=True
)

after = len(master)

print("Duplicates Removed :", before - after)

# ======================================================
# CONVERT DATES
# ======================================================

master["Policy_Start_Date"] = pd.to_datetime(
    master["Policy_Start_Date"],
    errors="coerce"
)

master["Policy_End_Date"] = pd.to_datetime(
    master["Policy_End_Date"],
    errors="coerce"
)

# ======================================================
# CREATE NEW BUSINESS COLUMNS
# ======================================================

master["Policy_Duration_Days"] = (

    master["Policy_End_Date"]

    -

    master["Policy_Start_Date"]

).dt.days

master["Premium_Band"] = pd.cut(

    master["Premium"],

    bins=[0,10000,50000,100000,500000,1000000],

    labels=[
        "Low",
        "Medium",
        "High",
        "Very High",
        "Ultra High"
    ]

)

master["Data_Quality_Flag"] = np.where(

    master["Customer_Name"]=="Unknown",

    "Review",

    "OK"

)

# ======================================================
# SAVE PROCESSED FILE
# ======================================================

processed_file = PROCESSED_DIR / "insurance_processed.csv"

master.to_csv(
    processed_file,
    index=False
)

# ======================================================
# CREATE FINAL DATASET
# ======================================================

master = master.sort_values(

    by="Policy_Start_Date",

    ascending=False

)

final_file = FINAL_DIR / "insurance_master.csv"

master.to_csv(
    final_file,
    index=False
)

# ======================================================
# SUMMARY
# ======================================================

print("=" * 50)

print("ETL COMPLETED")

print("=" * 50)

print("Final Rows :", len(master))

print("Columns :", len(master.columns))

print()

print(master.head())

print()

print("Processed File Saved To")

print(processed_file)

print()

print("Final File Saved To")

print(final_file)