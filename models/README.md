# models/

Pasta reservada para a próxima fase do projeto (modelo preditivo de NPS).

O desafio opcional (item 4) **não** foi executado nesta entrega, por decisão de escopo. A EDA já deixa preparados os insumos do modelo:

- Alvo definido e testado (`nps_score` / `nps_category`), ver `docs/02_definicao_da_target.md`;
- Lista de variáveis **proibidas** por vazamento de informação (`POST_SURVEY_COLS` em `src/config.py`);
- Fatores com sinal comprovado (atraso, reclamações, contatos, tempo de resolução) e fatores sem sinal.
