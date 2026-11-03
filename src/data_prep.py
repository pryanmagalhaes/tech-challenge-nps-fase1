"""Carga, auditoria de qualidade e tratamento da base de NPS.

Filosofia adotada:
    * NÃO apagamos linhas suspeitas: sinalizamos com flags (dq_*). Em uma base
      de 2.500 pedidos, remover registros sem confirmação do dono do dado
      enviesaria a análise. As flags permitem testar se os achados mudam
      quando os registros suspeitos são excluídos (teste de robustez).
    * Toda regra de qualidade é explícita e documentada em DATA_QUALITY_RULES.
"""
from __future__ import annotations

import pandas as pd

from .config import DATA_RAW_PATH, ID_COLS, TARGET_COL
from .metrics import classify_nps

# Esquema esperado: coluna -> (tipo, mínimo plausível, máximo plausível)
EXPECTED_SCHEMA = {
    "customer_id": ("int", 1, None),
    "customer_age": ("int", 18, 100),
    "customer_region": ("category", None, None),
    "customer_tenure_months": ("int", 0, None),
    "order_id": ("int", 1, None),
    "order_value": ("float", 0, None),
    "items_quantity": ("int", 1, None),
    "discount_value": ("float", 0, None),
    "payment_installments": ("int", 1, 24),
    "delivery_time_days": ("int", 0, None),
    "delivery_delay_days": ("int", 0, None),
    "freight_value": ("float", 0, None),
    "delivery_attempts": ("int", 1, None),
    "customer_service_contacts": ("int", 0, None),
    "resolution_time_days": ("int", 0, None),
    "nps_score": ("float", 0, 10),
    "repeat_purchase_30d": ("int", 0, 1),
    "complaints_count": ("int", 0, None),
    "csat_internal_score": ("float", 0, 10),
}

# Regras de consistência de negócio (cada uma vira uma flag dq_*)
DATA_QUALITY_RULES = {
    "dq_delay_gt_delivery_time": (
        "Dias de atraso maiores que o prazo total de entrega",
        lambda d: d["delivery_delay_days"] > d["delivery_time_days"],
    ),
    "dq_discount_gt_order_value": (
        "Desconto maior que o valor do pedido",
        lambda d: d["discount_value"] > d["order_value"],
    ),
    "dq_resolution_without_contact": (
        "Tempo de resolução > 0 sem nenhum contato com o atendimento",
        lambda d: (d["resolution_time_days"] > 0) & (d["customer_service_contacts"] == 0),
    ),
    "dq_complaints_gt_contacts": (
        "Mais reclamações do que contatos com o atendimento",
        lambda d: d["complaints_count"] > d["customer_service_contacts"],
    ),
    "dq_csat_zero": (
        "CSAT interno exatamente 0 (possível valor padrão / ausente)",
        lambda d: d["csat_internal_score"] == 0,
    ),
}


def load_raw(path=DATA_RAW_PATH) -> pd.DataFrame:
    """Lê a base bruta exatamente como foi recebida."""
    return pd.read_csv(path)


def validate_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Confere colunas, nulos e faixas plausíveis. Retorna uma tabela de auditoria."""
    rows = []
    for col, (dtype, vmin, vmax) in EXPECTED_SCHEMA.items():
        present = col in df.columns
        series = df[col] if present else pd.Series(dtype=float)
        is_num = present and pd.api.types.is_numeric_dtype(series)
        rows.append({
            "coluna": col,
            "presente": present,
            "tipo_esperado": dtype,
            "nulos": int(series.isna().sum()) if present else None,
            "abaixo_do_minimo": int((series < vmin).sum()) if (is_num and vmin is not None) else 0,
            "acima_do_maximo": int((series > vmax).sum()) if (is_num and vmax is not None) else 0,
            "min": series.min() if is_num else None,
            "max": series.max() if is_num else None,
        })
    missing_extra = set(df.columns) - set(EXPECTED_SCHEMA)
    if missing_extra:
        print(f"Atenção: colunas não previstas no dicionário: {sorted(missing_extra)}")
    return pd.DataFrame(rows)


def audit_consistency(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica as regras de negócio e devolve volume e % de registros afetados."""
    rows = []
    for flag, (description, rule) in DATA_QUALITY_RULES.items():
        mask = rule(df)
        rows.append({"regra": flag, "descricao": description,
                     "registros": int(mask.sum()), "%_base": round(mask.mean() * 100, 1)})
    duplicated_orders = int(df.duplicated(subset=ID_COLS[1:]).sum())
    rows.append({"regra": "dq_duplicated_order", "descricao": "order_id duplicado",
                 "registros": duplicated_orders, "%_base": round(duplicated_orders / len(df) * 100, 1)})
    return pd.DataFrame(rows)


