import requests
import json
import jwt
import datetime
import time

# Carregar o arquivo de credenciais
with open('/Users/Lucas Rocha Dantas/Documents/Lucas Rocha Dantas/Vida profissional/Cypher/Cypher Tech/Projeto_para_o_Ministerio_da_Ciencia_e_Tecnologia_do_Brasil/credenciais.json', 'r') as file:
    credentials = json.load(file)

# Função para criar uma JWT
def create_jwt(credentials):
    iat = datetime.datetime.now()
    exp = iat + datetime.timedelta(minutes=60)  # Token válido por 60 minutos
    jwt_payload = {
        "iss": credentials['client_email'],
        "scope": "https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/drive",  # Adicionado escopo do Google Drive
        "aud": credentials['token_uri'],
        "exp": int(time.mktime(exp.timetuple())),
        "iat": int(time.mktime(iat.timetuple()))
    }
    jwt_token = jwt.encode(jwt_payload, credentials['private_key'], algorithm='RS256')
    return jwt_token

# Obter a JWT
jwt_token = create_jwt(credentials)

# Obter um token de acesso
token_data = {
    'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    'assertion': jwt_token
}
response = requests.post(credentials['token_uri'], data=token_data)
token = response.json().get('access_token')

# Usar o token para criar uma planilha com a API do Google Sheets
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

    # Fazer a solicitação POST para a API do Google Drive para alterar as permissões da planilha
    drive_payload = {
        'role': 'reader',
        'type': 'anyone'
    }
    drive_response = requests.post(f'https://www.googleapis.com/drive/v3/files/{spreadsheet_id}/permissions',
                                   headers=headers, json=drive_payload)
    if drive_response.status_code == 200:
        print("Permissões alteradas. Planilha agora é de livre acesso.")
    else:
        print("Falha ao alterar as permissões da planilha.", drive_response.text)
else:
    print("Falha ao criar a planilha.", response.text)
