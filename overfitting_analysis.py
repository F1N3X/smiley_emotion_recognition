from __future__ import annotations

import csv
from pathlib import Path
from configs import *

WIDTH, HEIGHT = 1000, 600
MARGIN = {"left": 90, "right": 40, "top": 70, "bottom": 80}

PLOT_W = WIDTH  - MARGIN["left"] - MARGIN["right"]
PLOT_H = HEIGHT - MARGIN["top"]  - MARGIN["bottom"]


def load_losses(path: Path) -> tuple[list[int], list[float], list[float]]:
    epochs, train_losses, val_losses = [], [], []

    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            epochs.append(int(row["epoch"]))
            train_losses.append(float(row["train_loss"]))
            val_losses.append(float(row["validation_loss"]))

    if not epochs:
        raise ValueError(f"No data found in {path}")

    return epochs, train_losses, val_losses


def to_svg_x(epoch: int, x_min: int, x_max: int):
    ratio = (epoch - x_min) / (x_max - x_min)
    return MARGIN["left"] + ratio * PLOT_W


def to_svg_y(loss: float, y_min: float, y_max: float):
    ratio = (loss - y_min) / (y_max - y_min)
    return MARGIN["top"] + PLOT_H - ratio * PLOT_H  # SVG y-axis is inverted


def build_polyline(epochs: list[int], losses: list[float], x_min, x_max, y_min, y_max):
    return " ".join(
        f"{to_svg_x(e, x_min, x_max):.1f},{to_svg_y(l, y_min, y_max):.1f}"
        for e, l in zip(epochs, losses)
    )


def build_grid(y_min: float, y_max: float):
    lines = []
    for i in range(6):
        y_val = y_min + (y_max - y_min) * i / 5
        y_svg = to_svg_y(y_val, y_min, y_max)
        x1, x2 = MARGIN["left"], MARGIN["left"] + PLOT_W
        lines += [
            f'<line x1="{x1}" y1="{y_svg:.1f}" x2="{x2}" y2="{y_svg:.1f}" stroke="#d9d9d9" stroke-width="1"/>',
            f'<text x="{x1 - 10}" y="{y_svg + 4:.1f}" text-anchor="end" font-size="12" fill="#555">{y_val:.2f}</text>',
        ]
    return lines


def build_x_ticks(epochs: list[int], x_min: int, x_max: int):
    ticks = []
    y_base = MARGIN["top"] + PLOT_H
    for i in range(min(8, len(epochs))):
        epoch = epochs[round(i * (len(epochs) - 1) / 7)]
        x_svg = to_svg_x(epoch, x_min, x_max)
        ticks += [
            f'<line x1="{x_svg:.1f}" y1="{y_base}" x2="{x_svg:.1f}" y2="{y_base + 6}" stroke="#444" stroke-width="1"/>',
            f'<text x="{x_svg:.1f}" y="{y_base + 22}" text-anchor="middle" font-size="12" fill="#555">{epoch}</text>',
        ]
    return ticks


def plot_losses(epochs: list[int], train_losses: list[float], val_losses: list[float]):
    x_min, x_max = min(epochs), max(epochs)

    all_losses = train_losses + val_losses
    y_min = min(all_losses) - (max(all_losses) - min(all_losses)) * 0.08
    y_max = max(all_losses) + (max(all_losses) - min(all_losses)) * 0.08

    train_polyline = build_polyline(epochs, train_losses, x_min, x_max, y_min, y_max)
    val_polyline   = build_polyline(epochs, val_losses,   x_min, x_max, y_min, y_max)

    grid   = build_grid(y_min, y_max)
    ticks  = build_x_ticks(epochs, x_min, x_max)

    cx = WIDTH / 2
    lx = WIDTH - 255  # legend x
    ax = MARGIN["left"]
    ay = MARGIN["top"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}">
  <rect width="100%" height="100%" fill="#ffffff"/>

  <text x="{cx}" y="36" text-anchor="middle" font-size="24" font-weight="700" fill="#111">Comparaison des courbes de loss</text>
  <text x="{cx}" y="58" text-anchor="middle" font-size="13" fill="#666">Training loss vs validation loss</text>

  <rect x="{ax}" y="{ay}" width="{PLOT_W}" height="{PLOT_H}" fill="#fafafa" stroke="#cccccc"/>
  {''.join(grid)}
  {''.join(ticks)}

  <line x1="{ax}" y1="{ay}" x2="{ax}" y2="{ay + PLOT_H}" stroke="#333" stroke-width="1.5"/>
  <line x1="{ax}" y1="{ay + PLOT_H}" x2="{ax + PLOT_W}" y2="{ay + PLOT_H}" stroke="#333" stroke-width="1.5"/>

  <text x="{cx}" y="{HEIGHT - 22}" text-anchor="middle" font-size="13" fill="#333">Epoch</text>
  <text x="24" y="{ay + PLOT_H / 2}" text-anchor="middle" font-size="13" fill="#333"
        transform="rotate(-90 24 {ay + PLOT_H / 2})">Loss</text>

  <polyline fill="none" stroke="#1f77b4" stroke-width="3" stroke-linejoin="round" points="{train_polyline}"/>
  <polyline fill="none" stroke="#ff7f0e" stroke-width="3" stroke-linejoin="round" points="{val_polyline}"/>

  <rect x="{lx}" y="88" width="205" height="64" rx="10" fill="#ffffff" stroke="#dddddd"/>
  <line x1="{lx + 23}" y1="112" x2="{lx + 63}" y2="112" stroke="#1f77b4" stroke-width="3"/>
  <text x="{lx + 75}" y="116" font-size="13" fill="#222">Train loss</text>
  <line x1="{lx + 23}" y1="136" x2="{lx + 63}" y2="136" stroke="#ff7f0e" stroke-width="3"/>
  <text x="{lx + 75}" y="140" font-size="13" fill="#222">Validation loss</text>
</svg>"""

    OUTPUT_PATH.write_text(svg, encoding="utf-8")


def main():
    if not METRICS_PATH.exists():
        raise FileNotFoundError(f"Fichier introuvable : {METRICS_PATH}")

    epochs, train_losses, val_losses = load_losses(METRICS_PATH)
    plot_losses(epochs, train_losses, val_losses)
    print(f"Graphique enregistré dans {OUTPUT_PATH}")


if __name__ == "__main__":
    main()