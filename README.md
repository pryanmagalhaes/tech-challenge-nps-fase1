# NPS Preditivo · Tech Challenge Fase 1

> **O cliente aceita esperar. Não aceita ser surpreendido.**
> Diagnóstico dos fatores operacionais que explicam a satisfação dos clientes de um e-commerce e de onde agir **antes** da pesquisa de NPS.

---

## Resultado em 30 segundos

| | |
|---|---|
| **NPS atual** | **−80** (84% detratores, 11% neutros, 4% promotores) |
| **Fator nº 1** | **Atraso na entrega**: cada dia além do prometido tira ~1 ponto da nota (0 a 10) |
| **Achado-chave** | O **prazo total** de entrega **não** altera a nota; o **atraso**, sim |
| **Ponto de ruptura** | 1º dia de atraso = metade da queda (NPS −34 → −67); com 3+ dias, 98% são detratores e não há promotores |
| **2º amplificador** | Atendimento: a 2ª reclamação é a virada; com 3+ contatos, 95% são detratores |
| **Perfil do cliente** | Região, idade, tempo de casa e valor do pedido **não** diferenciam a nota |
| **Sinais antecedentes** | Atraso ≥ 2 dias **ou** ≥ 4 reclamações cobrem **90% dos detratores** |

---

## Objetivo do projeto

A empresa cresceu e passou a ter alta variabilidade de NPS entre clientes com operações aparentemente parecidas. Como o NPS só é coletado no fim da jornada, a gestão é reativa. Este projeto:

1. Enquadra o problema de negócio e o papel do NPS no e-commerce;
2. Define e discute a variável-alvo e seus riscos;
3. Identifica, com foco em negócio, **quais fatores operacionais explicam a satisfação**, onde está o **ponto de ruptura** e **quem** tende a dar notas altas ou baixas;
4. Traduz os achados em **recomendações priorizadas**, com limitações explícitas, para um público não técnico.

> O desafio opcional (item 4, modelo preditivo) **não** faz parte desta entrega, por decisão de escopo. A pasta `models/` documenta os insumos já preparados para a próxima fase.

---

## Onde está cada entrega

| Requisito do desafio | Onde encontrar |
|---|---|
| **1. Entendimento do negócio** (problema, importância do NPS, áreas beneficiadas, recompra, boca a boca, market share, indicadores de mercado) | [`docs/01_entendimento_do_negocio.md`](docs/01_entendimento_do_negocio.md) |
| **2. Definição da target** (variável, justificativa, momento de coleta, riscos) | [`docs/02_definicao_da_target.md`](docs/02_definicao_da_target.md) |
| **Tratamento e preparação da base** | [`notebooks/01_qualidade_e_tratamento_dos_dados.ipynb`](notebooks/01_qualidade_e_tratamento_dos_dados.ipynb) + [`src/data_prep.py`](src/data_prep.py) |
| **3. Análise exploratória (EDA)** com foco em negócio | [`notebooks/02_analise_exploratoria_eda.ipynb`](notebooks/02_analise_exploratoria_eda.ipynb) |
| Relatório executivo (EDA explicada para gestor) | [`reports/relatorio_executivo.md`](reports/relatorio_executivo.md) |
| **Apresentação de storytelling** (slides, público não técnico) | [`presentation/apresentacao_nps.html`](presentation/apresentacao_nps.html) |
| Dicionário de dados com notas de qualidade | [`docs/dicionario_de_dados.md`](docs/dicionario_de_dados.md) |

---

## Estrutura do repositório

```
tech-challenge-nps-fase1/
├── README.md                          ← você está aqui
├── requirements.txt                   ← dependências
├── Makefile                           ← reprodução com um comando
├── data/
│   ├── raw/desafio_nps_fase_1.csv     ← base original (não alterada)
│   └── processed/nps_tratado.csv      ← base analítica (gerada pelo notebook 01)
├── docs/
│   ├── 01_entendimento_do_negocio.md  ← requisito 1
│   ├── 02_definicao_da_target.md      ← requisito 2
│   └── dicionario_de_dados.md
├── notebooks/
│   ├── 01_qualidade_e_tratamento_dos_dados.ipynb
│   └── 02_analise_exploratoria_eda.ipynb   ← requisito 3
├── src/                               ← código reutilizável (fonte única das regras)
│   ├── config.py                      ← caminhos, regra do NPS, grupos de variáveis, paleta
│   ├── data_prep.py                   ← validação, flags de qualidade, variáveis de negócio
│   ├── metrics.py                     ← NPS, classificação e intervalo de confiança (bootstrap)
│   └── viz.py                         ← padrão visual dos gráficos
├── reports/
│   ├── relatorio_executivo.md
│   ├── figures/                       ← 12 gráficos exportados pela EDA
│   ├── key_metrics.json               ← números-chave (fonte para relatório e slides)
│   └── data_quality_report.csv
├── presentation/
│   ├── apresentacao_nps.html          ← 16 slides, abre em qualquer navegador
│   ├── build_presentation.py          ← gera o HTML a partir dos dados
│   └── roteiro_apresentacao_e_video.md
└── models/                            ← reservado para a próxima fase
```

---

## Descrição da base

