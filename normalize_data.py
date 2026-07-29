import os
import pandas as pd 

input_dir = 'data/bronze' #data raw
output_dir = 'data/silver'


os.makedirs(output_dir, exist_ok=True)


for file in os.listdir(input_dir):
    input_path = os.path.join(input_dir, file)
    name, ext = os.path.splitext(file)
    output_path = os.path.join(output_dir, f'{name}.parquet')
 
    if ext.lower() == '.csv':
        df = pd.read_csv(input_path)
    elif ext.lower() == '.json':
        try:
            df = pd.read_json(input_path)
        except ValueError:
            df = pd.read_json(input_path, lines=True)
    else:
        print(f"Arquivo {file} nao suportado")
        continue

    #garantir que colunas do tipo list converter para string
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)

    #remove linhas duplicadas
    df = df.drop_duplicates().reset_index(drop=True)

    df.to_parquet(output_path, index=False)

    print(f"Arquivo {file} normalizado e salvo como {output_path}")