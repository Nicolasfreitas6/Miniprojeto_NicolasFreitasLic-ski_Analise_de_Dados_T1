# Projeto: Análise Exploratória de Dados (AED) - Varejo - SCTEC

## Descrição
Este projeto realiza uma Análise Exploratória de Dados (EDA) da base de Varejo fornecida pela SCTEC, focando em limpeza, tratamento de inconsistências e extração de estatísticas descritivas. O objetivo é transformar dados brutos em informações úteis para suporte à decisão.

## Reflexão Teórica (ETL e Qualidade de Dados)
O processo de ETL (*Extract, Transform, Load*) aplicado foi fundamental para garantir a integridade dos dados:

- **Extração:** Realizada via `csv.DictReader` para garantir uma leitura estruturada nativa, posteriormente, foi transformado o csv em um DataFrame utilizando o Pandas, com o objetivo de cumprir os requisitos elencados no documento do mini-projeto, onde ambos eram pedidos, e para facilidade de manuseio dos dados;

- **Transformação:** Apliquei técnicas de limpeza de dados (*Data Cleaning*). Removi duplicatas e tratei campos nulos (inclusive, imputando pela mediana em campos numéricos e rotulando como "Sem Categoria" em campos de texto) para evitar a perda de registos de vendas e manter a precisão das estatísticas;

- **Qualidade de Dados:** Foram identificados dois problemas críticos, que foram descritos em comentários durante o código: 
    (1) Estrutura do arquivo corrompida por delimitadores extras. Ao final de cada linha, existem vários pontos e vírgulas extras (;;;;), o que faz com que o interpretador crie colunas extras sem nome (vazias), e com isso, gere 'ruídos' nos dados, ocupando memória desnecessária e dificultando a leitura direta por ferramentas de BI, pois colunas sem nome ou vazias podem ser interpretadas erroneamente como dados reais.

    (2) Dados faltantes em campos-chave. O tratamento destes itens assegura que o nosso relatório não seja distorcido, pois, haviam colunas como a de 'Categorias de Produtos' (PR_CAT), e também, ID's de identificação (CO_ID) e (CL_ID), o que acaba por inviabilizar a rastreabilidade do histórico de compras, podendo enviesar análises.

## Insights Obtidos
1. **Padrão de Família:** A moda do número de filhos dos clientes é 0, indicando que a maior parte da base é composta por clientes sem dependentes.

2. **Preferência de Categoria:** O setor de 'Alimentos' lidera o volume de compras com um volume muito superior, com Higiene logo após, se aproximando das demais categorias.

3. **Distribuição de Gênero:** O Gênero 'F', de feminino, apresenta um volume superior de transações, apesar de ser próximo ao do masculino.

4. **Qualidade:** A limpeza reduziu significativamente o ruído do arquivo original, tornando a base apta para futuras modelagens.

## Como Executar
Este projeto foi estruturado para ser executado tanto localmente quanto em ambientes de nuvem (como o Google Colab). Siga os passos abaixo:

**1. Clonar o Repositório:**
Abra o seu terminal (ou Git Bash) na pasta onde deseja salvar o projeto e execute o comando de clone:

    - git clone [https://github.com/Nicolasfreitas6/Miniprojeto_NicolasFreitasLic-ski_Analise_de_Dados_T1.git](https://github.com/Nicolasfreitas6/Miniprojeto_NicolasFreitasLic-ski_Analise_de_Dados_T1.git)
    - cd Miniprojeto_NicolasFreitasLic-ski_Analise_de_Dados_T1

**2. Instale as bibliotecas necessárias:** `pip install pandas`.

**3. Direcionamento do arquivo de DataFrame:** Certifique-se de que o arquivo `df_limpo_varejo.csv` está no mesmo diretório.

    _Obs:_ O arquivo 'Varejo.csv' dentro da pasta 'data' é o csv 'sujo', fornecido pela SCTEC para realizar a análise. O arquivo 'df_limpo_varejo csv' é o arquivo onde as limpezas foram realizadas.
    
**4. Execute o script principal:** `python EDA_Miniprojeto_SCTEC.py`.