"""Métricas de negócio: NPS e intervalos de confiança."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import PASSIVE_THRESHOLD, PROMOTER_THRESHOLD, RANDOM_SEED


def classify_nps(score: pd.Series) -> pd.Series:
    """Classifica cada nota em Detrator / Neutro / Promotor (regra em config.py)."""
    category = np.select(
        [score >= PROMOTER_THRESHOLD, score >= PASSIVE_THRESHOLD],
        ["Promotor", "Neutro"],
        default="Detrator",
    )
    return pd.Series(category, index=score.index, name="nps_category")


def nps_value(score: pd.Series) -> float:
    """NPS = % de promotores − % de detratores (escala de −100 a +100)."""
    if len(score) == 0:
        return np.nan
    promoters = (score >= PROMOTER_THRESHOLD).mean()
    detractors = (score < PASSIVE_THRESHOLD).mean()
    return float((promoters - detractors) * 100)


def nps_bootstrap_ci(score: pd.Series, n_boot: int = 2000, alpha: float = 0.05,
                     seed: int = RANDOM_SEED) -> tuple[float, float]:
    """Intervalo de confiança (percentil) do NPS via bootstrap.

    Serve para mostrar ao negócio a margem de incerteza de cada número,
    principalmente em grupos com poucos pedidos.
    """
    values = np.asarray(score)
    if len(values) < 2:
        return (np.nan, np.nan)
    rng = np.random.default_rng(seed)
    samples = rng.choice(values, size=(n_boot, len(values)), replace=True)
    boots = ((samples >= PROMOTER_THRESHOLD).mean(axis=1)
             - (samples < PASSIVE_THRESHOLD).mean(axis=1)) * 100
    return (float(np.percentile(boots, 100 * alpha / 2)),
            float(np.percentile(boots, 100 * (1 - alpha / 2))))


def nps_summary(df: pd.DataFrame, by, score_col: str = "nps_score",
                with_ci: bool = False) -> pd.DataFrame:
    """Tabela-resumo por grupo: volume, nota média, % de cada categoria e NPS."""
    grouped = df.groupby(by, observed=True)[score_col]
    summary = pd.DataFrame({
        "pedidos": grouped.size(),
        "share_base_%": grouped.size() / len(df) * 100,
        "nota_media": grouped.mean(),
        "%_detratores": grouped.apply(lambda s: (s < PASSIVE_THRESHOLD).mean() * 100),
        "%_neutros": grouped.apply(
            lambda s: ((s >= PASSIVE_THRESHOLD) & (s < PROMOTER_THRESHOLD)).mean() * 100),
        "%_promotores": grouped.apply(lambda s: (s >= PROMOTER_THRESHOLD).mean() * 100),
        "NPS": grouped.apply(nps_value),
    })
    if with_ci:
        ci = grouped.apply(nps_bootstrap_ci)
        summary["NPS_IC95_inf"] = ci.apply(lambda t: t[0])
        summary["NPS_IC95_sup"] = ci.apply(lambda t: t[1])
    return summary.round(1)
