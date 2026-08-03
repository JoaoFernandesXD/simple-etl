# simple-etl

Projeto de estudo/portfólio de um pipeline **ETL** em Python, construído para demonstrar extração, transformação e carga de dados a partir de múltiplas fontes (arquivo CSV, arquivo JSON e API externa) até um banco de dados relacional.

> ⚠️ Projeto em desenvolvimento. Algumas partes ainda estão sendo implementadas/ajustadas.

## Visão geral

O pipeline segue uma arquitetura inspirada no modelo **Medalhão (Bronze → Silver)**:

1. **Bronze** — dados brutos, como recebidos das fontes originais (`data/bronze`):
   - `user_data.csv`: cadastro de usuários (nome, idade, profissão, CEP, telefone, e-mail, sexo).
   - `products.json`: catálogo de produtos associados a usuários.
2. **Silver** — dados tratados e normalizados (`data/silver`), gerados a partir da camada Bronze:
   - Remoção de duplicados.
   - Conversão de colunas incompatíveis com o formato Parquet.
   - Enriquecimento do cadastro de usuários com dados de endereço (cidade, estado, bairro, logradouro, código IBGE) consultados via [API ViaCEP](https://viacep.com.br/) a partir do CEP de cada usuário.
3. **Carga** — os arquivos Parquet da camada Silver são lidos e persistidos em um banco **PostgreSQL**, com criação automática das tabelas.

## Tecnologias

- Python 3
- [pandas](https://pandas.pydata.org/) — leitura/transformação de dados e escrita em Parquet
- [requests](https://docs.python-requests.org/) — consumo da API ViaCEP
- [psycopg2](https://www.psycopg.org/) — conexão com PostgreSQL
- [python-dotenv](https://github.com/theskumar/python-dotenv) — variáveis de ambiente
- PostgreSQL via Docker (docker-compose)

## Estrutura do projeto

```
simple-etl/
├── data/
│   ├── bronze/          # dados brutos (CSV, JSON)
│   └── silver/          # dados tratados (Parquet)
├── client_api.py        # cliente de consulta à API ViaCEP
├── normalize_data.py    # normalização e enriquecimento (Bronze -> Silver)
├── database.py          # camada de acesso ao PostgreSQL (criação de tabelas e insert)
├── main.py               # carga dos arquivos Silver para o PostgreSQL
├── docker-compose.yml    # sobe o PostgreSQL usado no projeto
├── requirements.txt
└── .env.example
```

## Como executar

### 1. Pré-requisitos
- Python 3.10+
- Docker e Docker Compose

### 2. Configurar variáveis de ambiente
Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

### 3. Subir o banco de dados

```bash
docker-compose up -d
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Rodar o pipeline

```bash
# Bronze -> Silver (normalização e enriquecimento via API)
python normalize_data.py

# Silver -> PostgreSQL (carga no banco)
python main.py
```

## Status / próximos passos

- [ ] Testes automatizados
- [ ] Tratamento de erros mais robusto na camada de carga
- [ ] Camada Gold (agregações/modelagem para consumo)
- [ ] Orquestração do pipeline (ex.: um único comando/script de execução)

## Autor

Desenvolvido por [João Fernandes](https://github.com/JoaoFernandesXD) como projeto de estudo/portfólio.