def add_quality_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona uma coluna booleana por regra de qualidade + flag consolidada."""
    out = df.copy()
    for flag, (_, rule) in DATA_QUALITY_RULES.items():
        out[flag] = rule(out)
    # Flag "crítica": inconsistências lógicas de logística/financeiro.
    # As regras de atendimento e CSAT são tratadas como "dúvida de definição",
    # não como erro, e por isso não entram aqui (ver notebook 01).
    out["dq_critical"] = out["dq_delay_gt_delivery_time"] | out["dq_discount_gt_order_value"]
    return out


def add_business_features(df: pd.DataFrame) -> pd.DataFrame:
    """Cria variáveis de leitura de negócio usadas na EDA (sem alterar as originais)."""
    out = df.copy()

    # Alvo em categorias oficiais do NPS
    out["nps_category"] = pd.Categorical(classify_nps(out[TARGET_COL]),
                                         categories=["Detrator", "Neutro", "Promotor"], ordered=True)
    out["is_detractor"] = (out["nps_category"] == "Detrator").astype(int)
    out["is_promoter"] = (out["nps_category"] == "Promotor").astype(int)

    # Faixas operacionais (pontos de corte definidos com base na EDA e na leitura de negócio)
    out["delay_band"] = pd.cut(out["delivery_delay_days"], [-1, 0, 1, 2, 3, 99],
                               labels=["No prazo", "1 dia", "2 dias", "3 dias", "4+ dias"])
    out["complaints_band"] = pd.cut(out["complaints_count"], [-1, 1, 3, 5, 99],
                                    labels=["0–1", "2–3", "4–5", "6+"])
    out["contacts_band"] = pd.cut(out["customer_service_contacts"], [-1, 0, 1, 2, 99],
                                  labels=["0", "1", "2", "3+"])
    out["resolution_band"] = pd.cut(out["resolution_time_days"], [-1, 2, 5, 8, 99],
                                    labels=["0–2 dias", "3–5 dias", "6–8 dias", "9+ dias"])
    out["age_band"] = pd.cut(out["customer_age"], [17, 25, 35, 45, 55, 120],
                             labels=["18–25", "26–35", "36–45", "46–55", "56+"])
    out["tenure_band"] = pd.cut(out["customer_tenure_months"], [0, 12, 36, 60, 999],
                                labels=["Até 1 ano", "1–3 anos", "3–5 anos", "5+ anos"])
    out["order_value_band"] = pd.qcut(out["order_value"], 5,
                                      labels=["Q1 (menor)", "Q2", "Q3", "Q4", "Q5 (maior)"])

    # Indicadores derivados
    out["discount_pct"] = (out["discount_value"] / out["order_value"]).clip(upper=1) * 100
    out["freight_pct"] = out["freight_value"] / out["order_value"] * 100
    out["is_late"] = (out["delivery_delay_days"] > 0).astype(int)

    # "Jornada sem atrito": sem atraso relevante e sem escalonamento no atendimento
    out["frictionless_journey"] = (
        (out["delivery_delay_days"] <= 1) & (out["complaints_count"] <= 1)
    ).astype(int)
    return out


def build_processed_dataset(path=DATA_RAW_PATH) -> pd.DataFrame:
    """Pipeline completo: carga -> flags de qualidade -> features de negócio."""
    df = load_raw(path)
    df["customer_region"] = df["customer_region"].astype("category")
    df = add_quality_flags(df)
    df = add_business_features(df)
    return df
