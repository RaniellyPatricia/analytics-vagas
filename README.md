# TCC — Analytics Acadêmico com Vagas, Egressos e Aderência Curricular

Projeto de Trabalho de Conclusão de Curso voltado ao desenvolvimento de uma solução de Analytics Acadêmico para apoiar a coordenação do curso de Sistemas de Informação.

A proposta geral é analisar a relação entre:

* competências exigidas pelo mercado de trabalho;
* trajetória profissional dos egressos;
* competências previstas no Projeto Pedagógico do Curso e na matriz curricular.

O projeto está sendo desenvolvido em etapas. A fase atual concentra-se na coleta, organização e análise de anúncios de vagas de tecnologia publicados no Brasil.

---

## Objetivo do projeto

Desenvolver um estudo aplicado que permita comparar as demandas do mercado de trabalho com a formação acadêmica e a trajetória profissional dos egressos, gerando indicadores que possam apoiar decisões da coordenação do curso.

Entre os resultados esperados estão:

* base estruturada de vagas de tecnologia;
* análise exploratória dos anúncios;
* classificação das vagas por área de atuação;
* extração de competências técnicas;
* análise de dados públicos de egressos;
* análise das competências previstas no currículo;
* comparação entre mercado, formação e trajetória profissional;
* dashboard em Power BI.

---

## Escopo atual

A primeira etapa prática está focada na análise de vagas de tecnologia.

As atividades previstas nesta fase são:

1. testar fontes de vagas;
2. coletar anúncios com descrição completa;
3. estruturar e validar os dados;
4. limpar e preparar os textos;
5. definir categorias de classificação;
6. criar uma estratégia de rotulagem manual;
7. testar métodos simples de classificação;
8. avaliar métricas;
9. extrair competências dos anúncios.

O uso de Machine Learning será realizado somente após a construção de uma base rotulada com quantidade e qualidade suficientes para uma avaliação minimamente defensável.

---

## Fonte de dados testada

A primeira fonte utilizada foi a plataforma ProgramaThor:

`https://www.programathor.com.br/jobs`

A coleta foi realizada por meio de scripts em Python, utilizando requisições HTTP e extração de informações do HTML.

Até o momento, foram testadas as três primeiras páginas da listagem. Ainda não foi determinada a quantidade total de páginas disponíveis na plataforma.

---

## Resultados da coleta-piloto

A coleta ampliada das três primeiras páginas apresentou os seguintes resultados:

| Indicador                        | Resultado |
| -------------------------------- | --------: |
| Páginas analisadas               |         3 |
| URLs encontradas                 |        45 |
| Vagas coletadas com sucesso      |        42 |
| Vagas indisponíveis              |         3 |
| URLs duplicadas                  |         0 |
| Taxa de sucesso                  |    93,33% |
| Salários não especificados       |        20 |
| Percentual sem salário divulgado |    47,62% |

As três vagas indisponíveis retornaram erro HTTP 500. As URLs também foram testadas manualmente no navegador e permaneceram inacessíveis, indicando falha na própria fonte.

Os resultados representam apenas a amostra coletada e não devem ser generalizados para todo o mercado de trabalho brasileiro.

---

## Campos coletados

Cada anúncio pode conter os seguintes campos:

* fonte;
* data da coleta;
* título da vaga;
* empresa;
* tamanho da empresa;
* tipo de contrato;
* modalidade;
* localização;
* salário;
* senioridade;
* skills;
* descrição da empresa;
* atividades e responsabilidades;
* requisitos;
* texto completo;
* URL;
* mensagem de erro.

---

## Estrutura do projeto

