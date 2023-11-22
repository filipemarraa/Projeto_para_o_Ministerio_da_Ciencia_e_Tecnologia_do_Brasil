# Projeto de Automatização para o Ministério da Ciência e Tecnologia do Brasil

Este projeto visa automatizar processos manuais no âmbito do Ministério da Ciência e Tecnologia do Brasil, contribuindo para a otimização e eficiência das operações internas.

## Sobre o Projeto

O projeto foi desenvolvido por um grupo de cinco alunos da faculdade IDP, com o objetivo de oferecer soluções inovadoras para o Ministério da Ciência e Tecnologia. Ao automatizar processos manuais, esperamos reduzir a carga de trabalho manual e liberar recursos para atividades mais estratégicas e de alto valor agregado.

## Alunos

- Filipe Jacobson Marra
- Pedro Henrique Imanichi
- Luca Braggio
- Lucas Rocha Dantas
- Matheus

## Funcionalidades Principais

Neste projeto, implementamos as seguintes funcionalidades principais:

- Automatização de planilhas e controle de prazos.

# Especificações técnicas

## Etapa 1: Download dos Arquivos

 - O script começa importando os módulos necessários e estabelecendo o caminho base onde os arquivos serão salvos e manipulados. Ele usa requests para fazer uma solicitação HTTP GET à URL fornecida. Se a resposta for bem-sucedida (código de status HTTP 200), o Beautiful Soup é usado para analisar o conteúdo HTML e encontrar todos os links.

- O código procura um link que termina com "convenio.csv.zip" (o arquivo de interesse) e, quando encontrado, realiza o download do arquivo .zip em blocos de 128 bytes para evitar o uso excessivo de memória, especialmente útil para arquivos grandes.

## Etapa 2: Descompactação dos Arquivos

- Após o download bem-sucedido, o script tenta descompactar o arquivo .zip usando o módulo ZipFile. Ele extrai o conteúdo do arquivo .zip para o diretório especificado em caminho_base. Se a descompactação for bem-sucedida, o script imprime uma mensagem de confirmação.

## Etapa 3: Filtragem e Processamento dos Dados

- Com os dados descompactados disponíveis, o script lê o arquivo CSV original em um DataFrame do pandas. Ele define as colunas de interesse e filtra o DataFrame com base na condição desejada (neste caso, mantendo linhas onde SIT_CONVENIO é igual a 'Cancelado').

- Além disso, o script usa o módulo pytz para lidar com fusos horários e adicionar uma linha com a data e hora atuais no fuso horário de Brasília. Isso é feito criando um novo DataFrame com a data e hora e, em seguida, anexando-o ao DataFrame filtrado.

- Finalmente, o DataFrame resultante é salvo em um novo arquivo CSV, e o arquivo CSV original é excluído para não deixar dados desnecessários no sistema.

## Considerações Adicionais

- O script é bloqueante, o que significa que cada operação precisa ser concluída antes que a próxima comece.
- Não são usadas estruturas condicionais (if/else) para controlar o fluxo além das já fornecidas, pois cada etapa já depende da conclusão bem-sucedida da etapa anterior.
- O script trata exceções básicas, mas pode ser expandido para lidar com erros de rede, descompactação e leitura de arquivos de forma mais robusta.
- O script pressupõe que o arquivo .zip contém um arquivo CSV com o nome 'siconv_convenio.csv'. Se o nome do arquivo dentro do .zip for diferente, será necessário ajustar o script para usar o nome correto.
- O código usa a impressão de mensagens de console para informar o usuário sobre o progresso e os erros, o que é útil para depuração e acompanhamento do processo quando executado.

## Instalação

Para utilizar o projeto, siga estas instruções:

1. Clone este repositório em sua máquina local.
2. Execute o comando `npm install` para instalar todas as dependências.
3. Execute o comando `npm start` para iniciar o servidor.



