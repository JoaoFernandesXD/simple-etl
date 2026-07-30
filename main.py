
from database import Database
import os
import pandas as pd


db = Database(hostname='localhost', port=5432, database='etl_database', user='admin', password='admin')

for file in os.listdir("data/silver"):

    df = pd.read_parquet(f"data/silver/{file}")
    db.create_table(
        file.replace(".parquet", ""), 
        df.columns.tolist()
    )
    db.insert_data(file.replace(".parquet",""), df)

  