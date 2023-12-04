import requests
from bs4 import BeautifulSoup
import os
from zipfile import ZipFile
import pandas as pd
from datetime import datetime, timedelta
import pytz
import json
import jwt
import time

def create_jwt(credentials):
    iat = datetime.now()
    exp = iat + timedelta(minutes=60)
    jwt_payload = {
        "iss": credentials['client_email'],
        "scope": "https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/drive",
        "aud": credentials['token_uri'],
        "exp": int(time.mktime(exp.timetuple())),
        "iat": int(time.mktime(iat.timetuple()))
    }
    jwt_token = jwt.encode(jwt_payload, credentials['private_key'], algorithm='RS256')
    return jwt_token

def upload_data_to_sheet(data_frame, spreadsheet_id, credentials):
    # Tratar valores de ponto flutuante e NaN/Infinito
    df = data_frame.copy()
    df = df.fillna("NA")  # Substituir NaN por 'NA'
    df.replace([float('inf'), float('-inf')], "NA", inplace=True)  # Substituir infinitos por 'NA'
    for col in df.select_dtypes(include=['float']):
        df[col] = df[col].apply(lambda x: f"{x:.2f}" if isinstance(x, float) else x)

    jwt_token = create_jwt(credentials)
    token_data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': jwt_token
    }
    token_response = requests.post(credentials['token_uri'], data=token_data)
    token = token_response.json().get('access_token')

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = [df.columns.tolist()] + df.values.tolist()
    body = {
        'values': data
    }

    sheets_url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/Sheet1:append?valueInputOption=USER_ENTERED'

    sheets_response = requests.post(sheets_url, headers=headers, json=body)
    return sheets_response


caminho_base = "/Users/Lucas Rocha Dantas/Documents/Lucas Rocha Dantas/Vida profissional/Cypher/Cypher Tech/Projeto_para_o_Ministerio_da_Ciencia_e_Tecnologia_do_Brasil"

url = 'https://repositorio.dados.gov.br/seges/detru/'

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        file_url = link.get('href')
        if file_url.endswith("convenio.csv.zip"):
            file_response = requests.get(url + file_url, stream=True)
            if file_response.status_code == 200:
                with open(os.path.join(caminho_base, file_url), 'wb') as file:
                    for chunk in file_response.iter_content(chunk_size=128):
                        file.write(chunk)
                print(f"Download de {file_url} completo.")

                zip_file_path = os.path.join(caminho_base, file_url)
                with ZipFile(zip_file_path, 'r') as arq:
                    arq.extractall(caminho_base)
                print(f"O arquivo {file_url} foi descompactado com sucesso!!")

                caminho_planilha = os.path.join(caminho_base, 'siconv_convenio.csv')
                dados = pd.read_csv(caminho_planilha, delimiter=';', low_memory=False)

                indices_linhas = [
                    155849, 168725, 155003, 155842, 173311, 181503, 180358, 180238, 234969, 124415, 124411,
                    154571, 124728, 154546, 120593, 69722, 124408, 172925, 67843, 172930, 154552, 140382,
                    180359, 79165, 172911, 233583, 235826, 98599, 56774, 184860, 201304, 144166
                ]

                dados_filtrados = dados.loc[indices_linhas]

                colunas_desejadas = [
                    'NR_CONVENIO', 'ID_PROPOSTA', 'SIT_CONVENIO', 'NR_PROCESSO', 'DIA_INIC_VIGENC_CONV',
                    'DIA_FIM_VIGENC_CONV', 'DIA_FIM_VIGENC_ORIGINAL_CONV', 'DIAS_PREST_CONTAS',
                    'DIA_LIMITE_PREST_CONTAS', 'QTD_TA', 'VL_GLOBAL_CONV', 'VL_REPASSE_CONV',
                    'VL_CONTRAPARTIDA_CONV', 'VL_EMPENHADO_CONV'
                ]

                dados_filtrados = dados_filtrados[colunas_desejadas]
                fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')
                hora_atual_brasilia = datetime.now(fuso_horario_brasilia).strftime('%Y-%m-%d %H:%M:%S')
                dados_filtrados['Hora_Modificacao_Brasilia'] = hora_atual_brasilia

                try:
                    os.remove(caminho_planilha)
                    os.remove(zip_file_path)
                except OSError as e:
                    print(f"Erro ao deletar arquivos: {e.strerror}")

with open('/Users/Lucas Rocha Dantas/Documents/Lucas Rocha Dantas/Vida profissional/Cypher/Cypher Tech/Projeto_para_o_Ministerio_da_Ciencia_e_Tecnologia_do_Brasil/credenciais.json', 'r') as file:
    credentials = json.load(file)

jwt_token = create_jwt(credentials)
token_data = {
    'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    'assertion': jwt_token
}
response = requests.post(credentials['token_uri'], data=token_data)
token = response.json().get('access_token')

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
payload = {
    'properties': {
        'title': 'Nome da Planilha'
    }
}
response = requests.post('https://sheets.googleapis.com/v4/spreadsheets', headers=headers, json=payload)
if response.status_code == 200:
    spreadsheet_data = response.json()
    spreadsheet_id = spreadsheet_data.get('spreadsheetId')

    # Imprimir o link da planilha criada
    print(f"Link da Planilha: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")

    drive_payload = {
        'role': 'writer',
        'type': 'anyone'
    }
    drive_response = requests.post(f'https://www.googleapis.com/drive/v3/files/{spreadsheet_id}/permissions', headers=headers, json=drive_payload)
    if drive_response.status_code == 200:
        upload_response = upload_data_to_sheet(dados_filtrados, spreadsheet_id, credentials)
    if upload_response.status_code == 200:
        print("Dados carregados para o Google Sheets com sucesso.")
    else:
        print("Falha ao carregar dados para o Google Sheets.", upload_response.text)
else:
    print("Falha ao criar a planilha.", response.text)