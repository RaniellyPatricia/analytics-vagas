import pandas as pd
from pathlib import Path
import re


PASTA_PROJETO = Path(__file__).resolve().parents[2]

CAMINHO_ENTRADA = (
    PASTA_PROJETO
    / "data"
    / "samples"
    / "programathor_amostra_45_vagas.csv"
)

CAMINHO_SAIDA = (
    PASTA_PROJETO
    / "data"
    / "processed"
    / "programathor_vagas_processadas.csv"
)

def limpar_espacos(valor):
    """
    Substitui espaços repetidos, tabulações e quebras de linha
    por um único espaço.
    """

    if pd.isna(valor):
        return ""

    texto = str(valor)

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()

colunas_textuais = [
    "titulo",
    "empresa",
    "tamanho_empresa",
    "contrato",
    "modalidade",
    "localizacao",
    "salario",
    "senioridade",
    "skills",
    "descricao_empresa",
    "atividades",
    "requisitos",
    "texto_completo",
]


df = pd.read_csv(CAMINHO_ENTRADA)

print("Base carregada com sucesso!")
print("Quantidade total de registros:", len(df))

# Mantém somente as vagas que não apresentaram erro.
df_validas = df[df["erro"].isna()].copy()

print("\nDepois de remover registros com erro:")
print("Quantidade de vagas válidas:", len(df_validas))


# Remove possíveis URLs duplicadas.
quantidade_antes = len(df_validas)

df_validas = (
    df_validas
    .drop_duplicates(subset=["url"])
    .copy()
)

quantidade_depois = len(df_validas)

print("\nVerificação de duplicidades:")
print("Quantidade antes:", quantidade_antes)
print("Quantidade depois:", quantidade_depois)
print(
    "Duplicidades removidas:",
    quantidade_antes - quantidade_depois
)

for coluna in colunas_textuais:
    df_validas[coluna] = (
        df_validas[coluna]
        .apply(limpar_espacos)
    )

print("\nExemplo após a padronização dos textos:")

print(
    df_validas[
        [
            "titulo",
            "skills",
            "requisitos"
        ]
    ]
    .head(3)
    .to_string(index=False)
)

# Cria um nome mais preciso para as etiquetas fornecidas pela plataforma.
df_validas["skills_plataforma"] = df_validas["skills"]

# Junta os campos que serão utilizados na análise textual.
df_validas["texto_analise"] = (
    df_validas["titulo"]
    + " "
    + df_validas["skills_plataforma"]
    + " "
    + df_validas["atividades"]
    + " "
    + df_validas["requisitos"]
)

# Padroniza os espaços no texto final.
df_validas["texto_analise"] = (
    df_validas["texto_analise"]
    .apply(limpar_espacos)
)

# Mede a quantidade de caracteres de cada texto.
df_validas["tamanho_texto_analise"] = (
    df_validas["texto_analise"]
    .str.len()
)

print("\nExemplo do texto criado para análise:")

print(
    df_validas[
        [
            "titulo",
            "skills_plataforma",
            "texto_analise"
        ]
    ]
    .head(2)
    .to_string(index=False)
)

print("\nTamanho dos textos de análise:")

print(
    df_validas["tamanho_texto_analise"]
    .describe()
)

# Reorganiza o índice das vagas.
df_validas = df_validas.reset_index(drop=True)

# Remove colunas redundantes da base processada.
df_validas = df_validas.drop(
    columns=[
        "skills",
        "erro",
    ]
)

# Cria a pasta de saída.
CAMINHO_SAIDA.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Salva a base depois das transformações.
df_validas.to_csv(
    CAMINHO_SAIDA,
    index=False,
    encoding="utf-8-sig"
)

print("\nBase processada salva com sucesso!")
print("Arquivo:")
print(CAMINHO_SAIDA)

print("\nQuantidade de vagas salvas:")
print(len(df_validas))

print("\nQuantidade de colunas:")
print(len(df_validas.columns))