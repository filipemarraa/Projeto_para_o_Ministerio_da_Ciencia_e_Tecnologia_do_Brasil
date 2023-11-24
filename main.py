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

                    # Linhas específicas a serem filtradas
                    linhas_especificas = [
  
    "01245003244202258",
    "01245007491202142",
    "01245007439202196",
    "01245001336202201",
    "01245006778202317",
    "01245004365202306",
    "01245004141202396",
    "01245009771202357",
    "01250025586201954",
    "01250025593201956",
    "01245010248202110",
    "01250025767201981",
    "01245010265202149",
    "01250030184201891",
    "01200004959201515",
    "01250025606201997",  
    "01245010317202187",
    "01245004437202315",
    "01245001333202260",
    "01245001329202200",
    "01245001328202257",
    "01245007444202107",
    "01250016357202082",
    "01245004439202304",
    "01200001217201619",
    "01245003205202251",
    "01245004338202325",
    "01245005479202365",
    "01250030075201792",
    "01200002053201485",
    "01200002337201048",
    "01200007298200770",
    "01200004693200881",
    "01250024988202075",
]

                    # Colunas desejadas
                    colunas_desejadas = [
                        'NR_CONVENIO', 'ID_PROPOSTA', 'SIT_CONVENIO', 'NR_PROCESSO',
                        'DIA_INIC_VIGENC_CONV', 'DIA_FIM_VIGENC_CONV', 'DIA_FIM_VIGENC_ORIGINAL_CONV',
                        'DIAS_PREST_CONTAS', 'DIA_LIMITE_PREST_CONTAS', 'QTD_TA',
                        'VL_GLOBAL_CONV', 'VL_REPASSE_CONV', 'VL_CONTRAPARTIDA_CONV', 'VL_EMPENHADO_CONV'
                    ]

                    # Filtragem do DataFrame
                    df_filtrado = df[df['NR_CONVENIO'].isin(linhas_especificas)][colunas_desejadas]

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
