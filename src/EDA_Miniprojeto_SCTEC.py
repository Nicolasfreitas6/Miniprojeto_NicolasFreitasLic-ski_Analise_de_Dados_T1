import csv
import re
import datetime
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

#Sprint 2: Transformação de Strings, Integer e Float e Datetime
#Lendo as primeiras linhas do DF para uma visualização inicial
print(df_varejo.head())

#Verificando o tamanho do DF (linhas e colunas)
print(f"\nDimensões do dataset: {df_varejo.shape[0]} linhas e {df_varejo.shape[1]} colunas.")

# Olhar os tipos de dados e se existem valores nulos
print("\n--- Informações Estruturais ---")
print(df_varejo.info())

#Função de Limpeza de Texto usando Expressões Regulares (Regex) e Métodos de String
def limpar_texto_regex(texto):
    if pd.isna(texto) or str(texto).strip() == "":
        return texto
    #Removendo múltiplos espaços em branco seguidos e substitui por um espaço único
    texto_limpo = re.sub(r'\s+', ' ', str(texto))
    #Retornando o texto sem espaços nas pontas e padronizado em maiúsculo
    return texto_limpo.strip().upper()

#Função de Conversão para Inteiro usando Regex
def converter_para_inteiro(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return "0"  #Mantém como string temporariamente para o tratamento de nulos na Sprint 3
    #Mantém apenas os caracteres que são dígitos numéricos
    apenas_numeros = re.sub(r'\D', '', str(valor))
    return int(apenas_numeros) if apenas_numeros else 0

#Função de Conversão para Decimal (Float) usando Métodos e Regex
def converter_para_float(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return 0.0
    # Substitui a vírgula decimal brasileira por ponto antes da conversão
    valor_ajustado = str(valor).replace(',', '.')
    # Remove qualquer caractere que não seja número ou ponto
    valor_limpo = re.sub(r'[^\d.]', '', valor_ajustado)
    return float(valor_limpo) if valor_limpo else 0.0


# --- Aplicando as funções de transformação de colunas ---

#Aplicando limpeza de texto nas colunas categóricas
colunas_texto = ['CL_GENERO', 'CL_SEG', 'PR_CAT', 'PR_NOME']
for col in colunas_texto:
    if col in df_varejo.columns:
        df_varejo[col] = df_varejo[col].apply(limpar_texto_regex)

#Aplicando conversão de inteiros nos IDs e na coluna de Filhos (CL_FHL)
colunas_inteiras = ['CO_ID', 'CL_ID', 'CL_EC', 'CL_FHL', 'PR_ID']
for col in colunas_inteiras:
    if col in df_varejo.columns:
        df_varejo[col] = df_varejo[col].apply(converter_para_inteiro)

#Procurando e aplicando tratamento float caso existam colunas de preço/valores ocultas
for col in df_varejo.columns:
    if any(termo in col.lower() for termo in ['valor', 'preco', 'venda', 'peso', 'altura']):
        df_varejo[col] = df_varejo[col].apply(converter_para_float)
        print(f"-> Coluna decimal identificada e convertida: {col}")

#Transformando a coluna de data em datetime
df_varejo['DATA'] = pd.to_datetime(df_varejo['DATA'], format='%d/%m/%Y')

#Verificando o resultado da Sprint 2
print("\n--- Visualização dos dados após transformações da Sprint 2 ---")
print(df_varejo.head())
print("\nNovos tipos de dados confirmados:")
print(df_varejo.dtypes)
print("="*50 + "\n")