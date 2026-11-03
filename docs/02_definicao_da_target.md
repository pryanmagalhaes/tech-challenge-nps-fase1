# 2. Definição da variável-alvo (target)

> Etapa conceitual: qual é o alvo do problema e quais cuidados ele exige.

## 2.1 Qual variável representa a satisfação do cliente?

**`nps_score`**: a nota de 0 a 10 que o cliente dá à pergunta de recomendação, coletada após a experiência de compra.

Para a leitura de negócio, a nota é convertida nas três categorias oficiais do NPS:

| Categoria | Regra oficial (inteiros) | Regra adotada (nota contínua da base) |
|---|---|---|
| **Promotor** | 9 ou 10 | nota ≥ 9,0 |
| **Neutro** | 7 ou 8 | 7,0 ≤ nota < 9,0 |
| **Detrator** | 0 a 6 | nota < 7,0 |

E o indicador consolidado é: **NPS = % promotores − % detratores**, de −100 a +100.

A base traz as notas **com casa decimal** (ex.: 6,9). Isso não ocorre numa pesquisa NPS real. Testamos as duas formas de classificar (cortes contínuos e arredondamento): o NPS fica entre −80 e −74, e **o diagnóstico não muda** (notebook 01, seção 4.1).

## 2.2 Por que essa variável foi escolhida?

| Critério | `nps_score` | Alternativas consideradas |
|---|---|---|
| **É a métrica que o negócio quer mover** | Sim. O case nasce da variabilidade do NPS | — |
| **Mede a experiência inteira** | Sim. A pergunta de recomendação resume a jornada toda | `csat_internal_score` se relaciona sobretudo com o **atendimento** (correlação de −0,74 com o tempo de resolução), não com a jornada completa |
| **É comparável com o mercado** | Sim. Metodologia padronizada e amplamente usada | O CSAT interno é uma escala própria, sem benchmark externo |
| **Antecede o resultado financeiro** | Sim. A nota se conecta à recompra | `repeat_purchase_30d` é **resultado**, não satisfação; além disso, só é conhecido 30 dias depois |

Em resumo: o NPS é a variável que o negócio usa para se medir, que resume a experiência inteira e que antecede o resultado financeiro. Recompra e CSAT são úteis como **validação** e **monitoramento**, não como alvo.

## 2.3 Em que momento da jornada a informação é coletada?

```
Compra  ──►  Pagamento  ──►  Expedição  ──►  Entrega  ──►  Atendimento  ──►  ★ Pesquisa NPS  ──►  Recompra (30d)
 valor,        parcelas,       frete,          prazo,        contatos,          nps_score            repeat_purchase_30d
 itens,        desconto                        atraso,       reclamações,       (csat_internal_score
 região                                        tentativas    resolução           coletado em paralelo)
```

O NPS é coletado **no fim da jornada**, depois da entrega e de eventuais interações com o atendimento. Esse é exatamente o problema de negócio: quando a nota chega, a experiência já aconteceu. Todos os fatores operacionais (pedido, logística, atendimento) são conhecidos **antes** da pesquisa, e por isso podem ser usados como sinais antecipados.

## 2.4 Riscos de usar essa variável de forma inadequada

| Risco | O que pode dar errado | Como mitigar |
|---|---|---|
| **Vazamento de informação** (*data leakage*) | Usar `repeat_purchase_30d` ou `csat_internal_score` para “explicar” ou prever o NPS. A recompra acontece **depois** da pesquisa; o CSAT é outra medida de satisfação. O resultado seria um modelo que parece excelente no papel e é inútil na prática | Usar apenas variáveis disponíveis **antes** da pesquisa. Neste projeto, as duas variáveis foram separadas como “pós-pesquisa” em `src/config.py` |
| **Tratar a média da nota como NPS** | Nota média 4,4 e NPS −80 contam histórias diferentes. O NPS ignora neutros e é sensível à **cauda**; a média esconde a polarização | Sempre reportar o NPS oficial e a distribuição por categoria |
| **Viés de resposta** | Quem responde pesquisa tende a estar nos extremos (muito satisfeito ou muito irritado). Se a taxa de resposta variar por perfil, o NPS não representa toda a base | Monitorar a taxa de resposta por segmento; ponderar quando necessário |
| **Confundir correlação com causa** | “Clientes com mais contatos têm nota pior” não significa que **atender** piora a nota: o contato é sintoma de um problema anterior | Ler os achados como **associação**; validar causalidade com testes A/B ou pilotos controlados |
| **Gaming da métrica** | Se o NPS virar meta individual, equipes podem induzir a nota (“dê 10, por favor”) ou escolher a quem enviar a pesquisa | Usar o NPS como indicador de gestão, com regras de amostragem fixas; combinar com indicadores operacionais |
| **Arbitrariedade do corte** | Um cliente com 6,9 é detrator e um com 7,0 é neutro. Pequenas mudanças podem virar grandes variações no indicador | Analisar também a nota contínua e testar sensibilidade aos cortes (feito no notebook 01) |
| **Grupos pequenos** | NPS de um segmento com 20 respostas oscila muito por acaso | Reportar intervalo de confiança (bootstrap) e volume junto de cada NPS |
| **Base possivelmente simulada** | Relações perfeitas (ex.: recompra 100% acima de nota 8) indicam regras de geração. Magnitudes não devem ser extrapoladas para a operação real | Usar a **direção** dos achados; recalibrar com dados reais antes de projetar impacto financeiro |
