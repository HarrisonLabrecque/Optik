
"""
Optik — Plot Manager
Version: 0.2.0

Reusable Matplotlib plotting system for PySide6.

Features:
    - Embedded Matplotlib canvas
    - Navigation toolbar
    - Light and dark themes
    - Figure and axes management
    - Plot refreshing and clearing
    - Figure export (PNG, JPG, SVG, PDF)
    - Integration with existing ray diagram classes
"""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
)

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)


class PlotManager(QWidget):
    """
    Reusable Matplotlib plot widget for Optik.
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        figsize: tuple[float, float] = (8, 5),
        dpi: int = 100,
        show_toolbar: bool = True,
        theme: str = "dark",
    ) -> None:
        super().__init__(parent)

        self.figsize = figsize
        self.dpi = dpi
        self.show_toolbar = show_toolbar
        self.theme = theme.lower()

        self.figure = Figure(
            figsize=self.figsize,
            dpi=self.dpi,
        )

        self.ax: Axes = self.figure.add_subplot(111)

        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(
            self.canvas,
            self,
        )

        self._setup_ui()
        self.apply_theme(self.theme)

    # ============================================================
    # USER INTERFACE
    # ============================================================

    def _setup_ui(self) -> None:
        """Configure the widget layout."""

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        if self.show_toolbar:
            self.layout.addWidget(self.toolbar)
        else:
            self.toolbar.hide()

        self.layout.addWidget(self.canvas)

    # ============================================================
    # FIGURE MANAGEMENT
    # ============================================================

    def set_figure(self, figure: Figure) -> None:
        """
        Display an existing Matplotlib figure.

        Recreates the canvas and toolbar only when the
        incoming figure differs from the current figure.
        """

        if not isinstance(figure, Figure):
            raise TypeError(
                "Expected a matplotlib.figure.Figure."
            )

        if figure is self.figure:
            self.ax = (
                figure.axes[0]
                if figure.axes
                else figure.add_subplot(111)
            )
            self.refresh()
            return

        old_canvas = self.canvas
        old_toolbar = self.toolbar

        # Remove old widgets from the layout.
        self.layout.removeWidget(old_canvas)

        if self.show_toolbar:
            self.layout.removeWidget(old_toolbar)

        # Detach old widgets.
        old_canvas.setParent(None)
        old_toolbar.setParent(None)

        # Assign the new figure.
        self.figure = figure

        if self.figure.axes:
            self.ax = self.figure.axes[0]
        else:
            self.ax = self.figure.add_subplot(111)

        # Create a new canvas for the incoming figure.
        self.canvas = FigureCanvas(self.figure)

        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        # Recreate the navigation toolbar for the new canvas.
        self.toolbar = NavigationToolbar(
            self.canvas,
            self,
        )

        if self.show_toolbar:
            self.layout.insertWidget(0, self.toolbar)
        else:
            self.toolbar.hide()

        self.layout.addWidget(self.canvas)

        # Clean up old Qt widgets.
        old_canvas.deleteLater()
        old_toolbar.deleteLater()

        self.apply_theme(self.theme)
        self.refresh()

    def get_figure(self) -> Figure:
        """Return the current figure."""
        return self.figure

    def get_axes(self) -> Axes:
        """Return the primary axes."""
        return self.ax

    # ============================================================
    # REFRESHING
    # ============================================================

    def refresh(self) -> None:
        """Schedule a redraw."""
        self.canvas.draw_idle()

    def draw(self) -> None:
        """Render immediately."""
        self.canvas.draw()

    # ============================================================
    # CLEARING
    # ============================================================

    def clear(self) -> None:
        """Clear the current axes."""
        self.ax.clear()
        self.apply_theme(self.theme)

    def clear_figure(self) -> None:
        """Clear the figure and recreate its axes."""
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.apply_theme(self.theme)

    # ============================================================
    # THEMES
    # ============================================================

    def apply_theme(self, theme: str) -> None:
        """
        Apply a light or dark plotting theme.
        """

        theme = theme.lower()

        if theme not in ("light", "dark"):
            raise ValueError(
                "Theme must be 'light' or 'dark'."
            )

        self.theme = theme

        if theme == "dark":
            background = "#182338"
            foreground = "#f8fafc"
            grid_color = "#475569"
            spine_color = "#64748b"
        else:
            background = "#ffffff"
            foreground = "#0f172a"
            grid_color = "#cbd5e1"
            spine_color = "#94a3b8"

        self.figure.set_facecolor(background)

        for ax in self.figure.axes:
            ax.set_facecolor(background)

            ax.tick_params(colors=foreground)

            ax.xaxis.label.set_color(foreground)
            ax.yaxis.label.set_color(foreground)
            ax.title.set_color(foreground)

            for spine in ax.spines.values():
                spine.set_color(spine_color)

            ax.grid(
                True,
                color=grid_color,
                linestyle=":",
                alpha=0.4,
            )

        self.refresh()

    # ============================================================
    # AXIS CONFIGURATION
    # ============================================================

    def set_title(self, title: str) -> None:
        """Set the plot title."""
        self.ax.set_title(title)
        self.refresh()

    def set_labels(
        self,
        xlabel: str,
        ylabel: str,
    ) -> None:
        """Set the axis labels."""
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.refresh()

    def set_limits(
        self,
        xmin: float,
        xmax: float,
        ymin: float,
        ymax: float,
    ) -> None:
        """Set the axis limits."""

        if xmin >= xmax:
            raise ValueError(
                "xmin must be smaller than xmax."
            )

        if ymin >= ymax:
            raise ValueError(
                "ymin must be smaller than ymax."
            )

        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)
        self.refresh()

    def set_grid(self, enabled: bool = True) -> None:
        """Enable or disable the grid."""
        self.ax.grid(enabled)
        self.refresh()

    # ============================================================
    # PLOTTING HELPERS
    # ============================================================

    def plot_line(
        self,
        x,
        y,
        label: Optional[str] = None,
        color: Optional[str] = None,
        linewidth: float = 2.0,
    ) -> None:
        """Draw a line plot."""

        self.ax.plot(
            x,
            y,
            label=label,
            color=color,
            linewidth=linewidth,
        )

        if label:
            self.ax.legend()

        self.refresh()

    def plot_scatter(
        self,
        x,
        y,
        label: Optional[str] = None,
        color: Optional[str] = None,
        size: float = 30,
    ) -> None:
        """Draw a scatter plot."""

        self.ax.scatter(
            x,
            y,
            label=label,
            color=color,
            s=size,
        )

        if label:
            self.ax.legend()

        self.refresh()

    # ============================================================
    # DIAGRAM INTEGRATION
    # ============================================================

    def display_diagram(self, diagram) -> None:
        """
        Display a diagram containing a Matplotlib figure.

        Compatible with LensDiagram and other
        Matplotlib-based diagram classes.
        """

        if not hasattr(diagram, "figure"):
            raise TypeError(
                "Diagram must contain a 'figure' attribute."
            )

        self.set_figure(diagram.figure)

        # Diagram drawing may reset axis styling.
        self.apply_theme(self.theme)

    # ============================================================
    # EXPORT
    # ============================================================

    def save_plot(
        self,
        filename: str,
        dpi: int = 150,
    ) -> Path:
        """
        Export the current figure.

        Supported:
            PNG, JPG, JPEG, SVG, PDF
        """

        path = Path(filename)

        supported_formats = {
            ".png",
            ".jpg",
            ".jpeg",
            ".svg",
            ".pdf",
        }

        if path.suffix.lower() not in supported_formats:
            raise ValueError(
                "Unsupported image format."
            )

        if dpi <= 0:
            raise ValueError(
                "DPI must be greater than zero."
            )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.figure.savefig(
            path,
            dpi=dpi,
            bbox_inches="tight",
            facecolor=self.figure.get_facecolor(),
        )

        return path

    # ============================================================
    # RESET
    # ============================================================

    def reset(self) -> None:
        """Reset the plot while preserving its theme."""

        self.clear_figure()

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")

        self.refresh()


# ============================================================
# STANDALONE DEMONSTRATION
# ============================================================

if __name__ == "__main__":

    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = PlotManager(
        figsize=(9, 6),
        theme="dark",
    )

    window.setWindowTitle(
        "Optik — Plot Manager"
    )

    window.plot_line(
        x=[0, 1, 2, 3, 4],
        y=[0, 1, 4, 9, 16],
        label="Example Plot",
    )

    window.set_title(
        "Optik Plot Manager Demonstration"
    )

    window.set_labels("X", "Y")

    window.resize(900, 600)
    window.show()

    sys.exit(app.exec())
