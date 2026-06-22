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

LIMITE_VAGAS = 15
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
    / "programathor_amostra_15_vagas.csv"
)


# Colunas que serão salvas no CSV.
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
    Padroniza um texto para facilitar comparações.

    Exemplo:
    'Localização' -> 'localizacao'
    """

    if texto is None:
        return ""

    texto = str(texto).strip().lower()

    texto = unicodedata.normalize("NFD", texto)

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

    texto = soup.get_text("\n", strip=True)

    linhas = texto.split("\n")

    linhas_limpas = []

    for linha in linhas:
        linha = linha.strip()

        if linha:
            linhas_limpas.append(linha)

    return linhas_limpas


def encontrar_indice(linhas, texto_procurado, inicio=0):
    """
    Procura uma linha que seja exatamente igual ao texto informado.
    """

    texto_normalizado = normalizar(texto_procurado)

    for indice in range(inicio, len(linhas)):
        if normalizar(linhas[indice]) == texto_normalizado:
            return indice

    return None


def encontrar_linha_que_comeca_com(linhas, prefixo, inicio=0):
    """
    Procura uma linha que comece com determinado texto.

    Exemplo:
    prefixo = 'Salário:'
    """

    prefixo_normalizado = normalizar(prefixo)

    for indice in range(inicio, len(linhas)):
        linha_normalizada = normalizar(linhas[indice])

        if linha_normalizada.startswith(prefixo_normalizado):
            return indice

    return None


# ============================================================
# EXTRAÇÃO DOS LINKS
# ============================================================

def extrair_links_vagas(html):
    """
    Encontra os links individuais das vagas na página de listagem.
    """

    soup = BeautifulSoup(html, "lxml")

    links_html = soup.find_all("a", href=True)

    links_vagas = []

    for link in links_html:
        href = link["href"]

        # Procura URLs com padrões como:
        # /jobs/33592-analista-de-dados
        if re.search(r"/jobs/\d+", href):
            url_completa = urljoin(BASE_URL, href)

            # Remove parâmetros existentes depois de "?".
            url_completa = url_completa.split("?")[0]

            links_vagas.append(url_completa)

    # Remove links duplicados mantendo a ordem original.
    links_vagas = list(dict.fromkeys(links_vagas))

    return links_vagas


# ============================================================
# EXTRAÇÃO DE SEÇÕES TEXTUAIS
# ============================================================

def extrair_secao(
    linhas,
    nome_secao,
    secoes_de_parada,
    inicio_busca=0
):
    """
    Extrai o conteúdo localizado entre uma seção e a próxima seção.

    Exemplo:
    Atividades e Responsabilidades
        conteúdo desejado
    Requisitos
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

    conteudo = linhas[inicio_conteudo:fim_conteudo]

    texto_secao = " ".join(conteudo).strip()

    if texto_secao:
        return texto_secao

    return None


# ============================================================
# EXTRAÇÃO DE UMA VAGA INDIVIDUAL
# ============================================================

