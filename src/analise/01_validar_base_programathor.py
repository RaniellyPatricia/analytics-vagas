import pandas as pd
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parents[2]

CAMINHO_ARQUIVO = (
    PASTA_PROJETO
    / "data"
    / "samples"
    / "programathor_amostra_45_vagas.csv"
)


# ============================================================
# CARREGAMENTO DA BASE
# ============================================================

df = pd.read_csv(CAMINHO_ARQUIVO)

# Primeiro separamos as vagas válidas e as vagas com erro.
df_validas = df[df["erro"].isna()].copy()
df_com_erro = df[df["erro"].notna()].copy()


print("Base carregada com sucesso!")
print("Quantidade total de linhas:", df.shape[0])
print("Quantidade de colunas:", df.shape[1])


# ============================================================
# COLUNAS DA BASE
# ============================================================

print("\nColunas da base:")

for coluna in df.columns:
    print("-", coluna)


# ============================================================
# VALORES VAZIOS NAS VAGAS VÁLIDAS
# ============================================================

print("\nValores vazios nas vagas válidas:")
print(df_validas.isna().sum())


# ============================================================
# URLs DUPLICADAS
# ============================================================

quantidade_urls_duplicadas = (
    df["url"]
    .duplicated()
    .sum()
)

print("\nQuantidade de URLs duplicadas:")
print(quantidade_urls_duplicadas)


# ============================================================
# SALÁRIOS NÃO ESPECIFICADOS
# ============================================================

salarios_nao_especificados = (
    df_validas["salario"]
    .fillna("")
    .str.lower()
    .str.contains("não especificado")
    .sum()
)

print("\nQuantidade de salários não especificados:")
print(salarios_nao_especificados)

if len(df_validas) > 0:
    percentual_salarios_nao_especificados = (
        salarios_nao_especificados
        / len(df_validas)
        * 100
    )

    print(
        "Percentual de salários não especificados:",
        round(percentual_salarios_nao_especificados, 2),
        "%"
    )


# ============================================================
# TAMANHO DOS TEXTOS
# ============================================================

df_validas["tamanho_requisitos"] = (
    df_validas["requisitos"]
    .fillna("")
    .str.len()
)

df_validas["tamanho_atividades"] = (
    df_validas["atividades"]
    .fillna("")
    .str.len()
)


print("\nMenores textos de requisitos:")

print(
    df_validas[
        [
            "titulo",
            "tamanho_requisitos"
        ]
    ]
    .sort_values("tamanho_requisitos")
    .head()
    .to_string(index=False)
)


# ============================================================
# PROBLEMAS ESTRUTURAIS NAS VAGAS VÁLIDAS
# ============================================================

problemas = df_validas[
    (df_validas["titulo"].isna())
    | (df_validas["empresa"].isna())
    | (df_validas["skills"].isna())
    | (df_validas["requisitos"].isna())
    | (df_validas["tamanho_requisitos"] < 50)
]


print("\nVagas com possíveis problemas estruturais:")

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
                "url"
            ]
        ].to_string(index=False)
    )


# ============================================================
# RESUMO DA COLETA
# ============================================================

print("\nResumo final da coleta:")
print("Total de URLs encontradas:", len(df))
print("Vagas válidas para análise:", len(df_validas))
print("Vagas indisponíveis:", len(df_com_erro))

if len(df) > 0:
    taxa_sucesso = (
        len(df_validas)
        / len(df)
        * 100
    )

    print(
        "Taxa de sucesso:",
        round(taxa_sucesso, 2),
        "%"
    )


# ============================================================
# VAGAS INDISPONÍVEIS
# ============================================================

print("\nVagas indisponíveis na fonte:")

if df_com_erro.empty:
    print("Nenhuma vaga indisponível.")
else:
    print(
        df_com_erro[
            [
                "url",
                "erro"
            ]
        ].to_string(index=False)
    )