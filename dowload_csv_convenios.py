import requests
from bs4 import BeautifulSoup

# URL real do site que estamos raspando
url = 'https://repositorio.dados.gov.br/seges/detru/'

# Fazendo uma solicitação para a página
response = requests.get(url)

# Verificando se a solicitação foi bem-sucedida
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrando o link para o arquivo desejado
    for link in soup.find_all('a'):
        file_url = link.get('href')
        if file_url.endswith("convenio.csv.zip"):
            # Fazendo o download do arquivo
            file_response = requests.get(url + file_url, stream=True)
            if file_response.status_code == 200:
                with open(file_url, 'wb') as file:
                    for chunk in file_response.iter_content(chunk_size=128):
                        file.write(chunk)
                print(f"Download de {file_url} completo.")
            else:
                print(f"Falha ao baixar o arquivo {file_url}.")
else:
    print("Falha ao acessar a página.")
