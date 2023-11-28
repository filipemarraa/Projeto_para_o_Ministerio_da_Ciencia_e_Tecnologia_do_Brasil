import pandas as pd
import os
from datetime import datetime
import pytz

# Define o fuso horário de Brasília
fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')

# Caminho para o arquivo CSV original
caminho_para_csv_original = "/Users/filipemarra/Desktop/Projetos/Web_Scrapping/siconv_convenio.csv"

# Lê a planilha CSV original
df = pd.read_csv(caminho_para_csv_original)

# Lista as colunas que deseja manter
colunas_desejadas = ['NR_CONVENIO', 'ID_PROPOSTA', 'SIT_CONVENIO', 'NR_PROCESSO', 'DIA_INIC_VIGENC_CONV', 
                     'DIA_FIM_VIGENC_CONV', 'DIA_FIM_VIGENC_ORIGINAL_CONV', 'DIAS_PREST_CONTAS', 
                     'DIA_LIMITE_PREST_CONTAS', 'QTD_TA', 'VL_GLOBAL_CONV', 'VL_REPASSE_CONV', 
                     'VL_CONTRAPARTIDA_CONV', 'VL_EMPENHADO_CONV']

# Filtra o DataFrame para incluir apenas as colunas desejadas
df_filtrado = df[colunas_desejadas]

# Lista dos números de convênio desejados
numeros_convenio = ['01245010317202187', '01245003244202258', '01245007491202142', '01245007439202196', 
                    '01245001336202201', '01245006778202317', '01245004365202306', '01245004141202396', 
                    '01245009771202357', '01250025586201954', '01250025593201956', '01245010248202110', 
                    '01250025767201981', '01245010265202149', '01250030184201891', '01200004959201515', 
                    '01250025606201997', '01245004437202315', '01245001333202260', '01245001329202200', 
                    '01245001328202257', '01245007444202107', '01250016357202082', '01245004439202304', 
                    '01200001217201619', '01245003205202251', '01245004338202325', '01245005479202365', 
                    '01250030075201792', '01200002053201485', '01200002337201048', '01200007298200770', 
                    '01200004693200881', '01250024988202075']

# Filtra as linhas baseando-se nos números de convênio desejados
df_filtrado = df_filtrado[df_filtrado['NR_CONVENIO'].isin(numeros_convenio)]

# Obtém a data e hora atuais no fuso horário de Brasília
data_hora_atual_brasilia = datetime.now(fuso_horario_brasilia).strftime("%Y-%m-%d %H:%M:%S")

# Adiciona a data e hora de modificação como uma nova linha no DataFrame
df_modificacao = pd.DataFrame([[data_hora_atual_brasilia] + ['' for _ in range(len(colunas_desejadas) - 1)]], 
                              columns=['Data_Hora_Modificacao'] + colunas_desejadas[1:])
df_filtrado = df_filtrado.append(df_modificacao, ignore_index=True)

# Define o caminho para o novo arquivo CSV que será criado
caminho_para_csv_filtrado = '/Users/filipemarra/Desktop/Projetos/Web_Scrapping/planilha_filtrada.csv'

# Salva o DataFrame filtrado, agora incluindo a data e hora da modificação, no novo arquivo CSV
df_filtrado.to_csv(caminho_para_csv_filtrado, index=False)

# Tenta excluir o arquivo CSV original
try:
    os.remove(caminho_para_csv_original)
    print(f"O arquivo original foi excluído: {caminho_para_csv_original}")
except OSError as e:  # Captura a exceção se houver um erro
    print(f"Erro ao deletar o arquivo original: {e.strerror}")
