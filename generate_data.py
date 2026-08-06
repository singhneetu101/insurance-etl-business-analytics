import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import timedelta
import os

# -------------------------------
# Initialize Faker
# -------------------------------

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

# -------------------------------
# Create folders automatically
# -------------------------------

os.makedirs("../data/raw", exist_ok=True)

# -------------------------------
# Master Data
# -------------------------------

products = [
    "Motor",
    "Home",
    "Marine",
    "Travel",
    "Commercial Property"
]

branches = ["North", "South", "East", "West"]

cities = {
    "North": ["Delhi", "Chandigarh", "Jaipur"],
    "South": ["Bangalore", "Chennai", "Hyderabad"],
    "East": ["Kolkata", "Bhubaneswar", "Patna"],
    "West": ["Mumbai", "Ahmedabad", "Pune"]
}

occupations = [
    "Engineer",
    "Doctor",
    "Teacher",
    "Business",
    "Lawyer",
    "Student",
    "Consultant",
    "Accountant"
]

status_list = [
    "Active",
    "Expired",
    "Cancelled",
    "Renewed",
    "Lapsed"
]

customers = []

for i in range(1, 3001):

    branch = random.choice(branches)

    city = random.choice(cities[branch])

    customer = {

        "Customer_ID": f"CUST{i:05d}",

        "Customer_Name": fake.name(),

        "Gender": random.choice(["Male", "Female"]),

        "Occupation": random.choice(occupations),

        "Annual_Income": random.randint(300000,3000000),

        "Branch": branch,

        "City": city,

        "State": fake.state()

    }

    customers.append(customer)

customers_df = pd.DataFrame(customers)

print(customers_df.head())

agents = []

for i in range(1,121):

    branch = random.choice(branches)

    agent = {

        "Agent_ID": f"AG{i:03d}",

        "Agent_Name": fake.name(),

        "Experience_Years": random.randint(1,20),

        "Branch": branch

    }

    agents.append(agent)

agents_df = pd.DataFrame(agents)

print(agents_df.head())

policies = []

customer_ids = customers_df["Customer_ID"].tolist()

agent_ids = agents_df["Agent_ID"].tolist()

for i in range(1,10001):

    product = random.choice(products)

    branch = random.choice(branches)

    start_date = fake.date_between(
        start_date="-3y",
        end_date="today"
    )

    end_date = start_date + timedelta(days=365)

    premium = {

        "Motor": random.randint(5000,40000),

        "Home": random.randint(8000,70000),

        "Marine": random.randint(20000,200000),

        "Travel": random.randint(1000,20000),

        "Commercial Property": random.randint(50000,1000000)

    }[product]

    policy = {

        "Policy_ID": f"POL{i:06d}",

        "Customer_ID": random.choice(customer_ids),

        "Agent_ID": random.choice(agent_ids),

        "Product": product,

        "Branch": branch,

        "Policy_Start_Date": start_date,

        "Policy_End_Date": end_date,

        "Premium": premium,

        "Sum_Insured": premium * random.randint(20,100),

        "Policy_Status": random.choice(status_list)

    }

    policies.append(policy)

policies_df = pd.DataFrame(policies)

print(policies_df.head())

customers_df.to_csv(
    "../data/raw/customers.csv",
    index=False
)

agents_df.to_csv(
    "../data/raw/agents.csv",
    index=False
)

policies_df.to_csv(
    "../data/raw/policies.csv",
    index=False
)

print("Files created successfully!")

from pathlib import Path

# Get project root
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

customers_df.to_csv(RAW_DIR / "customers.csv", index=False)
agents_df.to_csv(RAW_DIR / "agents.csv", index=False)
policies_df.to_csv(RAW_DIR / "policies.csv", index=False)

print(f"Files saved in: {RAW_DIR}")