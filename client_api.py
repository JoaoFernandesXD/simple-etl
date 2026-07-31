import requests
import logging
logging.basicConfig(
    filename="etl.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

class ConsultaAPI:
    """
        Classe responsável por consultar informações de CEP através de uma API.
    """
    def __init__(self, url_base):
        """
        Inicializa a classe.

        Args:
            url_base (str): URL base da API (ex.: https://viacep.com.br/ws)
        """
        self.url_base = url_base

    def obter_dados(self, cep: int):
        """
        Consulta um CEP na API.

        Args:
            cep (str): CEP que será pesquisado.

        Returns:
                Retorna um dicionário com os dados do CEP caso a consulta
                seja realizada com sucesso. Caso ocorra algum erro,
                retorna None.
        """
        url_completa = f"{self.url_base}/{cep}/json/"
        try:
            response = requests.get(url_completa, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            logging.error(f"Erro HTTP: {e}")
            
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Erro ao buscar CEP {cep} na API", response.status_code)
            return None
        except requests.exceptions.Timeout as e:
            logging.warning(f"timeout para cep {cep}: {e}")
            return None
    
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisicao para cep {cep}: {e}")
            return None