# 1. Entendimento do negócio

> Etapa conceitual. O objetivo aqui é enquadrar o problema antes de olhar os dados, para que a análise responda à pergunta certa.

## 1.1 Qual problema de negócio está sendo resolvido?

A empresa cresceu rápido no e-commerce e passou a operar um volume muito maior de pedidos, entregas e atendimentos. Com a escala, a satisfação dos clientes ficou **instável e difícil de explicar**: clientes com indicadores operacionais aparentemente parecidos terminam a jornada como promotores ou como detratores.

O problema tem duas camadas:

| Camada | Descrição | Consequência hoje |
|---|---|---|
| **Diagnóstico** | A empresa não sabe quais fatores operacionais realmente movem a satisfação | Recursos são distribuídos sem prioridade clara entre logística, atendimento, preço e produto |
| **Tempo** | O NPS só é coletado **depois** que a jornada termina | A empresa descobre a insatisfação quando não há mais o que fazer pelo cliente; a gestão é **reativa** |

Em uma frase: **transformar dados operacionais que já existem durante a jornada em sinais antecipados de insatisfação, para que a empresa aja enquanto ainda é possível mudar a experiência do cliente.**

A pergunta orientadora desta fase é:

> **Quais fatores operacionais realmente explicam a satisfação do cliente, e em que ponto da jornada a empresa deveria agir antes da pesquisa de NPS?**

## 1.2 Por que o NPS é importante para um e-commerce?

O Net Promoter Score mede a **disposição do cliente em recomendar** a empresa (“De 0 a 10, quanto você recomendaria…?”). Ele importa especialmente no e-commerce por quatro razões:

1. **A troca de loja custa um clique.** No varejo físico, conveniência e localização seguram o cliente. No digital, o concorrente está na aba ao lado, e o custo de mudar é quase zero. Lealdade precisa ser conquistada a cada pedido.
2. **A experiência é majoritariamente operacional.** O cliente não vê a loja, o vendedor ou o estoque; ele vê **prazo, entrega e atendimento**. Por isso o NPS no e-commerce funciona como um termômetro direto da operação.
3. **Reputação é pública e pesquisável.** Avaliações em marketplaces, Reclame Aqui e redes sociais influenciam a decisão de compra de quem nunca comprou. Um detrator escreve; um promotor indica.
4. **É simples, comparável e acionável.** Uma única pergunta, com metodologia padronizada, permite comparar períodos, canais, regiões e concorrentes, e conectar a nota a ações.

## 1.3 Quais áreas se beneficiam desses insights?

| Área | Como usa os insights | Exemplo de decisão |
|---|---|---|
| **Logística** | Saber que o **atraso**, e não o prazo total, define a nota | Recalibrar o prazo prometido por rota; renegociar SLA com transportadoras com base no impacto em NPS |
| **Atendimento (SAC)** | Saber que cada contato e cada reclamação adicional derrubam a nota | Meta de resolução no 1º contato; fila prioritária para pedidos atrasados |
| **Produto / UX** | Exibir no checkout um prazo realista e comunicação proativa no rastreio | Mostrar prazo com margem de segurança; notificar atraso antes do cliente perguntar |
| **Pricing / Comercial** | Saber que desconto, parcelamento e frete **não** compram satisfação nesta base | Evitar usar cupom como “remédio” para problema operacional |
| **CRM / Marketing** | Identificar promotores (candidatos a indicação) e detratores em formação | Programa de indicação para promotores; ação de recuperação para clientes com atraso |
| **Estratégia / Diretoria** | Ver o NPS como indicador antecedente de recompra e de reputação | Priorizar investimentos que movem a nota, não apenas os que reduzem custo |
| **Finanças** | Conectar satisfação a receita recorrente | Estimar o valor de reter um cliente e o custo de um detrator |

## 1.4 Reflexão: como o NPS impacta o negócio

### Recompra
Promotores voltam a comprar com mais frequência e são menos sensíveis a preço. No e-commerce, onde o **custo de aquisição de cliente (CAC)** costuma ser alto e crescente, a recompra é o que torna um cliente lucrativo: o primeiro pedido frequentemente apenas paga a aquisição. Detratores, por outro lado, raramente voltam; cada um representa um CAC que não se pagou.

> Na base analisada, **nenhum detrator recomprou em 30 dias** e **todos os promotores recompraram**. A relação é perfeita demais para ser real (ver limitações), mas a direção é clara e consistente com a literatura de mercado.

### Boca a boca
O NPS foi criado justamente para medir o potencial de boca a boca. Promotores trazem clientes novos com **CAC próximo de zero** e com mais confiança na marca. Detratores fazem o oposto, e de forma assimétrica: experiências negativas tendem a ser compartilhadas com mais pessoas e com mais intensidade do que as positivas, e hoje ficam **registradas publicamente** (avaliações, Reclame Aqui, redes sociais), influenciando clientes futuros por muito tempo.

### Market share em e-commerce
No digital, participação de mercado é resultado de **aquisição + retenção + reputação**. O NPS afeta as três:
- **Retenção:** promotores ficam; detratores migram para o concorrente, que ganha share sem gastar em aquisição.
- **Aquisição:** a reputação pública reduz (ou aumenta) a taxa de conversão de quem está decidindo onde comprar.
- **Eficiência:** uma base de promotores permite crescer com menos investimento em mídia, liberando margem para preço e serviço.

Empresas com NPS consistentemente superior ao dos concorrentes tendem a crescer acima do mercado. Com NPS de −80, a empresa está, na prática, **financiando o crescimento dos concorrentes**: cada detrator é um cliente e uma recomendação que mudam de lado.

## 1.5 Indicadores de mercado que complementariam a análise

| Indicador | O que acrescenta | Fonte possível |
|---|---|---|
| **Benchmark de NPS do setor** | Saber se −80 é um problema da empresa ou do segmento | Estudos setoriais de NPS, consultorias de CX, associações de varejo digital |
| **SLA logístico de mercado** | Comparar prazo prometido e taxa de entrega no prazo com os concorrentes | Relatórios de transportadoras, estudos de logística de e-commerce, mystery shopping |
| **Reputação pública** | Nota e índice de solução de reclamações versus concorrentes | Reclame Aqui, avaliações em marketplaces e lojas de aplicativo |
| **Prazo e frete dos concorrentes** | Entender se a promessa da empresa é competitiva | Coleta de preços e prazos (web scraping / benchmarking) |
| **Share of wallet e churn** | Quanto do gasto do cliente na categoria fica com a empresa | Painéis de consumo, dados de cartão/fintechs |
| **CAC e LTV** | Traduzir NPS em valor financeiro | Dados internos de marketing e finanças |
| **Sazonalidade de mercado** | Separar efeito operacional de picos de demanda (Black Friday, Natal) | Calendário comercial e volume histórico |
| **Indicadores internos já existentes** | CSAT, tempo médio de atendimento, taxa de resolução no 1º contato, OTIF | Sistemas de SAC e de logística |

> **OTIF** (*On Time In Full*): percentual de pedidos entregues no prazo e completos. É o indicador logístico mais próximo do que esta análise mostrou ser o principal fator de satisfação.
