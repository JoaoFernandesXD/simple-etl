import pandas as pd
import os


class GoldLayer:
    def __init__(self):
        os.makedirs("data/gold", exist_ok=True)

    def carregamento_usuarios(self):
        file_user = "data/silver/user_data.parquet"
        return pd.read_parquet(file_user)

    def users_by_state(self, df):
        # quantos usuarios temos por estado?
        total_usuario_estado = (
            df.groupby("estado")
            .size()
            .reset_index(name="quantidade_usuarios")
        )
        total_usuario_estado.to_parquet("data/gold/users_by_state.parquet")
        return total_usuario_estado

    def users_by_city(self, df):
        # quantos usuarios existem por cidade?
        total_usuario_cidade = (
            df.groupby("cidade")
            .size()
            .reset_index(name="total_usuario_cidade")
        )
        total_usuario_cidade.to_parquet("data/gold/users_by_city.parquet")
        return total_usuario_cidade

    def mean_users_state(self, df):
        # qual é a idade media de nossos clientes por estado?
        idade_media_cliente_estado = (
            df.groupby("estado")["idade"]
            .mean()
            .reset_index(name="idade_media_cliente_estado")
        )
        idade_media_cliente_estado.to_parquet("data/gold/mean_users_state.parquet")
        return idade_media_cliente_estado

    def job_users_count(self, df):
        # quantidade de usuarios por profissao
        usuario_profissao = (
            df.groupby("profissao")
            .size()
            .reset_index(name="usuario_profissao")
        )
        usuario_profissao.to_parquet("data/gold/job_users_count.parquet")
        return usuario_profissao

    def sex_users(self, df):
        # distribuicao por sexo
        distribuicao_sexo = (
            df.groupby("sexo")
            .size()
            .reset_index(name="distribuicao_sexo")
        )
        distribuicao_sexo.to_parquet("data/gold/sex_users.parquet")
        return distribuicao_sexo