- **Arquivo:** `data/raw/desafio_nps_fase_1.csv`
- **Volume:** 2.500 linhas × 19 colunas · sem nulos · sem duplicados
- **Granularidade:** 1 linha = 1 cliente = 1 pedido = 1 resposta de NPS
- **Grupos de variáveis:**

| Grupo | Variáveis |
|---|---|
| Cliente | idade, região, tempo de relacionamento |
| Pedido | valor, itens, desconto, parcelas |
| Logística | prazo total, dias de atraso, frete, tentativas de entrega |
| Atendimento | contatos, tempo de resolução, reclamações |
| Alvo | `nps_score` (0 a 10) |
| Pós-pesquisa (não usadas como fator) | `repeat_purchase_30d`, `csat_internal_score` |

Detalhes, faixas e observações de qualidade em [`docs/dicionario_de_dados.md`](docs/dicionario_de_dados.md).

---

## Metodologia

**1. Enquadramento de negócio.** Problema, hipóteses e pergunta orientadora definidos antes de olhar os dados.

**2. Qualidade e tratamento** (notebook 01)
- Validação de esquema, faixas plausíveis, nulos e duplicados;
- **Regras de consistência de negócio** (ex.: atraso maior que o prazo total, desconto maior que o pedido), com decisão documentada para cada uma;
- Política **“sinalizar, não apagar”**: flags `dq_*` e **teste de robustez** comparando os achados com e sem registros suspeitos (os quatro principais fatores não mudam);
- **Teste de sensibilidade** da classificação do NPS (notas decimais: corte contínuo vs. arredondamento; NPS de −80 vs. −74, mesmo diagnóstico);
- Identificação de **vazamento de informação**: recompra e CSAT são consequência da satisfação e ficam fora da explicação.

**3. EDA orientada a perguntas de negócio** (notebook 02)
- **Ranking de fatores** pela correlação de Spearman (robusta a não linearidade) e **peso exclusivo** de cada fator (queda no R² ao retirá-lo de uma regressão linear explicativa, padronizada);
- **Pontos de ruptura** por faixas operacionais, com **NPS e intervalo de confiança de 95% por bootstrap**;
- **Interação** atraso × reclamações;
- **Perfil de cliente** com teste de Kruskal-Wallis;
- **Composição dos detratores** por gatilho operacional;
- **Cenários de ordem de grandeza** (reponderação pelo comportamento de pedidos semelhantes).

**4. Comunicação.** Relatório executivo, slides e roteiro com linguagem de negócio, recomendações com dono e indicador, e limitações explícitas.

### Decisões de projeto relevantes

| Decisão | Justificativa |
|---|---|
| Promotor ≥ 9, Neutro 7 a < 9, Detrator < 7 (cortes contínuos) | A base traz notas decimais; o corte contínuo não descarta informação e o resultado é equivalente ao arredondamento |
| Não remover registros inconsistentes | Sem confirmação do dono do dado, remover enviesa; o teste de robustez mostra que os achados não dependem deles |
| Spearman em vez de Pearson | Variáveis discretas e relações potencialmente não lineares |
| Regressão linear apenas **explicativa** | Separar efeitos de fatores que ocorrem juntos; não é um modelo preditivo e não foi avaliado como tal |
| Bootstrap para o NPS | O NPS é uma diferença de proporções; o bootstrap dá intervalos sem suposições de distribuição |

---

## Como reproduzir

**Pré-requisitos:** Python 3.10 ou superior.

```bash
# 1. Clonar e entrar no repositório
git clone <url-do-repositorio>
cd tech-challenge-nps-fase1

# 2. (Recomendado) criar ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar tudo: tratamento -> EDA -> apresentação
make all
```

Sem `make` (ex.: Windows):

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_qualidade_e_tratamento_dos_dados.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_analise_exploratoria_eda.ipynb
python presentation/build_presentation.py
```

Ou abra os notebooks no Jupyter / VS Code e execute **na ordem (01 → 02)**. O notebook 01 gera `data/processed/nps_tratado.csv`, que é a entrada do notebook 02.

**Saídas geradas:** base tratada, relatório de qualidade, 12 figuras em `reports/figures/`, `reports/key_metrics.json` e `presentation/apresentacao_nps.html`.

**Apresentação:** abra `presentation/apresentacao_nps.html` em qualquer navegador. Use ← → (ou clique / deslize) para navegar e **F** para tela cheia. Para exportar em PDF, use *Imprimir → Salvar como PDF* (cada slide vira uma página).

---

## Principais limitações

1. **Associação não é causalidade**: recomendações devem ser validadas com pilotos e grupo de controle.
2. **Sinais de base simulada**: recompra determinística (0% abaixo de nota 8, 100% acima) e notas decimais. Usar a **direção** dos achados; recalibrar magnitudes com dados reais.
3. **Ausência de data do pedido, prazo prometido, transportadora e categoria**: impede análise de sazonalidade e da origem do atraso.
4. **44% da variação da nota não é explicada** pelos fatores disponíveis (produto, preço e comunicação não estão na base).
5. **Inconsistências de cadastro** (ex.: 4,8% com atraso maior que o prazo total), sinalizadas e testadas.

Detalhes no [relatório executivo](reports/relatorio_executivo.md#7-limitações-e-cuidados) e no notebook 01.

---

## Stack

Python · pandas · NumPy · SciPy · scikit-learn · Matplotlib · seaborn · Jupyter
