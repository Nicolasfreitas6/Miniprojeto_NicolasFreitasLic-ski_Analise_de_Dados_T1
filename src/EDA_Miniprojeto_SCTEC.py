import csv
import re
from datetime import datetime
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

#Verificando o resultado da Sprint 2
print("\n--- Visualização dos dados após transformações da Sprint 2 ---")
print(df_varejo.head())
print("\nNovos tipos de dados confirmados:")
print(df_varejo.dtypes)
print("="*50 + "\n")

##Relatando dois problemas encontrados no Dataset:
#1. Inconsistência de Estrutura com Colunas Vazias, ao final de cada linha, existem vários pontos e vírgulas extras (;;;;), o que faz com que o interpretador crie colunas extras sem nome (vazias).
#2. Dados Faltantes (Nulos/Missing Values), ao analisar o conjunto, foi possível encontrar categorias de produtos que não possuem classificação e ID's de identificação com valores não preenchidos.

##Sprint 3: Limpeza de Nulos e Duplicatas
#Verificando valores nulos por coluna
print("Valores nulos por coluna:")
print(df_varejo.isnull().sum())

#Verificando valores duplicados por coluna
total_duplicatas = df_varejo.duplicated().sum()
print(f"\nTotal de linhas duplicadas: {total_duplicatas}")

#Removendo as linhas que são cópias exatas umas das outras, mantendo a primeira ocorrência.
df_varejo = df_varejo.drop_duplicates()

#Transformando a coluna de data em datetime
def converter_para_datetime(data_str):
    try:
        #Convertendo a string no formato Dia/Mês/Ano
        return datetime.strptime(str(data_str), '%d/%m/%Y')
    except ValueError:
        #Se a data for inválida ou vazia, retorna nulo (Not a Time)
        return pd.NaT

df_varejo['DATA'] = df_varejo['DATA'].apply(converter_para_datetime)

#Tratando categorias vazias
def preencher_categoria(categoria):
    # Se o valor for nulo (NaN) ou uma string vazia
    if pd.isna(categoria) or str(categoria).strip() == '':
        return 'Sem Categoria'
    else:
        return categoria
    
df_varejo['PR_CAT'] = df_varejo['PR_CAT'].apply(preencher_categoria)

#--- Justificativa da limpeza de nulos ---
#1. PR_CAT: Valores vazios foram imputados com "Sem Categoria" para não perdermos o registo  da compra do cliente, mantendo o volume de vendas correto e não afetando estatísticas.
#2. Identificadores (CO_ID, PR_ID, CL_ID): Registros sem o ID da compra, ID do produto ou ID do cliente são graves e poluem muito o dataset, pois, se não sabemos o que foi comprado, ou quem comprou, esse registo é inútil para qualquer cruzamento de dados. Como não podemos "adivinhar" o ID de um cliente ou de um produto, a única alternativa plausível é eliminar esses registos inválidos.
#3. CL_FHL (Número de filhos): Caso existam nulos nesta coluna, serão imputados com a mediana, para não distorcer a estatística, tendo em vista que a média é sensível a outliers.

#Removendo linhas onde os IDs essenciais são nulos
df_varejo = df_varejo.dropna(subset=['CO_ID', 'PR_ID', 'CL_ID'])

#Imputando nulos na coluna Número de Filhos (CL_FHL) com a mediana
mediana_filhos = df_varejo['CL_FHL'].median()

#Preenchendo os nulos e garante que o tipo se mantém inteiro
df_varejo['CL_FHL'] = df_varejo['CL_FHL'].fillna(mediana_filhos)

print("\nVerificação final após limpeza do Sprint 3:")
print("-" * 50)
print(f"Número de registos finais: {df_varejo.shape[0]}")
print(f"Total de duplicatas restantes: {df_varejo.duplicated().sum()}")
print("Valores nulos restantes por coluna:")
print(df_varejo.isnull().sum())
print("-" * 50)

##Sprint 4: Estatística Descritiva Básica
#Estatística básica da coluna de número de filhos
print("1. Estatísticas Descritivas para 'Número de Filhos' (CL_FHL):")

#Usando o método .describe() para calcular automaticamente estatísticas básicas e rápidas da coluna de número de filhos.
estatisticas_filhos = df_varejo['CL_FHL'].describe()
print(estatisticas_filhos)

#A moda (o valor que mais se repete) não vem no describe(), logo calculei à parte
moda_filhos = df_varejo['CL_FHL'].mode()[0]
print(f"Moda: {moda_filhos}")

##Aqui farei agrupamentos, como requisito para nota máxima, mas também, entender alguns questionamentos quanto ao dataset 
#Agrupamento 1: Qual é o genero que mais consome (em volume de itens)?
#Agrupei por Genero e contei a quantidade de IDs de produtos registados.
print("Agrupamento 1: Volume de itens comprados por Genero")
compras_por_genero = df_varejo.groupby('CL_GENERO')['PR_ID'].count().sort_values(ascending=False)
print(compras_por_genero)

#Agrupamento 2: Quais são as categorias com maior saída de produtos?
#Agrupei por Categoria e contei, ordenando do maior para o menor.
print("Agrupamento 2: Categorias de produtos mais vendidas")
categorias_mais_vendidas = df_varejo.groupby('PR_CAT')['PR_ID'].count().sort_values(ascending=False)
print(categorias_mais_vendidas)