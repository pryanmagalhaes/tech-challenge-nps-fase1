"""Configurações centrais do projeto.

Tudo o que é "regra de negócio" ou "decisão de projeto" fica aqui, em um único
lugar, para que notebooks e scripts usem exatamente os mesmos parâmetros.
"""
from pathlib import Path

# ---------------------------------------------------------------------------
# Caminhos (resolvidos a partir da raiz do repositório, independente de onde
# o notebook ou script é executado)
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_RAW_PATH = ROOT_DIR / "data" / "raw" / "desafio_nps_fase_1.csv"
DATA_PROCESSED_DIR = ROOT_DIR / "data" / "processed"
DATA_PROCESSED_PATH = DATA_PROCESSED_DIR / "nps_tratado.csv"
REPORTS_DIR = ROOT_DIR / "reports"
QUALITY_REPORT_PATH = REPORTS_DIR / "data_quality_report.csv"
FIGURES_DIR = REPORTS_DIR / "figures"
METRICS_JSON_PATH = REPORTS_DIR / "key_metrics.json"

# ---------------------------------------------------------------------------
# Regra oficial do NPS (Bain & Company / Fred Reichheld)
#   Promotor: 9–10 | Neutro: 7–8 | Detrator: 0–6
# Como a base traz notas contínuas (ex.: 6.9), adotamos limites contínuos:
#   Promotor: nota >= 9.0 | Neutro: 7.0 <= nota < 9.0 | Detrator: nota < 7.0
# A sensibilidade a essa escolha é testada no notebook 01.
# ---------------------------------------------------------------------------
PROMOTER_THRESHOLD = 9.0
PASSIVE_THRESHOLD = 7.0
NPS_CATEGORY_ORDER = ["Detrator", "Neutro", "Promotor"]

# ---------------------------------------------------------------------------
# Grupos de variáveis por etapa da jornada (usados na EDA)
# ---------------------------------------------------------------------------
ID_COLS = ["customer_id", "order_id"]
TARGET_COL = "nps_score"

CUSTOMER_COLS = ["customer_age", "customer_region", "customer_tenure_months"]
ORDER_COLS = ["order_value", "items_quantity", "discount_value", "payment_installments"]
LOGISTICS_COLS = ["delivery_time_days", "delivery_delay_days", "freight_value", "delivery_attempts"]
SERVICE_COLS = ["customer_service_contacts", "resolution_time_days", "complaints_count"]

# Variáveis observadas DEPOIS (ou junto) da pesquisa de NPS. São úteis para
# entender a CONSEQUÊNCIA da satisfação, mas não devem ser usadas para
# explicar ou prever o NPS (risco de vazamento de informação / causalidade reversa).
POST_SURVEY_COLS = ["repeat_purchase_30d", "csat_internal_score"]

# Variáveis numéricas candidatas a "fatores operacionais" da satisfação
DRIVER_COLS = (
    ["customer_age", "customer_tenure_months"] + ORDER_COLS + LOGISTICS_COLS + SERVICE_COLS
)

# Rótulos em português para gráficos e tabelas voltados ao negócio
LABELS_PT = {
    "customer_age": "Idade do cliente",
    "customer_region": "Região",
    "customer_tenure_months": "Tempo de casa (meses)",
    "order_value": "Valor do pedido",
    "items_quantity": "Qtd. de itens",
    "discount_value": "Desconto",
    "payment_installments": "Nº de parcelas",
    "delivery_time_days": "Prazo total de entrega",
    "delivery_delay_days": "Dias de atraso",
    "freight_value": "Valor do frete",
    "delivery_attempts": "Tentativas de entrega",
    "customer_service_contacts": "Contatos com atendimento",
    "resolution_time_days": "Tempo de resolução",
    "complaints_count": "Reclamações",
    "repeat_purchase_30d": "Recompra em 30 dias",
    "csat_internal_score": "CSAT interno",
    "nps_score": "Nota NPS",
}

# ---------------------------------------------------------------------------
# Identidade visual (mesma paleta dos gráficos e da apresentação)
# ---------------------------------------------------------------------------
COLORS = {
    "ink": "#1B2430",
    "muted": "#6B7482",
    "grid": "#E3E6EA",
    "paper": "#FFFFFF",
    "detractor": "#B3261E",
    "passive": "#C98A0B",
    "promoter": "#1F7A6D",
    "highlight": "#2F5DA8",
}
CATEGORY_COLORS = {
    "Detrator": COLORS["detractor"],
    "Neutro": COLORS["passive"],
    "Promotor": COLORS["promoter"],
}

RANDOM_SEED = 42
