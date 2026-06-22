# Diário de coleta de vagas

## 1. Identificação da coleta

* **Fonte:** ProgramaThor
* **Endereço da listagem:** `https://www.programathor.com.br/jobs`
* **Data da coleta:** 22/06/2026
* **Tipo de coleta:** automatizada, por meio de scripts em Python
* **Finalidade:** testar a viabilidade da fonte e construir uma amostra inicial de vagas de tecnologia para o TCC.

---

## 2. Tecnologias utilizadas

A coleta foi realizada em Python, utilizando principalmente as seguintes bibliotecas:

* `requests`: realização das requisições HTTP;
* `BeautifulSoup`: leitura e extração de informações do HTML;
* `lxml`: processamento do HTML;
* `pandas`: estruturação e exportação dos dados;
* `pathlib`: gerenciamento dos caminhos dos arquivos.

Foi utilizado um intervalo de dois segundos entre as requisições das páginas individuais das vagas, com o objetivo de reduzir a frequência de acessos ao site.

---

## 3. Teste inicial de acesso

Foi realizado um primeiro teste de acesso à página de vagas da ProgramaThor.

Resultado obtido:

* código HTTP retornado: `200`;
* página acessada com sucesso;
* conteúdo HTML recebido normalmente.

Esse resultado indicou que a página poderia ser acessada por meio do script de coleta.

Arquivo utilizado:

`src/coleta/01_teste_acesso_programathor.py`

---

## 4. Coleta inicial de 15 vagas

Na primeira coleta, foram extraídos os links presentes na primeira página da listagem.

Foram coletadas 15 vagas, com os seguintes campos:

* fonte;
* data da coleta;
* título;
* empresa;
* tamanho da empresa;
* tipo de contrato;
* modalidade;
* localização;
* salário;
* senioridade;
* skills;
* descrição da empresa;
* atividades;
* requisitos;
* texto completo;
* URL;
* mensagem de erro.

Arquivo utilizado:

`src/coleta/02_coletar_amostra_programathor.py`

Arquivo gerado:

`data/samples/programathor_amostra_15_vagas.csv`

---

## 5. Teste de paginação

Foi realizado um teste nas páginas 1, 2 e 3 da listagem.

Resultados:

| Página    | Quantidade de links |
| --------- | ------------------: |
| 1         |                  15 |
| 2         |                  15 |
| 3         |                  15 |
| **Total** |              **45** |

A comparação entre as páginas apresentou:

* nenhum link repetido entre as páginas 1 e 2;
* nenhum link repetido entre as páginas 1 e 3;
* conteúdos diferentes nas três páginas.

O teste demonstrou que o parâmetro `?page=` permite acessar páginas distintas da listagem.

Arquivo utilizado:

`src/coleta/03_teste_paginacao_programathor.py`

### Observação

O teste confirmou o funcionamento das três primeiras páginas, mas ainda não determinou a quantidade total de páginas disponíveis na plataforma.

---

## 6. Coleta ampliada

Após a validação da paginação, foi realizada uma coleta das três primeiras páginas da ProgramaThor.

Resultados:

* páginas percorridas: 3;
* links encontrados: 45;
* URLs duplicadas: 0;
* vagas coletadas com sucesso: 42;
* vagas indisponíveis: 3;
* taxa de sucesso: 93,33%.

Arquivo utilizado:

`src/coleta/04_coletar_multiplas_paginas_programathor.py`

Arquivo gerado:

`data/samples/programathor_amostra_45_vagas.csv`

---

## 7. Falhas encontradas

Três URLs retornaram erro HTTP 500:

* `https://www.programathor.com.br/jobs/32478-front-end-developer-senior`
* `https://www.programathor.com.br/jobs/31930-engenheiro-a-backend-senior`
* `https://www.programathor.com.br/jobs/31809-desenvolvedor-a-backend-javascript-node-js-jr`

As páginas também foram testadas manualmente no navegador e permaneceram indisponíveis.

Dessa forma, as falhas foram atribuídas à própria fonte, e não à lógica de extração do script.

As linhas foram mantidas no arquivo com a URL e a mensagem de erro, evitando o descarte silencioso das ocorrências.

---

## 8. Validação estrutural

A base ampliada foi validada por meio do script:

`src/analise/01_validar_base_programathor.py`

Resultados da validação:

* total de URLs: 45;
* vagas válidas: 42;
* vagas indisponíveis: 3;
* URLs duplicadas: 0;
* problemas estruturais nas vagas válidas: nenhum;
* campos obrigatórios vazios nas vagas válidas: nenhum;
* salários não especificados: 20;
* percentual de salários não especificados: 47,62%.

Os textos de requisitos das vagas válidas possuíam pelo menos 98 caracteres, não sendo identificados textos excessivamente curtos pelo critério inicial adotado.

---

## 9. Limitações identificadas

A coleta realizada possui as seguintes limitações:

* foram analisadas somente as três primeiras páginas;
* ainda não foi determinada a quantidade total de páginas;
* a plataforma pode alterar ou remover anúncios ao longo do tempo;
* algumas páginas podem permanecer listadas mesmo estando indisponíveis;
* a amostra representa apenas uma plataforma de vagas;
* a distribuição das áreas pode refletir o perfil específico da ProgramaThor;
* a validação realizada até o momento foi estrutural, e não semântica;
* o resultado representa um recorte temporal da plataforma na data da coleta.

---

## 10. Próximas atividades

* verificar até qual página a paginação permanece válida;
* identificar a última página da listagem;
* verificar repetições entre todas as páginas;
* realizar validação qualitativa de uma amostra das vagas;
* comparar os campos extraídos com os anúncios originais;
* preparar uma base processada apenas com vagas válidas;
* criar o campo textual destinado à análise;
* definir critérios e categorias para rotulagem manual;
* avaliar a distribuição das vagas por área antes de aplicar Machine Learning.
