# Dicionário de dados

Base: `data/raw/desafio_nps_fase_1.csv` · 2.500 linhas · 19 colunas · 0 nulos · 0 duplicados.
Granularidade: **1 linha = 1 cliente = 1 pedido = 1 resposta de NPS.**

## Variáveis originais

| Coluna | Descrição | Tipo | Faixa observada | Etapa da jornada | Papel na análise | Observações de qualidade |
|---|---|---|---|---|---|---|
| `customer_id` | Identificador único do cliente | inteiro | 1 a 2.500 | — | Identificador | Único por linha |
| `order_id` | Identificador único do pedido | inteiro | 50.001 a 52.500 | — | Identificador | Único por linha |
| `customer_age` | Idade do cliente | inteiro | 18 a 69 | Cliente | Fator (perfil) | — |
| `customer_region` | Região geográfica | categórica | 5 regiões | Cliente | Fator (perfil) | Distribuição equilibrada (468 a 521 por região) |
| `customer_tenure_months` | Tempo de relacionamento (meses) | inteiro | 1 a 119 | Cliente | Fator (perfil) | — |
| `order_value` | Valor total do pedido | decimal | 7,76 a 1.983,81 | Pedido | Fator | Pode ser líquido de desconto (1,4% com desconto > valor) |
| `items_quantity` | Quantidade de itens | inteiro | 1 a 6 | Pedido | Fator | — |
| `discount_value` | Valor de desconto | decimal | 0,02 a 230,33 | Pedido | Fator | Ver `order_value` |
| `payment_installments` | Número de parcelas | inteiro | 1 a 11 | Pedido | Fator | — |
| `delivery_time_days` | Tempo total de entrega (dias) | inteiro | 2 a 14 | Logística | Fator | 4,8% com atraso > prazo total: definição a confirmar |
| `delivery_delay_days` | Dias de atraso | inteiro | 0 a 8 | Logística | **Fator nº 1** | 88,9% dos pedidos têm atraso ≥ 1 dia |
| `freight_value` | Valor do frete | decimal | 2,62 a 76,13 | Logística | Fator | — |
| `delivery_attempts` | Tentativas de entrega | inteiro | 1 a 3 | Logística | Fator | — |
| `customer_service_contacts` | Contatos com o atendimento | inteiro | 0 a 7 | Atendimento | Fator | — |
| `resolution_time_days` | Tempo de resolução (dias) | inteiro | 0 a 11 | Atendimento | Fator | 20,4% com resolução > 0 sem contato registrado |
| `complaints_count` | Reclamações registradas | inteiro | 0 a 11 | Atendimento | Fator | 97,1% com mais reclamações que contatos: provavelmente multicanal |
| `nps_score` | Nota NPS (0 a 10) | decimal | 0 a 10 | Pós-jornada | **Alvo** | Nota contínua (atípico para NPS) |
| `repeat_purchase_30d` | Recompra em até 30 dias | binária | 0 / 1 | Pós-pesquisa | **Consequência** (não usar como fator) | Relação determinística com a nota (100% se nota ≥ 8) |
| `csat_internal_score` | Score interno de satisfação | decimal | 0 a 10 | Pós-atendimento | **Consequência / outra medida** (não usar como fator) | 18,5% exatamente zero |

## Variáveis criadas (`src/data_prep.py`)

| Coluna | Regra | Uso |
|---|---|---|
| `nps_category` | Detrator < 7 ≤ Neutro < 9 ≤ Promotor | Leitura oficial do NPS |
| `is_detractor`, `is_promoter` | Indicadores 0/1 da categoria | Cálculo de taxas |
| `delay_band` | No prazo, 1, 2, 3, 4+ dias | Ponto de ruptura logístico |
| `complaints_band` | 0–1, 2–3, 4–5, 6+ | Ponto de ruptura no atendimento |
| `contacts_band` | 0, 1, 2, 3+ | Ponto de ruptura no atendimento |
| `resolution_band` | 0–2, 3–5, 6–8, 9+ dias | Efeito do tempo de resolução |
| `age_band`, `tenure_band`, `order_value_band` | Faixas de perfil (valor em quintis) | Perfil de cliente |
| `discount_pct`, `freight_pct` | Desconto e frete em % do pedido | Comparação entre tickets |
| `is_late` | Atraso > 0 | Indicador de pontualidade |
| `frictionless_journey` | Atraso ≤ 1 dia **e** reclamações ≤ 1 | Jornada sem atrito |
| `dq_*` | Uma flag por regra de qualidade | Auditoria e teste de robustez |
| `dq_critical` | Atraso > prazo **ou** desconto > valor | Teste de robustez |
