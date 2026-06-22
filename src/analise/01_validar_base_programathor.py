import pandas as pd
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parents[2]

CAMINHO_ARQUIVO = (
    PASTA_PROJETO
    / "data"
    / "samples"
    / "programathor_amostra_15_vagas.csv"
)

df = pd.read_csv(CAMINHO_ARQUIVO)

print("Base carregada com sucesso!")
print("Quantidade de linhas:", df.shape[0])
print("Quantidade de colunas:", df.shape[1])

print("\nColunas da base:")

for coluna in df.columns:
    print("-", coluna)

print("\nValores vazios por coluna:")
print(df.isna().sum())

quantidade_urls_duplicadas = df["url"].duplicated().sum()

print("\nQuantidade de URLs duplicadas:")
print(quantidade_urls_duplicadas)

salarios_nao_especificados = (
    df["salario"]
    .fillna("")
    .str.lower()
    .str.contains("não especificado")
    .sum()
)

print("\nQuantidade de salários não especificados:")
print(salarios_nao_especificados)

df["tamanho_requisitos"] = (
    df["requisitos"]
    .fillna("")
    .str.len()
)

df["tamanho_atividades"] = (
    df["atividades"]
    .fillna("")
    .str.len()
)

print("\nMenores textos de requisitos:")

print(
    df[
        [
            "titulo",
            "tamanho_requisitos"
        ]
    ]
    .sort_values("tamanho_requisitos")
    .head()
)

problemas = df[
    (df["titulo"].isna())
    | (df["empresa"].isna())
    | (df["skills"].isna())
    | (df["requisitos"].isna())
    | (df["tamanho_requisitos"] < 50)
    | (df["erro"].notna())
]

print("\nVagas com possíveis problemas:")

if problemas.empty:
    print("Nenhum problema estrutural encontrado.")
else:
    print(
        problemas[
            [
                "titulo",
                "empresa",
                "skills",
                "tamanho_requisitos",
                "erro",
                "url"
            ]
        ].to_string(index=False)
    )