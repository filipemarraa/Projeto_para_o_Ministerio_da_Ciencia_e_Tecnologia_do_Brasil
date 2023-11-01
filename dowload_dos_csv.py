import requests
from bs4 import BeautifulSoup

# URL real do site que você estamos raspando
url = 'https://repositorio.dados.gov.br/seges/detru/'

# Fazendo uma solicitação para a página
response = requests.get(url)

# Verificando se a solicitação foi bem-sucedida
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrando o link para o arquivo desejado
    file_link = None
    for link in soup.find_all('a'):
        if 'siconv.zip' in link.get('href'):
            file_link = link.get('href')
            break

    if file_link:
        # Fazendo o download do arquivo
        file_response = requests.get(url + file_link, stream=True)
        if file_response.status_code == 200:
            with open('siconv.zip', 'wb') as file:
                for chunk in file_response.iter_content(chunk_size=128):
                    file.write(chunk)
            print("Download completo.")
        else:
            print("Falha ao baixar o arquivo.")
    else:
        print("Link para o arquivo não encontrado.")
else:
    print("Falha ao acessar a página.")
