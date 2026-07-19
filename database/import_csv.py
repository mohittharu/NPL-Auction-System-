import pandas as pd
from sqlalchemy import create_engine

# Read the CSV
df = pd.read_csv("data/npl_data.csv")

# Connect to MySQL
engine = create_engine(
    "mysql+pymysql://root:12345@localhost/npl_auction_system"
)

# Import CSV into MySQL
df.to_sql(
    name="players",
    con=engine,
    if_exists="replace",
    index=False
)

print("✅ CSV imported successfully!")