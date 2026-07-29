import requests
import pandas as pd

def get_cep(cep):

    endpoint = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        response = requests.get(endpoint, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None
    except requests.exceptions.ConnectionError as e:
        print(f"Erro ao buscar CEP {cep} na API", response.status_code)
        return None
    except requests.exceptions.Timeout as e:
        print(f"timeout para cep {cep}: {e}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisicao para cep {cep}: {e}")
        return None


running_cep_list = []
patch_users = "data/bronze/user_data.csv"
users_df = pd.read_csv(patch_users)

cep_list = users_df["cep"].tolist()



for cep in cep_list[:10]:
    new_cep = cep.replace("-","")
    if "erro" in new_cep:
        continue
    running_cep_list.append(cep)


running_cep_list_df = pd.DataFrame(running_cep_list)
running_cep_list_df.to_csv("list_cep_all.csv", index=False)