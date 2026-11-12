"""画量子线路图的公用工具。"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle


class Circuit:
    def __init__(self, ax, n_qubits, n_cols, labels=None, x0=0.0, y_top=None):
        self.ax = ax
        self.n = n_qubits
        self.cols = n_cols
        self.x0 = x0
        self.dx = 1.25
        self.y = [-(i) for i in range(n_qubits)]
        if labels is None:
            labels = [f"$q_{i}$" for i in range(n_qubits)]
        self.labels = labels
        ax.set_xlim(x0 - 1.25, x0 + n_cols * self.dx + 0.5)
        ax.set_ylim(min(self.y) - 0.62, max(self.y) + 0.62)
        ax.axis("off")
        for i, yy in enumerate(self.y):
            ax.plot([x0, x0 + (n_cols - 0.35) * self.dx], [yy, yy], color="#5c6b7a", lw=1.0)
            ax.text(x0 - 0.42, yy, labels[i], fontsize=8.6, color="#33414f", ha="right", va="center")

    def x(self, col):
        return self.x0 + col * self.dx

    def gate(self, col, qubit, label, width=0.66, height=0.66, color="#e8f0f8", edge="#4a6f9c"):
        x = self.x(col)
        y = self.y[qubit]
        self.ax.add_patch(Rectangle((x - width / 2, y - height / 2), width, height,
                                    facecolor=color, edgecolor=edge, lw=1.0, zorder=3))
        self.ax.text(x, y, label, fontsize=8.6, color="#1f2a37", ha="center", va="center", zorder=4)

    def cnot(self, col, control, target):
        x = self.x(col)
        yc, yt = self.y[control], self.y[target]
        self.ax.plot([x, x], [yc, yt], color="#4a6f9c", lw=1.1, zorder=3)
        self.ax.plot([x], [yc], "o", ms=5.0, color="#4a6f9c", zorder=4)
        self.ax.add_patch(Circle((x, yt), 0.155, facecolor="white", edgecolor="#4a6f9c", lw=1.1, zorder=4))
        self.ax.plot([x - 0.155, x + 0.155], [yt, yt], color="#4a6f9c", lw=1.1, zorder=5)
        self.ax.plot([x, x], [yt - 0.155, yt + 0.155], color="#4a6f9c", lw=1.1, zorder=5)

    def cz(self, col, a, b):
        x = self.x(col)
        for q in (a, b):
            self.ax.plot([x], [self.y[q]], "o", ms=5.0, color="#4a6f9c", zorder=4)
        self.ax.plot([x, x], [self.y[a], self.y[b]], color="#4a6f9c", lw=1.1, zorder=3)

    def swap(self, col, a, b):
        x = self.x(col)
        for q in (a, b):
            self.ax.plot([x - 0.11, x + 0.11], [self.y[q] - 0.11, self.y[q] + 0.11], color="#4a6f9c", lw=1.3)
            self.ax.plot([x - 0.11, x + 0.11], [self.y[q] + 0.11, self.y[q] - 0.11], color="#4a6f9c", lw=1.3)
        self.ax.plot([x, x], [self.y[a], self.y[b]], color="#4a6f9c", lw=1.0, zorder=2)

    def measure(self, col, qubit, width=0.66):
        x = self.x(col)
        y = self.y[qubit]
        self.ax.add_patch(Rectangle((x - width / 2, y - 0.28), width, 0.56,
                                    facecolor="#f4f1e8", edgecolor="#8a7a55", lw=1.0, zorder=3))
        self.ax.text(x, y, "M", fontsize=8.4, color="#5a4a2a", ha="center", va="center", zorder=4)

    def barrier(self, col):
        x = self.x(col)
        y0, y1 = min(self.y) - 0.42, max(self.y) + 0.42
        self.ax.plot([x, x], [y0, y1], color="#b9c3cf", lw=0.9, ls=(0, (3, 3)))

    def annotate(self, col, text, dy=0.45, qubit=0):
        x = self.x(col)
        self.ax.text(x, self.y[qubit] + dy, text, fontsize=7.6, color="#6b7785", ha="center", va="bottom")

    def multi(self, col, q_from, q_to, label, width=0.9, color="#eef3ee", edge="#5f7d5f", rotate=0):
        x = self.x(col)
        y1, y2 = self.y[q_from], self.y[q_to]
        top, bot = max(y1, y2), min(y1, y2)
        self.ax.add_patch(Rectangle((x - width / 2, bot - 0.34), width, (top - bot) + 0.68,
                                    facecolor=color, edgecolor=edge, lw=1.0, zorder=3))
        self.ax.text(x, (top + bot) / 2, label, fontsize=8.4, color="#1f2a37",
                     ha="center", va="center", zorder=4, rotation=rotate)

    def cphase(self, col, control, target, label, size=0.42):
        x = self.x(col)
        yc, yt = self.y[control], self.y[target]
        self.ax.plot([x, x], [yc, yt], color="#4a6f9c", lw=1.0, zorder=2)
        self.ax.plot([x], [yc], "o", ms=4.4, color="#4a6f9c", zorder=3)
        self.ax.add_patch(Rectangle((x - size / 2, yt - size / 2), size, size,
                                    facecolor="#e8f0f8", edgecolor="#4a6f9c", lw=0.9, zorder=3))
        self.ax.text(x, yt, label, fontsize=6.6, color="#1f2a37", ha="center", va="center", zorder=4)

    def controls(self, col, q_controls, q_target):
        x = self.x(col)
        ys = [self.y[q] for q in q_controls] + [self.y[q_target]]
        self.ax.plot([x, x], [min(ys), max(ys)], color="#4a6f9c", lw=1.1, zorder=3)
        for q in q_controls:
            self.ax.plot([x], [self.y[q]], "o", ms=5.0, color="#4a6f9c", zorder=4)
        yt = self.y[q_target]
        self.ax.add_patch(Circle((x, yt), 0.155, facecolor="white", edgecolor="#4a6f9c", lw=1.1, zorder=4))
        self.ax.plot([x - 0.155, x + 0.155], [yt, yt], color="#4a6f9c", lw=1.1, zorder=5)
        self.ax.plot([x, x], [yt - 0.155, yt + 0.155], color="#4a6f9c", lw=1.1, zorder=5)
