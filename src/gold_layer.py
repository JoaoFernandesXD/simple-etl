import pandas as pd
import os


class GoldLayer:
    """Camada Gold do pipeline de ETL.

    Responsavel por consumir os dados tratados da camada Silver e gerar
    agregacoes basicas prontas para consumo (dashboards, relatorios,
    etc). Cada metodo de agregacao persiste seu resultado em um arquivo
    parquet dentro do diretorio 'data/gold'.
    """

    def __init__(self):
        """Inicializa a camada Gold garantindo que o diretorio de saida exista."""
        os.makedirs("data/gold", exist_ok=True)

    def carregamento_usuarios(self):
        """Carrega os dados de usuarios da camada Silver.

        Returns:
            pd.DataFrame: DataFrame com os dados de usuarios lidos do
            arquivo 'data/silver/user_data.parquet'.
        """
        file_user = "data/silver/user_data.parquet"
        return pd.read_parquet(file_user)

    def users_by_state(self, df):
        """Calcula a quantidade de usuarios agrupados por estado.

        Args:
            df: DataFrame de usuarios contendo a coluna 'estado'.

        Returns:
            pd.DataFrame: DataFrame com as colunas 'estado' e
            'quantidade_usuarios'. Tambem salvo em
            'data/gold/users_by_state.parquet'.
        """
        total_usuario_estado = (
            df.groupby("estado")
            .size()
            .reset_index(name="quantidade_usuarios")
        )
        total_usuario_estado.to_parquet("data/gold/users_by_state.parquet")
        return total_usuario_estado

    def users_by_city(self, df):
        """Calcula a quantidade de usuarios agrupados por cidade.

        Args:
            df (pd.DataFrame): DataFrame de usuarios contendo a coluna 'cidade'.

        Returns:
            pd.DataFrame: DataFrame com as colunas 'cidade' e
            'total_usuario_cidade'. Tambem salvo em
            'data/gold/users_by_city.parquet'.
        """
        total_usuario_cidade = (
            df.groupby("cidade")
            .size()
            .reset_index(name="total_usuario_cidade")
        )
        total_usuario_cidade.to_parquet("data/gold/users_by_city.parquet")
        return total_usuario_cidade

    def mean_users_state(self, df):
        """Calcula a idade media dos usuarios agrupados por estado.

        Args:
            df (pd.DataFrame): DataFrame de usuarios contendo as colunas
                'estado' e 'idade'.

        Returns:
            pd: DataFrame com as colunas 'estado' e
            'idade_media_cliente_estado'. Tambem salvo em
            'data/gold/mean_users_state.parquet'.
        """
        idade_media_cliente_estado = (
            df.groupby("estado")["idade"]
            .mean()
            .reset_index(name="idade_media_cliente_estado")
        )
        idade_media_cliente_estado.to_parquet("data/gold/mean_users_state.parquet")
        return idade_media_cliente_estado

    def job_users_count(self, df):
        """Calcula a quantidade de usuarios agrupados por profissao.

        Args:
            df: DataFrame de usuarios contendo a coluna 'profissao'.

        Returns:
            pd.DataFrame: DataFrame com as colunas 'profissao' e
            'usuario_profissao'. Tambem salvo em
            'data/gold/job_users_count.parquet'.
        """
        usuario_profissao = (
            df.groupby("profissao")
            .size()
            .reset_index(name="usuario_profissao")
        )
        usuario_profissao.to_parquet("data/gold/job_users_count.parquet")
        return usuario_profissao

    def sex_users(self, df):
        """Calcula a distribuicao de usuarios agrupados por sexo.

        Args:
            df (pd.DataFrame): DataFrame de usuarios contendo a coluna 'sexo'.

        Returns:
            pd.DataFrame: DataFrame com as colunas 'sexo' e
            'distribuicao_sexo'. Tambem salvo em
            'data/gold/sex_users.parquet'.
        """
        distribuicao_sexo = (
            df.groupby("sexo")
            .size()
            .reset_index(name="distribuicao_sexo")
        )
        distribuicao_sexo.to_parquet("data/gold/sex_users.parquet")
        return distribuicao_sexo