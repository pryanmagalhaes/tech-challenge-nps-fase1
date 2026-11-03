"""Padrão visual dos gráficos: limpo, legível e consistente com a apresentação."""
from __future__ import annotations

import matplotlib.pyplot as plt

from .config import COLORS, FIGURES_DIR


def set_style() -> None:
    """Aplica o estilo do projeto a todos os gráficos matplotlib/seaborn."""
    plt.rcParams.update({
        "figure.figsize": (10, 5),
        "figure.dpi": 110,
        "savefig.dpi": 160,
        "savefig.bbox": "tight",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 30,
        "axes.labelcolor": COLORS["muted"],
        "axes.edgecolor": COLORS["grid"],
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": COLORS["grid"],
        "grid.linewidth": 0.8,
        "xtick.color": COLORS["muted"],
        "ytick.color": COLORS["muted"],
        "text.color": COLORS["ink"],
        "legend.frameon": False,
    })


def subtitle(ax, text: str) -> None:
    """Subtítulo em cinza logo abaixo do título (a 'mensagem' do gráfico)."""
    ax.text(0, 1.025, text, transform=ax.transAxes, fontsize=10.5,
            color=COLORS["muted"], va="bottom")


def save(fig, name: str) -> None:
    """Salva a figura em reports/figures com nome padronizado."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES_DIR / f"{name}.png", facecolor="white")
