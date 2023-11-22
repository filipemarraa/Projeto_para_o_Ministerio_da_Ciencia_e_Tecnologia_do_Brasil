import requests
from bs4 import BeautifulSoup
import os
from zipfile import ZipFile
import pandas as pd
from datetime import datetime
import pytz

# Caminho base onde os arquivos serão salvos e manipulados
caminho_base = "/Users/filipemarra/Desktop/Projetos/Web_Scrapping"

# URL real do site que estamos raspando
url = 'https://repositorio.dados.gov.br/seges/detru/'

# Iniciando o processo de download do arquivo .zip
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
                
                # Processo de descompactação
                zip_file_path = os.path.join(caminho_base, file_url)
                try:
                    with ZipFile(zip_file_path, 'r') as arq:
                        arq.extractall(caminho_base)
                    print(f"O arquivo {file_url} foi descompactado com sucesso!!")
                    
                    # Após a descompactação, podemos continuar com a filtragem da planilha
                    caminho_para_csv_original = os.path.join(caminho_base, 'siconv_convenio.csv')  # Ajuste o nome do arquivo CSV conforme o real nome do arquivo extraído
                    df = pd.read_csv(caminho_para_csv_original)

                    # Definição das colunas desejadas e filtragem do DataFrame
                    colunas_desejadas = ['NR_CONVENIO', 'ID_PROPOSTA', 'SIT_CONVENIO']
                    df_filtrado = df[colunas_desejadas]
                    df_filtrado = df_filtrado[df_filtrado['SIT_CONVENIO'] == 'Cancelado']

                    # Adição da data e hora da última modificação
                    fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')
                    data_hora_atual_brasilia = datetime.now(fuso_horario_brasilia).strftime("%Y-%m-%d %H:%M:%S")
                    df_modificacao = pd.DataFrame([[data_hora_atual_brasilia] + ['' for _ in range(len(colunas_desejadas) - 1)]],
                                                  columns=['Data_Hora_Modificacao'] + colunas_desejadas[1:])
                    df_filtrado = df_filtrado.append(df_modificacao, ignore_index=True)

                    # Salvando o DataFrame filtrado e excluindo o original
                    caminho_para_csv_filtrado = os.path.join(caminho_base, 'planilha_filtrada.csv')
                    df_filtrado.to_csv(caminho_para_csv_filtrado, index=False)
                    os.remove(caminho_para_csv_original)
                    print(f"O arquivo original foi excluído: {caminho_para_csv_original}")

                except Exception as e:
                    print(f"Erro ao descompactar ou processar o arquivo {file_url}: {e}")
            else:
                print(f"Falha ao baixar o arquivo {file_url}.")
else:
    print("Falha ao acessar a página.")



'''
1 - Baixa o arquivo .zip do site especificado.
2 - Descompacta o arquivo .zip para obter o .csv.
3 - Lê o .csv, filtra as colunas e as linhas desejadas, e adiciona uma linha com a data e hora da modificação.
4 - Salva a nova planilha filtrada.
5 - Exclui a planilha original.
'''