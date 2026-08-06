import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import urllib

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FINAL_FILE = BASE_DIR / "data" / "final" / "insurance_master.csv"

# =====================================================
# Read Final Dataset
# =====================================================

df = pd.read_csv(FINAL_FILE)

print(df.head())

print(f"\nRows: {len(df)}")

# =====================================================
# SQL Server Connection
# =====================================================

server = r"MYCOMP\SQLEXPRESS"
database = "InsurancePortfolio"

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

params = urllib.parse.quote_plus(connection_string)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}"
)

# =====================================================
# Load Data
# =====================================================

print("\nLoading data into SQL Server...")

df.to_sql(
    name="Insurance_Master",
    con=engine,
    if_exists="replace",
    index=False
)

print("\nData loaded successfully!")