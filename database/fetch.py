import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:12345@localhost/npl_auction_system"
)

df = pd.read_sql("SELECT * FROM players", engine)

print(df.head())
print(df.shape)