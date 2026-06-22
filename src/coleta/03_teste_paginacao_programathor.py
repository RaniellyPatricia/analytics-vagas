import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.programathor.com.br"
LIST_URL = "https://www.programathor.com.br/jobs"

PAGINAS_PARA_TESTAR = [1, 2, 3]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}


def baixar_html(url):
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return response.text


def extrair_links_vagas(html):
    soup = BeautifulSoup(html, "lxml")

    links_html = soup.find_all("a", href=True)

    links_vagas = []

    for link in links_html:
        href = link["href"]

        if re.search(r"/jobs/\d+", href):
            url_completa = urljoin(BASE_URL, href)
            url_completa = url_completa.split("?")[0]

            links_vagas.append(url_completa)

    links_vagas = list(dict.fromkeys(links_vagas))

    return links_vagas


def main():
    links_por_pagina = {}

    for pagina in PAGINAS_PARA_TESTAR:

        if pagina == 1:
            url_pagina = LIST_URL
        else:
            url_pagina = f"{LIST_URL}?page={pagina}"

        print("\n" + "=" * 60)
        print("Testando página:", pagina)
        print("URL:", url_pagina)

        try:
            html = baixar_html(url_pagina)

            links_vagas = extrair_links_vagas(html)

            links_por_pagina[pagina] = links_vagas

            print(
                "Quantidade de vagas encontradas:",
                len(links_vagas)
            )

            print("Primeiros três links:")

            for link in links_vagas[:3]:
                print("-", link)

        except requests.RequestException as erro:
            print("Erro ao acessar a página:")
            print(erro)

            links_por_pagina[pagina] = []

    links_pagina_1 = set(
        links_por_pagina.get(1, [])
    )

    for pagina in [2, 3]:
        links_pagina_atual = set(
            links_por_pagina.get(pagina, [])
        )

        quantidade_repetidos = len(
            links_pagina_1.intersection(
                links_pagina_atual
            )
        )

        paginas_iguais = (
            links_pagina_1 == links_pagina_atual
        )

        print("\n" + "-" * 60)
        print(
            f"Comparação entre página 1 e página {pagina}:"
        )
        print(
            "Links repetidos:",
            quantidade_repetidos
        )
        print(
            "As páginas possuem as mesmas vagas?",
            paginas_iguais
        )


if __name__ == "__main__":
    main()