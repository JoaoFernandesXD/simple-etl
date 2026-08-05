from src.database import Database
from src.normalize_data import NormalizeData
import pandas as pd 
import os
from dotenv import load_dotenv
load_dotenv()

db = Database(hostname=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), database=os.getenv('DB_DATABASE'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'))


def main():

    transforme = NormalizeData(input_dir = 'data/bronze', output_dir = 'data/silver')
    transforme.normalize_data()

    for file in os.listdir("data/silver"):

        df = pd.read_parquet(f"data/silver/{file}")
        db.create_table(
            #file.replace(".parquet", ""), 
            #df.columns.tolist()
        )
        db.insert_data(file.replace(".parquet",""), df)




main()


  