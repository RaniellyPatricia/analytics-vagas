import re
import time
import unicodedata
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup


# ============================================================
# CONFIGURAÇÕES
# ============================================================

BASE_URL = "https://www.programathor.com.br"
LIST_URL = "https://www.programathor.com.br/jobs"

# Quantidade de páginas que serão percorridas.
MAX_PAGINAS = 3

# Pausa entre o acesso a cada vaga individual.
TEMPO_ENTRE_REQUISICOES = 2

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}


# Encontra automaticamente a pasta principal do projeto.
PASTA_PROJETO = Path(__file__).resolve().parents[2]

CAMINHO_SAIDA = (
    PASTA_PROJETO
    / "data"
    / "samples"
    / "programathor_amostra_45_vagas.csv"
)


COLUNAS = [
    "fonte",
    "data_coleta",
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
    "url",
    "erro",
]


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def baixar_html(url):
    """
    Acessa uma página e devolve o HTML recebido.
    """

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return response.text


def normalizar(texto):
    """
    Padroniza o texto para facilitar comparações.

    Exemplo:
    'Localização' -> 'localizacao'
    """

    if texto is None:
        return ""

    texto = str(texto).strip().lower()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    return texto


def preparar_linhas(soup):
    """
    Transforma o texto da página em uma lista de linhas limpas.
    """

    texto = soup.get_text(
        "\n",
        strip=True
    )

    linhas = texto.split("\n")

    linhas_limpas = []

    for linha in linhas:
        linha = linha.strip()

        if linha:
            linhas_limpas.append(linha)

    return linhas_limpas


def encontrar_indice(
    linhas,
    texto_procurado,
    inicio=0
):
    """
    Procura uma linha exatamente igual ao texto informado.
    """

    texto_normalizado = normalizar(
        texto_procurado
    )

    for indice in range(
        inicio,
        len(linhas)
    ):
        if normalizar(linhas[indice]) == texto_normalizado:
            return indice

    return None


def encontrar_linha_que_comeca_com(
    linhas,
    prefixo,
    inicio=0
):
    """
    Procura uma linha que comece com determinado prefixo.
    """

    prefixo_normalizado = normalizar(
        prefixo
    )

    for indice in range(
        inicio,
        len(linhas)
    ):
        linha_normalizada = normalizar(
            linhas[indice]
        )

        if linha_normalizada.startswith(
            prefixo_normalizado
        ):
            return indice

    return None


def montar_url_pagina(numero_pagina):
    """
    Monta a URL de uma página da listagem.
    """

    if numero_pagina == 1:
        return LIST_URL

    return f"{LIST_URL}?page={numero_pagina}"


# ============================================================
# EXTRAÇÃO DE LINKS
# ============================================================

def extrair_links_vagas(html):
    """
    Encontra links únicos de vagas na página de listagem.
    """

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    links_html = soup.find_all(
        "a",
        href=True
    )

    links_vagas = []

    for link in links_html:
        href = link["href"]

        if re.search(
            r"/jobs/\d+",
            href
        ):
            url_completa = urljoin(
                BASE_URL,
                href
            )

            url_completa = url_completa.split(
                "?"
            )[0]

            links_vagas.append(
                url_completa
            )

    links_vagas = list(
        dict.fromkeys(links_vagas)
    )

    return links_vagas


# ============================================================
# EXTRAÇÃO DE SEÇÕES
# ============================================================

def extrair_secao(
    linhas,
    nome_secao,
    secoes_de_parada,
    inicio_busca=0
):
    """
    Extrai o texto localizado entre uma seção e outra.
    """

    indice_inicio_secao = encontrar_indice(
        linhas,
        nome_secao,
        inicio_busca
    )

    if indice_inicio_secao is None:
        return None

    inicio_conteudo = indice_inicio_secao + 1
    fim_conteudo = len(linhas)

    for secao in secoes_de_parada:
        indice_parada = encontrar_indice(
            linhas,
            secao,
            inicio_conteudo
        )

        if indice_parada is not None:
            fim_conteudo = min(
                fim_conteudo,
                indice_parada
            )

    conteudo = linhas[
        inicio_conteudo:
        fim_conteudo
    ]

    texto_secao = " ".join(
        conteudo
    ).strip()

    if texto_secao:
        return texto_secao

    return None


# ============================================================
# EXTRAÇÃO DE UMA VAGA
# ============================================================

