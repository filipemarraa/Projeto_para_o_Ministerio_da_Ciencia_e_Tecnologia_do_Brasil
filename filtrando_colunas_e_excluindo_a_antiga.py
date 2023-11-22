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
colunas_desejadas = ['NR_CONVENIO', 'ID_PROPOSTA', 'SIT_CONVENIO']

# Filtra o DataFrame para incluir apenas as colunas desejadas
df_filtrado = df[colunas_desejadas]

# Filtra as linhas baseando-se na condição desejada
df_filtrado = df_filtrado[df_filtrado['SIT_CONVENIO'] == 'Cancelado']

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
