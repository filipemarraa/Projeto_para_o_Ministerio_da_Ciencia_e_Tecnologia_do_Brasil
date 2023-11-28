import requests
from bs4 import BeautifulSoup
import os
from zipfile import ZipFile
import pandas as pd
from datetime import datetime
import pytz

# Caminho base onde os arquivos serão salvos e manipulados
caminho_base = "/Users/imanichi/Documents/teste mcti"

# URL real do site que estamos raspando
url = 'https://repositorio.dados.gov.br/seges/detru/'

# Iniciando o download do arquivo zip
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        file_url = link.get('href')
        if file_url.endswith("convenio.csv.zip"):
            file_response = requests.get(url + file_url, stream=True)
            if file_response.status_code == 200:
                with open(os.path.join(caminho_base, file_url), 'wb') as file:  # Alteração aqui
                    for chunk in file_response.iter_content(chunk_size=128):
                        file.write(chunk)
                print(f"Download de {file_url} completo.")

                # Processo de descompactação
                zip_file_path = os.path.join(caminho_base, file_url)
                try:
                    with ZipFile(zip_file_path, 'r') as arq:
                        arq.extractall(caminho_base)
                    print(f"O arquivo {file_url} foi descompactado com sucesso!!")

                    # Após descompactação, iremos filtrar a planilha
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

                    # Definir o fuso horario
                    fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')

                    # Obter a hora atual
                    hora_atual_brasilia = datetime.now(fuso_horario_brasilia).strftime('%Y-%m-%d %H:%M:%S')

                    # inserir nova coluna
                    dados_filtrados['Hora_Modificacao_Brasilia'] = hora_atual_brasilia

                    caminho_nova_planilha = os.path.join(caminho_base, "planilha_filtrada.csv")
                    dados_filtrados.to_csv(caminho_nova_planilha, index=False)

                    # Excluir o arquivo antigo
                    caminho_planilha_zip = "/Users/imanichi/Documents/teste mcti/siconv_convenio.csv.zip"
                    try:
                        os.remove(caminho_planilha)
                        os.remove(caminho_planilha_zip)
                        print(f"O arquivo original foi excluído: {caminho_planilha}")
                        print(f"O arquivo original zip foi excluído: {caminho_planilha_zip}")
                    except OSError as e:
                        print(f"Erro ao deletar o arquivo original: {e.strerror}")
                        print(f"Erro ao deletar o arquivo zip original: {e.strerror}")
                    except Exception as e:
                        print(f"Erro ao descompactar ou processar o arquivo {file_url}: {e}")
                except Exception as e:
                    print(f"Erro ao descompactar ou processar o arquivo {file_url}: {e}")
else:
    print("Falha ao acessar a página.")