```text
TCC-analytics-vagas/
├── data/
│   ├── processed/
│   ├── raw/
│   └── samples/
│       ├── programathor_amostra_15_vagas.csv
│       └── programathor_amostra_45_vagas.csv
├── docs/
│   └── diario_coleta.md
├── notebooks/
├── outputs/
│   ├── graficos/
│   └── tabelas/
├── src/
│   ├── analise/
│   │   └── 01_validar_base_programathor.py
│   ├── coleta/
│   │   ├── 01_teste_acesso_programathor.py
│   │   ├── 02_coletar_amostra_programathor.py
│   │   ├── 03_teste_paginacao_programathor.py
│   │   └── 04_coletar_multiplas_paginas_programathor.py
│   └── limpeza/
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Descrição dos scripts

### `01_teste_acesso_programathor.py`

Testa o acesso à página principal de vagas e apresenta:

* código de resposta HTTP;
* tamanho do conteúdo HTML recebido.

### `02_coletar_amostra_programathor.py`

Coleta uma amostra inicial de 15 vagas presentes na primeira página da plataforma.

### `03_teste_paginacao_programathor.py`

Testa as páginas 1, 2 e 3 da listagem e verifica:

* quantidade de links encontrados;
* diferença entre as páginas;
* ocorrência de URLs repetidas.

### `04_coletar_multiplas_paginas_programathor.py`

Percorre as três primeiras páginas, reúne os links únicos e coleta os dados individuais das vagas.

O script mantém um intervalo entre as requisições para reduzir a frequência de acessos ao servidor.

### `01_validar_base_programathor.py`

Realiza a validação estrutural da base coletada, verificando:

* quantidade de registros;
* valores vazios;
* URLs duplicadas;
* vagas indisponíveis;
* tamanho dos textos;
* salários não especificados;
* taxa de sucesso da coleta.

---

## Preparação do ambiente

### 1. Criar o ambiente virtual

No PowerShell:

```powershell
python -m venv venv
```

### 2. Ativar o ambiente virtual

```powershell
.\venv\Scripts\Activate.ps1
```

Quando estiver ativo, o terminal deverá apresentar:

```text
(venv)
```

### 3. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

---

## Execução dos scripts

Os comandos devem ser executados a partir da pasta principal do projeto.

### Testar o acesso

```powershell
python src/coleta/01_teste_acesso_programathor.py
```

### Coletar a amostra inicial

```powershell
python src/coleta/02_coletar_amostra_programathor.py
```

### Testar a paginação

```powershell
python src/coleta/03_teste_paginacao_programathor.py
```

### Coletar múltiplas páginas

```powershell
python src/coleta/04_coletar_multiplas_paginas_programathor.py
```

### Validar a base coletada

```powershell
python src/analise/01_validar_base_programathor.py
```

Os anúncios disponíveis na plataforma podem mudar ao longo do tempo. Por isso, uma nova execução pode produzir resultados diferentes da amostra armazenada no projeto.

---

## Tecnologias utilizadas

* Python;
* pandas;
* requests;
* Beautiful Soup;
* lxml;
* Git;
* GitHub;
* Visual Studio Code.

Outras tecnologias poderão ser incorporadas nas etapas posteriores, como:

* scikit-learn;
* TF-IDF;
* Power BI;
* técnicas de mineração de texto.

---

## Categorias iniciais de classificação

As categorias preliminares consideradas para as vagas são:

* Desenvolvimento;
* Dados, BI e Analytics;
* Sistemas, Negócios e Produto;
* Infraestrutura, Cloud e DevOps;
* QA e Testes;
* Segurança da Informação;
* Suporte Técnico;
* Outros ou Indefinido.

Essas categorias ainda deverão ser avaliadas e transformadas em um guia de rotulagem com critérios claros, exemplos e regras para casos ambíguos.

---

## Limitações atuais

A etapa atual possui as seguintes limitações:

* coleta restrita às três primeiras páginas;
* utilização de uma única plataforma;
* amostra pequena para treinamento de Machine Learning;
* possibilidade de alteração ou remoção dos anúncios;
* existência de páginas listadas, mas indisponíveis;
* viés relacionado ao perfil de vagas divulgado pela ProgramaThor;
* validação estrutural concluída, mas validação semântica ainda pendente;
* ausência, até o momento, de uma base rotulada manualmente.

---

## Cuidados metodológicos

Os resultados devem ser interpretados como um recorte da fonte e do período de coleta.

A coleta deve respeitar os limites técnicos da plataforma, evitar excesso de requisições e registrar falhas, datas e decisões tomadas durante o processo.

Dados pessoais desnecessários não devem ser coletados. Nas etapas envolvendo egressos, deverão ser considerados os princípios éticos, a LGPD, a finalidade acadêmica e a utilização responsável de informações públicas.

---

## Próximas etapas

* atualizar e manter o diário de coleta;
* identificar a última página válida da plataforma;
* realizar validação qualitativa das vagas;
* separar a base bruta da base processada;
* criar o campo textual destinado à análise;
* definir o protocolo de rotulagem manual;
* analisar a distribuição das categorias;
* extrair competências técnicas;
* avaliar a viabilidade de um modelo simples de classificação;
* posteriormente integrar dados de egressos e do currículo.
