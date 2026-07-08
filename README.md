
Pipeline em Python para coleta, validação, limpeza e estruturação de vagas de tecnologia por web scraping.

## Sobre o projeto

Este projeto desenvolve um fluxo de coleta de dados de vagas de tecnologia a partir de páginas web, com foco em transformar informações não estruturadas de anúncios em uma base organizada e pronta para análise.

O objetivo principal é demonstrar um pipeline completo de dados, passando por:

- acesso à fonte de vagas;
- coleta automatizada das páginas;
- extração dos dados principais;
- validação da estrutura dos anúncios;
- limpeza e padronização dos textos;
- exportação da base em formato estruturado;
- preparação dos dados para análises futuras.

## Objetivo

Construir um pipeline em Python capaz de coletar, tratar e organizar dados de vagas de tecnologia publicadas em uma plataforma web.

## Tecnologias utilizadas

- Python
- Requests
- BeautifulSoup
- Pandas
- Regex
- CSV
- Jupyter Notebook

## Dados coletados

A coleta busca estruturar informações como:

- título da vaga;
- empresa;
- localização;
- modalidade de trabalho;
- nível de experiência;
- tecnologias ou habilidades citadas;
- descrição da vaga;
- link da vaga;
- data da coleta.

## Estrutura do projeto

```text
tech-jobs-scraping-pipeline/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── src/
│   ├── scraper.py
│   ├── parser.py
│   ├── cleaner.py
│   └── utils.py
│
├── README.md
├── requirements.txt
└── .gitignore
