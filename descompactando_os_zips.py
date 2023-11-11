import os
from zipfile import ZipFile

caminho = "/Users/filipemarra/Desktop/Projetos/Web_Scrapping"
zip_encontrado = False

for item in os.listdir(caminho):
    if item.endswith('.zip'):
        zip_encontrado = True
        try:
            arq = ZipFile(os.path.join(caminho, item), 'r')
            arq.extractall(caminho)  # Aqui, o segundo argumento define o diretório para onde extrair os arquivos
            arq.close()
            print(f"O arquivo {item} foi descompactado com sucesso!!")
        except Exception as e:
            print(f"Erro ao descompactar o arquivo {item}: {e}")

if not zip_encontrado:
    print("Nenhum arquivo .zip encontrado no diretório.")