def extrair_dados_vaga(url_vaga):
    """
    Acessa uma vaga individual e extrai seus campos.
    """

    html = baixar_html(
        url_vaga
    )

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    linhas = preparar_linhas(
        soup
    )

    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    titulo_tag = soup.find("h1")

    if titulo_tag:
        titulo = titulo_tag.get_text(
            strip=True
        )
    else:
        titulo = None

    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    indice_inicio = encontrar_indice(
        linhas,
        "Início"
    )

    skills = []

    if titulo and indice_inicio is not None:
        indice_titulo_antes_inicio = None

        for indice in range(
            0,
            indice_inicio
        ):
            if normalizar(
                linhas[indice]
            ) == normalizar(titulo):
                indice_titulo_antes_inicio = indice

        if indice_titulo_antes_inicio is not None:
            skills = linhas[
                indice_titulo_antes_inicio + 1:
                indice_inicio
            ]

    # --------------------------------------------------------
    # LOCALIZA O TÍTULO PRINCIPAL
    # --------------------------------------------------------

    indice_titulo_principal = None

    if titulo and indice_inicio is not None:
        for indice in range(
            indice_inicio,
            len(linhas)
        ):
            if normalizar(
                linhas[indice]
            ) == normalizar(titulo):
                indice_titulo_principal = indice
                break

    if indice_titulo_principal is not None:
        inicio_busca = indice_titulo_principal
    else:
        inicio_busca = 0

    # --------------------------------------------------------
    # LIMITA OS METADADOS
    # --------------------------------------------------------

    indice_descricao = encontrar_indice(
        linhas,
        "Descrição da empresa",
        inicio_busca
    )

    if indice_descricao is None:
        fim_metadados = len(linhas)
    else:
        fim_metadados = indice_descricao

    linhas_metadados = linhas[
        inicio_busca:
        fim_metadados
    ]

    # --------------------------------------------------------
    # EMPRESA
    # --------------------------------------------------------

    empresa = None

    if indice_titulo_principal is not None:
        proximo_indice = (
            indice_titulo_principal + 1
        )

        if proximo_indice < len(linhas):
            empresa = linhas[
                proximo_indice
            ]

            if normalizar(
                empresa
            ) == "vaga externa":
                segundo_indice = (
                    proximo_indice + 1
                )

                if segundo_indice < len(linhas):
                    empresa = linhas[
                        segundo_indice
                    ]

    # --------------------------------------------------------
    # TAMANHO DA EMPRESA
    # --------------------------------------------------------

    tamanho_empresa = None

    opcoes_tamanho_empresa = [
        "Pequena/média empresa",
        "Grande empresa",
        "Startup",
    ]

    for linha in linhas_metadados:
        if linha in opcoes_tamanho_empresa:
            tamanho_empresa = linha
            break

    # --------------------------------------------------------
    # CONTRATO
    # --------------------------------------------------------

    contrato = None

    opcoes_contrato = [
        "CLT",
        "PJ",
        "Estágio",
        "CLT / PJ",
        "Cooperado",
        "Freelancer",
    ]

    for linha in linhas_metadados:
        if linha in opcoes_contrato:
            contrato = linha
            break

    # --------------------------------------------------------
    # MODALIDADE
    # --------------------------------------------------------

    modalidade = None

    for linha in linhas_metadados:
        linha_normalizada = normalizar(
            linha
        )

        if "home office" in linha_normalizada:
            modalidade = "Remoto"
            break

        if "remoto" in linha_normalizada:
            modalidade = "Remoto"

        elif "hibrido" in linha_normalizada:
            modalidade = "Híbrido"

        elif "presencial" in linha_normalizada:
            modalidade = "Presencial"

    # --------------------------------------------------------
    # LOCALIZAÇÃO
    # --------------------------------------------------------

    localizacao = None

    indice_localizacao = encontrar_indice(
        linhas,
        "Localização:",
        inicio_busca
    )

    if indice_localizacao is not None:
        proximo_indice = (
            indice_localizacao + 1
        )

        if proximo_indice < len(linhas):
            localizacao = linhas[
                proximo_indice
            ]

    # --------------------------------------------------------
    # SALÁRIO
    # --------------------------------------------------------

    salario = None

    indice_salario = encontrar_linha_que_comeca_com(
        linhas,
        "Salário:",
        inicio_busca
    )

    if indice_salario is not None:
        salario = re.sub(
            r"^Salário:\s*",
            "",
            linhas[indice_salario],
            flags=re.IGNORECASE
        ).strip()

    # --------------------------------------------------------
    # SENIORIDADE
    # --------------------------------------------------------

    senioridade = None

    opcoes_senioridade = [
        "Estágio",
        "Trainee",
        "Júnior",
        "Junior",
        "Pleno",
        "Sênior",
        "Senior",
        "Especialista",
    ]

    for linha in linhas_metadados:
        if linha in opcoes_senioridade:
            senioridade = linha
            break

    # --------------------------------------------------------
    # SEÇÕES TEXTUAIS
    # --------------------------------------------------------

    descricao_empresa = extrair_secao(
        linhas,
        "Descrição da empresa",
        [
            "Atividades e Responsabilidades",
            "Requisitos",
        ],
        inicio_busca
    )

    atividades = extrair_secao(
        linhas,
        "Atividades e Responsabilidades",
        [
            "Requisitos",
        ],
        inicio_busca
    )

    requisitos = extrair_secao(
        linhas,
        "Requisitos",
        [
            "O que nós oferecemos",
            "Benefícios",
            "Diferenciais da empresa",
            "Seu perfil combina em ...%",
            "Cadastre-se para descobrir sua compatibilidade",
        ],
        inicio_busca
    )

    vaga = {
        "fonte": "ProgramaThor",
        "data_coleta": datetime.now().strftime(
            "%Y-%m-%d"
        ),
        "titulo": titulo,
        "empresa": empresa,
        "tamanho_empresa": tamanho_empresa,
        "contrato": contrato,
        "modalidade": modalidade,
        "localizacao": localizacao,
        "salario": salario,
        "senioridade": senioridade,
        "skills": ", ".join(skills),
        "descricao_empresa": descricao_empresa,
        "atividades": atividades,
        "requisitos": requisitos,
        "texto_completo": " ".join(linhas),
        "url": url_vaga,
        "erro": None,
    }

    return vaga


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main():
    print("=" * 65)
    print("COLETA DE MÚLTIPLAS PÁGINAS DA PROGRAMATHOR")
    print("=" * 65)

    todos_links = []

    # --------------------------------------------------------
    # COLETA DOS LINKS DAS PÁGINAS
    # --------------------------------------------------------

    for numero_pagina in range(
        1,
        MAX_PAGINAS + 1
    ):
        url_pagina = montar_url_pagina(
            numero_pagina
        )

        print("\n" + "-" * 65)
        print(
            "Coletando links da página:",
            numero_pagina
        )
        print("URL:", url_pagina)

        try:
            html_listagem = baixar_html(
                url_pagina
            )

            links_pagina = extrair_links_vagas(
                html_listagem
            )

            print(
                "Links encontrados nesta página:",
                len(links_pagina)
            )

            todos_links.extend(
                links_pagina
            )

        except requests.RequestException as erro:
            print(
                "Erro ao acessar a página:",
                erro
            )

    # Remove URLs repetidas entre as páginas.
    todos_links = list(
        dict.fromkeys(todos_links)
    )

    print("\n" + "=" * 65)
    print(
        "Total de links únicos encontrados:",
        len(todos_links)
    )
    print("=" * 65)

    if not todos_links:
        print(
            "\nNenhuma vaga foi encontrada. "
            "A coleta será encerrada."
        )
        return

    # --------------------------------------------------------
    # COLETA DOS DADOS DE CADA VAGA
    # --------------------------------------------------------

    dados = []

    for numero, url_vaga in enumerate(
        todos_links,
        start=1
    ):
        print("\n" + "-" * 65)

        print(
            f"Coletando vaga {numero}/"
            f"{len(todos_links)}"
        )

        print(url_vaga)

        try:
            vaga = extrair_dados_vaga(
                url_vaga
            )

            dados.append(
                vaga
            )

            print(
                "Título extraído:",
                vaga["titulo"]
            )

        except Exception as erro:
            print(
                "Erro ao coletar a vaga:",
                erro
            )

            dados.append({
                "fonte": "ProgramaThor",
                "data_coleta": datetime.now().strftime(
                    "%Y-%m-%d"
                ),
                "titulo": None,
                "empresa": None,
                "tamanho_empresa": None,
                "contrato": None,
                "modalidade": None,
                "localizacao": None,
                "salario": None,
                "senioridade": None,
                "skills": None,
                "descricao_empresa": None,
                "atividades": None,
                "requisitos": None,
                "texto_completo": None,
                "url": url_vaga,
                "erro": str(erro),
            })

        time.sleep(
            TEMPO_ENTRE_REQUISICOES
        )

    # --------------------------------------------------------
    # CRIAÇÃO E SALVAMENTO DA TABELA
    # --------------------------------------------------------

    df = pd.DataFrame(
        dados,
        columns=COLUNAS
    )

    CAMINHO_SAIDA.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        CAMINHO_SAIDA,
        index=False,
        encoding="utf-8-sig"
    )

    # --------------------------------------------------------
    # RESUMO FINAL
    # --------------------------------------------------------

    print("\n" + "=" * 65)
    print("COLETA FINALIZADA")
    print("=" * 65)

    print("\nArquivo salvo em:")
    print(CAMINHO_SAIDA)

    print("\nQuantidade de vagas salvas:")
    print(len(df))

    print("\nQuantidade de erros:")
    print(df["erro"].notna().sum())

    print("\nQuantidade de URLs duplicadas:")
    print(df["url"].duplicated().sum())

    colunas_resumo = [
        "titulo",
        "empresa",
        "contrato",
        "modalidade",
        "senioridade",
        "skills",
    ]

    print("\nResumo das vagas coletadas:")

    print(
        df[colunas_resumo]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()