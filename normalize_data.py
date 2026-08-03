import os
import pandas as pd 
import logging
from client_api import ConsultaAPI
logging.basicConfig(
    filename="etl.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


class NormalizeData:
    """
    Executa o processo de normalização dos dados entre as camadas
    Bronze e Silver da arquitetura Medalhão.

    Responsabilidades:
        - Ler arquivos CSV e JSON da camada Bronze.
        - Aplicar transformações e normalizações nos dados.
        - Remover registros duplicados.
        - Converter estruturas incompatíveis com Parquet.
        - Salvar os dados tratados na camada Silver.
    """
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.cep = ConsultaAPI()
        os.makedirs(output_dir, exist_ok=True)

    def normalize_data(self) -> None:
        """
        Executa o processo de normalização da camada Bronze para a camada Silver.

        Para cada arquivo encontrado no diretório de entrada:
        - identifica o tipo do arquivo
        - realiza a leitura dos dados
        - aplica as transformações necessárias
        - remove registros duplicados
        - salva o resultado em formato Parquet no diretório de saída.
        """
        for file in os.listdir(self.input_dir):
            input_path = os.path.join(self.input_dir, file)
            name, ext = os.path.splitext(file)
            output_path = os.path.join(self.output_dir, f'{name}.parquet')

                
            if ext == '.csv':

                df = pd.read_csv(input_path)
                if name == "user_data":
                   self.enriquecer_usuario(df)
            elif ext == '.json':
                try:
                    df = pd.read_json(input_path)
                except ValueError:
                    df = pd.read_json(input_path, lines=True)
            else:
                logging.error(f"Arquivo {file} nao suportado")
                continue

            df = self.convert_columns(df)
           
            #remove linhas duplicadas
            df = df.drop_duplicates().reset_index(drop=True)

            df.to_parquet(output_path, index=False)
        
            logging.info(f"Arquivo {file} normalizado e salvo como {output_path}")

    def convert_columns(self, df):
        """
            Converte para string os valores do tipo lista presentes nas colunas
            do DataFrame.

            Essa transformação garante compatibilidade com o formato Parquet,
            evitando problemas durante a gravação dos dados.

            Args:
                df (pd.DataFrame): DataFrame a ser normalizado.

            Returns:
                pd.DataFrame: DataFrame com as colunas tratadas.
        """
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, list)).any():
                df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)
        return df

    def enriquecer_usuario(self, df):
        """
            Enriquece o DataFrame de usuários com informações de endereço
            a partir do CEP, utilizando a API ViaCEP.

            Para cada CEP presente no DataFrame, a função consulta a API
            e adiciona as seguintes colunas:
                - cidade
                - estado
                - bairro
                - logradouro
                - ibge

            Parâmetros
            ----------
            df
                DataFrame contendo pelo menos a coluna 'cep'.

            Retorno
            -------
                DataFrame original com as novas colunas de endereço adicionadas.
                Caso a API não retorne dados para algum CEP, o valor None é atribuído.
        """
        df = df.copy()

        resultados = {
            "cidade": [],
            "estado": [],
            "bairro": [],
            "logradouro": [],
            "ibge": []
        }

        for cep in df["cep"]:
            cep_limpo = str(cep).replace("-", "").strip() if pd.notna(cep) else None

            dados = self.cep.obter_dados(cep_limpo) if cep_limpo else None

            resultados["cidade"].append(dados.get("localidade") if dados else None)
            resultados["estado"].append(dados.get("uf") if dados else None)
            resultados["bairro"].append(dados.get("bairro") if dados else None)
            resultados["logradouro"].append(dados.get("logradouro") if dados else None)
            resultados["ibge"].append(dados.get("ibge") if dados else None)

        for coluna, valores in resultados.items():
            df[coluna] = valores

        logging.info(f"Enriquecidos {len(df)} usuários com dados do ViaCEP.")

        return df


if __name__ == "__main__":
    normalize_data = NormalizeData(input_dir = 'data/bronze', output_dir = 'data/silver')
    normalize_data.normalize_data()
