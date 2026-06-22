# Diário de coleta de vagas

## 1. Identificação da coleta

* **Fonte:** ProgramaThor
* **Página de listagem:** `https://www.programathor.com.br/jobs`
* **Data da coleta-piloto:** 22/06/2026
* **Tipo de coleta:** automatizada, utilizando scripts em Python
* **Finalidade:** avaliar a viabilidade da fonte e construir uma amostra inicial de vagas de tecnologia para o desenvolvimento do TCC.

A coleta faz parte da etapa inicial do projeto de Analytics Acadêmico, cujo objetivo é analisar a relação entre as competências exigidas pelo mercado de trabalho, as competências apresentadas pelos egressos e as competências previstas na formação acadêmica do curso de Sistemas de Informação.

---

## 2. Tecnologias utilizadas

A coleta foi realizada em Python com o auxílio das seguintes bibliotecas:

* `requests`: realização das requisições HTTP;
* `BeautifulSoup`: leitura e extração de informações do HTML;
* `lxml`: processamento do conteúdo HTML;
* `pandas`: organização, validação e exportação dos dados;
* `pathlib`: gerenciamento dos caminhos dos arquivos;
* `re`: identificação de padrões nos links;
* `time`: controle do intervalo entre as requisições.

Foi mantido um intervalo de dois segundos entre os acessos às páginas individuais das vagas, com o objetivo de reduzir a frequência de requisições ao servidor.

---

## 3. Teste inicial de acesso

Inicialmente, foi desenvolvido um script simples para testar o acesso à página principal de vagas da ProgramaThor.

### Resultado

* código HTTP retornado: `200`;
* página acessada com sucesso;
* conteúdo HTML recebido normalmente;
* tamanho do HTML: aproximadamente 213 mil caracteres.

O resultado demonstrou que a página poderia ser acessada por meio de uma requisição HTTP realizada pelo script.

### Arquivo utilizado

`src/coleta/01_teste_acesso_programathor.py`

---

## 4. Coleta inicial de 15 vagas

Após o teste de acesso, foi realizada uma primeira coleta utilizando somente a página inicial da listagem.

Foram identificados 15 links únicos de vagas.

### Campos coletados

* fonte;
* data da coleta;
* título;
* empresa;
* tamanho da empresa;
* contrato;
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

### Arquivo utilizado

`src/coleta/02_coletar_amostra_programathor.py`

### Arquivo gerado

`data/samples/programathor_amostra_15_vagas.csv`

A base inicial foi utilizada para testar a estrutura dos campos e verificar se as principais informações dos anúncios poderiam ser extraídas.

---

## 5. Validação estrutural da amostra inicial

A amostra de 15 vagas foi submetida a uma validação estrutural.

Foram verificados:

* quantidade de linhas;
* quantidade de colunas;
* nomes das colunas;
* valores vazios;
* URLs duplicadas;
* presença de salários não especificados;
* tamanho dos textos de atividades;
* tamanho dos textos de requisitos;
* existência de mensagens de erro.

A amostra inicial apresentou 15 registros e 17 colunas, sem URLs duplicadas ou erros de coleta.

---

## 6. Teste de paginação

Em seguida, foi desenvolvido um teste para verificar o funcionamento da paginação da ProgramaThor.

Foram testadas as páginas:

* página 1: `https://www.programathor.com.br/jobs`
* página 2: `https://www.programathor.com.br/jobs?page=2`
* página 3: `https://www.programathor.com.br/jobs?page=3`

### Resultado do teste

| Página    | Links encontrados |
| --------- | ----------------: |
| 1         |                15 |
| 2         |                15 |
| 3         |                15 |
| **Total** |            **45** |

A comparação mostrou:

* zero links repetidos entre as páginas 1 e 2;
* zero links repetidos entre as páginas 1 e 3;
* conteúdo diferente nas três páginas;
* funcionamento do parâmetro `?page=`.

O teste demonstrou que as três primeiras páginas apresentavam conjuntos diferentes de vagas.

### Arquivo utilizado

`src/coleta/03_teste_paginacao_programathor.py`

### Limitação

O teste comprovou o funcionamento das três primeiras páginas, mas ainda não determinou a quantidade total de páginas disponíveis na plataforma.

---

## 7. Coleta ampliada

Após a validação da paginação, foi realizada uma coleta automatizada das três primeiras páginas.

### Resultado

* páginas percorridas: 3;
* links encontrados: 45;
* URLs duplicadas: 0;
* vagas coletadas com sucesso: 42;
* vagas indisponíveis: 3;
* taxa de sucesso: 93,33%.

### Arquivo utilizado

`src/coleta/04_coletar_multiplas_paginas_programathor.py`

### Arquivo gerado

`data/samples/programathor_amostra_45_vagas.csv`

A coleta percorreu cada página da listagem, reuniu os links encontrados, removeu possíveis duplicidades e acessou individualmente cada anúncio.

---

## 8. Falhas encontradas

