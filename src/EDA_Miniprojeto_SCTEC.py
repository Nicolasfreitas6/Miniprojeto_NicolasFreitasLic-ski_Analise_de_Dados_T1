import csv
import pandas as pd

##Sprint 1: Importação dos dados
#Criando uma lista vazia para armazenar os dados lidos
dados_brutos = []


#Lendo arquivo CSV, com o modo leitura ("r"), usando codificação UTF-8 e 'with' para garantir que o arquivo será fechado automaticamente após ser executado.
with open('data/Varejo.csv', 'r', encoding='utf-8') as arq:
    leitor_csv = csv.DictReader(arq, delimiter=';')

    for linha in leitor_csv:
        dados_brutos.append(linha)

print("Leitura do csv.DictReader concluída com sucesso!\n")

#Transformando a lista em DataFrame pois o documento do desafio determina os dois pontos.
df_varejo = pd.DataFrame(dados_brutos)

#Removendo colunas que não têm nome (geradas como '' ou None pelo DictReader), isso acontece, devido aos vários ponto e vírgula do csv.
df_varejo = df_varejo.loc[:, ~df_varejo.columns.isin(['', None])]

print("-" * 40)
print("Informações Iniciais da Base de Dados")
print("-" * 40)
print(f"Número de registros (linhas): {df_varejo.shape[0]}")
print(f"Número de colunas: {df_varejo.shape[1]}")
print("\nTipos de dados por coluna:")
print(df_varejo.dtypes)
print("-" * 40)