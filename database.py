import os
import pandas as pd
import psycopg2


class Database:
    def __init__(self, hostname, port, database, user, password):
        self.hostname = hostname
        self.port = port
        self.database = database
        self.user = user
        self.password =  password
        self.conn = psycopg2.connect(host=self.hostname, port=self.port, database=self.database, user=self.user, password=self.password)
        
    def create_table(self, name_table, columns):
        cursor = self.conn.cursor()
        types_columns = [f"{col} TEXT" for col in columns]
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {name_table} ({', '.join(types_columns)})")
        self.conn.commit()
        

    def insert_data(self, name_table, df):
        cursor = self.conn.cursor()
        for index, row in df.iterrows():
            valures = tuple(row.values)
            cursor.execute(f"INSERT INTO {name_table} VALUES {valures}")
        self.conn.commit()
       

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
       
        return result

    def select_from_all(self, name_table, limit=10):
        query = f"SELECT * FROM {name_table} LIMIT {limit}"
        return self.execute_query(query)

    
    def connection_close(self):
        self.conn.close()


if __name__ == "__main__":
    db = Database(hostname='localhost', port=5432, database='etl_database', user='admin', password='admin')

    df = pd.DataFrame({"id": [1,2,3], "nome": ["joao","maria","pedro"]})

    db.create_table("joao1", df.columns.tolist())
    db.insert_data("joao1", df)

    print(db.select_from_all("joao1"))
    db.connection_close()