Três páginas retornaram erro HTTP 500 durante a coleta:

* `https://www.programathor.com.br/jobs/32478-front-end-developer-senior`
* `https://www.programathor.com.br/jobs/31930-engenheiro-a-backend-senior`
* `https://www.programathor.com.br/jobs/31809-desenvolvedor-a-backend-javascript-node-js-jr`

As três URLs também foram testadas manualmente no navegador e permaneceram indisponíveis.

Dessa forma, as falhas foram atribuídas ao servidor da fonte, e não à lógica de extração do código.

As linhas foram preservadas no arquivo de coleta contendo:

* URL;
* data da coleta;
* fonte;
* mensagem de erro.

Os demais campos permaneceram vazios, pois o conteúdo dos anúncios não estava disponível.

Essa decisão evita o descarte silencioso das falhas e mantém a rastreabilidade do processo.

---

## 9. Validação estrutural da base ampliada

A base de 45 URLs foi validada por meio do script:

`src/analise/01_validar_base_programathor.py`

### Resultado

* total de URLs encontradas: 45;
* vagas válidas para análise: 42;
* vagas indisponíveis: 3;
* URLs duplicadas: 0;
* taxa de sucesso: 93,33%;
* campos estruturais vazios nas vagas válidas: 0;
* problemas estruturais identificados: 0;
* salários não especificados: 20;
* percentual de vagas válidas sem salário informado: 47,62%.

O menor texto de requisitos entre as vagas válidas possuía 98 caracteres.

O critério inicial utilizado para identificar textos possivelmente incompletos foi um tamanho inferior a 50 caracteres. Nenhuma vaga válida foi classificada como problemática por esse critério.

### Interpretação da coluna de erro

Nas 42 vagas válidas, a coluna `erro` permaneceu vazia. Isso indica que os anúncios foram processados sem falhas.

Nas três vagas indisponíveis, a coluna `erro` contém a mensagem HTTP retornada pelo servidor.

---

## 10. Seleção da amostra para validação qualitativa

Após a validação estrutural, foi selecionada uma amostra aleatória de oito vagas válidas.

A seleção foi realizada com:

`random_state=42`

Esse parâmetro permite reproduzir a mesma amostra em execuções futuras.

### Campos selecionados para conferência

* título;
* empresa;
* contrato;
* modalidade;
* localização;
* senioridade;
* skills;
* atividades;
* requisitos;
* URL.

Também foram criadas colunas para preenchimento manual com as respostas:

* `sim`;
* `parcial`;
* `não`.

### Arquivo utilizado

`src/analise/02_preparar_validacao_qualitativa.py`

### Arquivo gerado

`data/samples/validacao_qualitativa_8_vagas.csv`

---

## 11. Validação qualitativa

As oito vagas selecionadas foram comparadas manualmente com suas páginas originais.

Na conferência realizada, não foram observadas divergências relevantes nos seguintes campos:

* título;
* empresa;
* contrato;
* modalidade;
* localização;
* senioridade;
* atividades;
* requisitos.

A estrutura geral da extração foi considerada adequada para a continuidade do projeto.

### Observação sobre o campo de skills

A coluna `skills` representa somente as etiquetas de tecnologias apresentadas pela própria ProgramaThor.

Outras competências técnicas e comportamentais podem aparecer nos textos de:

* título;
* atividades;
* requisitos;
* descrição da vaga.

Portanto, a coluna `skills` não deve ser interpretada como uma relação completa de todas as competências exigidas no anúncio.

Nas etapas posteriores, a análise de competências deverá utilizar conjuntamente:

* título;
* skills da plataforma;
* atividades;
* requisitos.

A partir desses campos poderá ser criado um texto destinado à análise e aplicada uma estratégia de extração baseada em dicionários, regras ou mineração de texto.

### Limitação da validação

A validação qualitativa foi realizada sobre uma amostra de oito vagas. Portanto, ela não garante que todos os anúncios da plataforma apresentem exatamente a mesma estrutura.

---

## 12. Arquivos desenvolvidos até o momento

### Scripts de coleta

* `src/coleta/01_teste_acesso_programathor.py`
* `src/coleta/02_coletar_amostra_programathor.py`
* `src/coleta/03_teste_paginacao_programathor.py`
* `src/coleta/04_coletar_multiplas_paginas_programathor.py`

### Scripts de análise

* `src/analise/01_validar_base_programathor.py`
* `src/analise/02_preparar_validacao_qualitativa.py`

### Bases geradas

* `data/samples/programathor_amostra_15_vagas.csv`
* `data/samples/programathor_amostra_45_vagas.csv`
* `data/samples/validacao_qualitativa_8_vagas.csv`

---

## 13. Limitações identificadas

A coleta realizada possui as seguintes limitações:

