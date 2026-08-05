from src.database import Database
from src.normalize_data import NormalizeData
import pandas as pd 
import os
from dotenv import load_dotenv
load_dotenv()

def transforme_dados():
     transforme = NormalizeData(input_dir = 'data/bronze', output_dir = 'data/silver')
     return transforme.normalize_data()

def carregamento_banco(db):
    for file in os.listdir("data/silver"):
   
           df = pd.read_parquet(f"data/silver/{file}")
           db.create_table(
               file.replace(".parquet", ""), 
               df.columns.tolist()
           )
           db.insert_data(file.replace(".parquet",""), df)


def main():
    db = Database(hostname=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), database=os.getenv('DB_DATABASE'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'))

    transforme_dados()
    carregamento_banco(db)


if __name__ == "__main__":
    main()


  