def extrair_dados_vaga(url_vaga):
    """
    Acessa uma vaga individual e extrai os principais campos.
    """

    html = baixar_html(url_vaga)

    soup = BeautifulSoup(html, "lxml")

    linhas = preparar_linhas(soup)

    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    titulo_tag = soup.find("h1")

    if titulo_tag:
        titulo = titulo_tag.get_text(strip=True)
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

        for indice in range(0, indice_inicio):
            if normalizar(linhas[indice]) == normalizar(titulo):
                indice_titulo_antes_inicio = indice

        if indice_titulo_antes_inicio is not None:
            skills = linhas[
                indice_titulo_antes_inicio + 1:
                indice_inicio
            ]

    # --------------------------------------------------------
    # LOCALIZA O TÍTULO PRINCIPAL DA VAGA
    # --------------------------------------------------------

    indice_titulo_principal = None

    if titulo and indice_inicio is not None:
        for indice in range(indice_inicio, len(linhas)):
            if normalizar(linhas[indice]) == normalizar(titulo):
                indice_titulo_principal = indice
                break

    if indice_titulo_principal is not None:
        inicio_busca = indice_titulo_principal
    else:
        inicio_busca = 0

    # Limita a busca dos metadados até o começo da descrição.
    indice_descricao = encontrar_indice(
        linhas,
        "Descrição da empresa",
        inicio_busca
    )

    if indice_descricao is None:
        fim_metadados = len(linhas)
    else:
        fim_metadados = indice_descricao

    linhas_metadados = linhas[inicio_busca:fim_metadados]

    # --------------------------------------------------------
    # EMPRESA
    # --------------------------------------------------------

    empresa = None

    if indice_titulo_principal is not None:
        proximo_indice = indice_titulo_principal + 1

        if proximo_indice < len(linhas):
            empresa = linhas[proximo_indice]

            # Algumas vagas externas mostram primeiro
            # "VAGA EXTERNA" e só depois o nome da empresa.
            if normalizar(empresa) == "vaga externa":
                segundo_indice = proximo_indice + 1

                if segundo_indice < len(linhas):
                    empresa = linhas[segundo_indice]

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
        linha_normalizada = normalizar(linha)

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
        proximo_indice = indice_localizacao + 1

        if proximo_indice < len(linhas):
            localizacao = linhas[proximo_indice]

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

    # --------------------------------------------------------
    # MONTA O REGISTRO DA VAGA
    # --------------------------------------------------------

    vaga = {
        "fonte": "ProgramaThor",
        "data_coleta": datetime.now().strftime("%Y-%m-%d"),
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
    print("=" * 60)
    print("COLETA DE VAGAS DA PROGRAMATHOR")
    print("=" * 60)

    print("\nAcessando a página de listagem:")
    print(LIST_URL)

    try:
        html_listagem = baixar_html(LIST_URL)

    except requests.RequestException as erro:
        print("\nNão foi possível acessar a página de vagas.")
        print("Erro:", erro)
        return

    links_vagas = extrair_links_vagas(html_listagem)

    print(
        "\nTotal de links de vagas encontrados:",
        len(links_vagas)
    )

    links_amostra = links_vagas[:LIMITE_VAGAS]

    print(
        "Quantidade de vagas que serão coletadas:",
        len(links_amostra)
    )

    dados = []

    for numero, url_vaga in enumerate(
        links_amostra,
        start=1
    ):
        print("\n" + "-" * 60)

        print(
            f"Coletando vaga {numero}/"
            f"{len(links_amostra)}"
        )

        print(url_vaga)

        try:
            vaga = extrair_dados_vaga(url_vaga)

            dados.append(vaga)

            print(
                "Título extraído:",
                vaga["titulo"]
            )

        except Exception as erro:
            print("Erro ao coletar a vaga:", erro)

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

        # Pausa para não fazer muitas requisições seguidas.
        time.sleep(TEMPO_ENTRE_REQUISICOES)

    # Cria a tabela.
    df = pd.DataFrame(
        dados,
        columns=COLUNAS
    )

    # Cria a pasta de saída, caso ela ainda não exista.
    CAMINHO_SAIDA.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Salva o CSV.
    df.to_csv(
        CAMINHO_SAIDA,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n" + "=" * 60)
    print("COLETA FINALIZADA")
    print("=" * 60)

    print("\nArquivo salvo em:")
    print(CAMINHO_SAIDA)

    print("\nQuantidade de vagas salvas:")
    print(len(df))

    print("\nQuantidade de erros:")
    print(df["erro"].notna().sum())

    colunas_resumo = [
        "titulo",
        "empresa",
        "contrato",
        "modalidade",
        "senioridade",
        "skills",
    ]

    print("\nResumo das vagas coletadas:")
    print(df[colunas_resumo].to_string(index=False))


if __name__ == "__main__":
    main()