* foram percorridas somente as três primeiras páginas;
* ainda não foi identificada a última página da listagem;
* foi utilizada apenas uma plataforma;
* a amostra pode refletir características específicas da ProgramaThor;
* os anúncios disponíveis podem mudar ao longo do tempo;
* algumas URLs podem permanecer na listagem mesmo quando a página individual está indisponível;
* a coleta representa um recorte temporal;
* a validação qualitativa foi realizada sobre uma amostra de oito vagas;
* a base ainda é pequena para treinamento de um modelo supervisionado;
* as categorias de classificação ainda não possuem protocolo formal de rotulagem;
* as competências ainda não foram extraídas dos textos.

---

## 14. Decisões metodológicas

Até o momento, foram adotadas as seguintes decisões:

* preservar a base original coletada;
* não preencher artificialmente dados ausentes;
* manter as URLs que apresentaram erro;
* separar vagas válidas de vagas indisponíveis;
* utilizar validação estrutural e qualitativa;
* não considerar a coluna `skills` como lista completa de competências;
* não iniciar Machine Learning antes da criação de uma base rotulada;
* manter um intervalo entre as requisições;
* registrar as decisões, resultados e limitações no diário de coleta.

---

## 15. Próximas etapas

* criar um resumo automatizado da validação qualitativa;
* identificar a última página válida da ProgramaThor;
* verificar duplicidades entre todas as páginas;
* criar uma base processada somente com as vagas válidas;
* renomear ou interpretar o campo `skills` como `skills_plataforma`;
* criar o campo `texto_analise`;
* limpar e padronizar os textos;
* definir as categorias de classificação;
* elaborar um guia de rotulagem manual;
* rotular uma amostra inicial;
* analisar a distribuição das categorias;
* extrair competências técnicas e comportamentais;
* avaliar posteriormente a viabilidade de um modelo simples de classificação.

## 16. Teste de extensão da paginação

Após a validação das três primeiras páginas, foi desenvolvido um novo script com o objetivo de verificar até onde a paginação da ProgramaThor continuava apresentando vagas diferentes.

O teste percorreu páginas sucessivas, comparando os links encontrados em cada página com os links já identificados anteriormente.

### Arquivo utilizado

`src/coleta/05_descobrir_ultima_pagina_programathor.py`

### Critérios de parada

O script foi configurado para interromper a execução quando ocorresse uma das seguintes situações:

* página sem links de vagas;
* página contendo somente links já identificados;
* erro de acesso;
* alcance do limite máximo de 50 páginas.

O limite de 50 páginas foi utilizado como medida de segurança para evitar uma execução excessivamente longa.

### Resultado do teste

* páginas testadas: 50;
* última página testada com vagas novas: 50;
* URLs únicas encontradas: 748;
* página sem vagas encontrada: não;
* página totalmente repetida encontrada: não;
* última página real da plataforma identificada: não.

A página 50 ainda apresentou links de vagas que não haviam aparecido nas páginas anteriores. Portanto, o teste não identificou o final real da paginação.

O resultado permite afirmar que, no momento da execução, a plataforma possuía pelo menos 50 páginas de anúncios acessíveis e pelo menos 748 URLs únicas de vagas.

Não é correto afirmar que a ProgramaThor possuía exatamente 50 páginas, pois a execução foi encerrada pelo limite de segurança configurado no script, e não pela ausência de novas vagas.

### Diferença entre o total esperado e o encontrado

Caso todas as 50 páginas apresentassem exatamente 15 vagas diferentes, o total teórico seria de 750 URLs.

Entretanto, foram encontradas 748 URLs únicas. Essa diferença pode estar relacionada a:

* repetição de algum anúncio entre páginas;
* página com menos de 15 vagas;
* alteração da listagem durante a execução;
* movimentação ou remoção de anúncios enquanto o teste era realizado.

Como o script utiliza um conjunto de URLs únicas, possíveis repetições são eliminadas automaticamente.

### Decisão de escopo

Apesar de terem sido identificadas 748 URLs únicas nas primeiras 50 páginas, decidiu-se não coletar imediatamente todos os anúncios.

A coleta completa aumentaria significativamente:

* o tempo de execução;
* a quantidade de requisições;
* o volume de falhas a serem verificadas;
* o trabalho de validação;
* o esforço necessário para rotulagem manual;
* o risco de desequilíbrio entre as categorias.

Como próxima etapa, será realizada uma coleta ampliada e controlada de aproximadamente 20 páginas, com potencial de gerar até cerca de 300 URLs.

Esse volume será utilizado para avaliar:

* qualidade da coleta em escala maior;
* quantidade de registros indisponíveis;
* ocorrência de duplicidades;
* distribuição das vagas por área;
* diversidade das categorias propostas;
* necessidade de inclusão de uma segunda fonte;
* viabilidade de uma futura classificação supervisionada.

### Limitação temporal

A quantidade de páginas e anúncios pode mudar ao longo do tempo, pois novas vagas podem ser publicadas e anúncios antigos podem ser removidos.

Dessa forma, o resultado de 748 URLs representa um recorte da plataforma na data de execução do teste.
