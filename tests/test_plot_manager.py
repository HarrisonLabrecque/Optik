
"""
Optik — Plot Manager Tests
Version: 0.2.0

Tests:
    - Widget initialization
    - Matplotlib figure and axes
    - Navigation toolbar
    - Figure replacement
    - Canvas reuse
    - Light and dark themes
    - Axis configuration
    - Line and scatter plotting
    - Plot clearing and resetting
    - Diagram integration
    - Figure export
    - Invalid inputs

Requirements:
    pytest
    pytest-qt
    matplotlib
    PySide6
"""

from pathlib import Path
from types import SimpleNamespace

import pytest

from matplotlib.figure import Figure
from matplotlib.axes import Axes

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)

from visualization.plot_manager import PlotManager


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def plot_manager(qtbot):
    """Create a PlotManager for each test."""

    widget = PlotManager(
        figsize=(8, 5),
        dpi=100,
        show_toolbar=True,
        theme="dark",
    )

    qtbot.addWidget(widget)

    return widget


@pytest.fixture
def light_plot_manager(qtbot):
    """Create a PlotManager using the light theme."""

    widget = PlotManager(
        theme="light",
    )

    qtbot.addWidget(widget)

    return widget


@pytest.fixture
def sample_figure():
    """Create an independent Matplotlib figure."""

    figure = Figure(figsize=(6, 4))
    figure.add_subplot(111)

    return figure


# ============================================================
# INITIALIZATION TESTS
# ============================================================

def test_plot_manager_is_widget(plot_manager):
    assert plot_manager is not None


def test_initial_figure(plot_manager):
    assert isinstance(
        plot_manager.figure,
        Figure,
    )


def test_initial_axes(plot_manager):
    assert isinstance(
        plot_manager.ax,
        Axes,
    )


def test_initial_canvas(plot_manager):
    assert isinstance(
        plot_manager.canvas,
        FigureCanvas,
    )


def test_initial_toolbar(plot_manager):
    assert isinstance(
        plot_manager.toolbar,
        NavigationToolbar,
    )


def test_initial_theme(plot_manager):
    assert plot_manager.theme == "dark"


def test_initial_figsize(plot_manager):
    assert plot_manager.figsize == (8, 5)


def test_initial_dpi(plot_manager):
    assert plot_manager.dpi == 100


def test_get_figure(plot_manager):
    assert plot_manager.get_figure() is plot_manager.figure


def test_get_axes(plot_manager):
    assert plot_manager.get_axes() is plot_manager.ax


def test_toolbar_visible_configuration(plot_manager):
    assert plot_manager.show_toolbar is True
    assert plot_manager.layout.indexOf(
        plot_manager.toolbar
    ) != -1


def test_toolbar_hidden_configuration(qtbot):
    widget = PlotManager(show_toolbar=False)
    qtbot.addWidget(widget)

    assert widget.show_toolbar is False
    assert widget.layout.indexOf(widget.toolbar) == -1
    assert widget.toolbar.isHidden()


# ============================================================
# FIGURE MANAGEMENT TESTS
# ============================================================

def test_set_figure(plot_manager, sample_figure):
    plot_manager.set_figure(sample_figure)

    assert plot_manager.figure is sample_figure


def test_set_figure_updates_axes(plot_manager, sample_figure):
    expected_axes = sample_figure.axes[0]

    plot_manager.set_figure(sample_figure)

    assert plot_manager.ax is expected_axes


def test_set_figure_creates_canvas(plot_manager, sample_figure):
    old_canvas = plot_manager.canvas

    plot_manager.set_figure(sample_figure)

    assert plot_manager.canvas is not old_canvas
    assert plot_manager.canvas.figure is sample_figure


def test_set_figure_recreates_toolbar(plot_manager, sample_figure):
    old_toolbar = plot_manager.toolbar

    plot_manager.set_figure(sample_figure)

    assert plot_manager.toolbar is not old_toolbar
    assert plot_manager.toolbar.canvas is plot_manager.canvas


def test_set_figure_updates_layout(plot_manager, sample_figure):
    plot_manager.set_figure(sample_figure)

    assert plot_manager.layout.indexOf(
        plot_manager.canvas
    ) != -1

    assert plot_manager.layout.indexOf(
        plot_manager.toolbar
    ) != -1


def test_set_same_figure_reuses_canvas(plot_manager):
    original_canvas = plot_manager.canvas

    plot_manager.set_figure(plot_manager.figure)

    assert plot_manager.canvas is original_canvas


def test_set_same_figure_reuses_toolbar(plot_manager):
    original_toolbar = plot_manager.toolbar

    plot_manager.set_figure(plot_manager.figure)

    assert plot_manager.toolbar is original_toolbar


def test_set_figure_without_axes(plot_manager):
    figure = Figure()

    plot_manager.set_figure(figure)

    assert len(plot_manager.figure.axes) == 1
    assert isinstance(plot_manager.ax, Axes)


@pytest.mark.parametrize(
    "invalid_figure",
    [
        None,
        123,
        "not a figure",
        [],
        {},
    ],
)
def test_set_figure_invalid_type(
    plot_manager,
    invalid_figure,
):
    with pytest.raises(TypeError):
        plot_manager.set_figure(invalid_figure)


def test_multiple_figure_replacements(plot_manager):
    for _ in range(3):
        figure = Figure()
        figure.add_subplot(111)

        plot_manager.set_figure(figure)

        assert plot_manager.canvas.figure is figure
        assert plot_manager.toolbar.canvas is plot_manager.canvas


# ============================================================
# THEME TESTS
# ============================================================

def test_dark_theme(plot_manager):
    plot_manager.apply_theme("dark")

    assert plot_manager.theme == "dark"
    assert plot_manager.figure.get_facecolor() is not None


def test_light_theme(light_plot_manager):
    assert light_plot_manager.theme == "light"
    assert light_plot_manager.figure.get_facecolor() is not None


def test_switch_to_light_theme(plot_manager):
    plot_manager.apply_theme("light")

    assert plot_manager.theme == "light"


def test_switch_to_dark_theme(light_plot_manager):
    light_plot_manager.apply_theme("dark")

    assert light_plot_manager.theme == "dark"


def test_theme_case_insensitive(plot_manager):
    plot_manager.apply_theme("LIGHT")

    assert plot_manager.theme == "light"


@pytest.mark.parametrize(
    "invalid_theme",
    [
        "blue",
        "system",
        "automatic",
        "",
    ],
)
def test_invalid_theme(plot_manager, invalid_theme):
    with pytest.raises(ValueError):
        plot_manager.apply_theme(invalid_theme)


def test_theme_preserved_after_figure_change(
    plot_manager,
    sample_figure,
):
    plot_manager.apply_theme("light")

    plot_manager.set_figure(sample_figure)

    assert plot_manager.theme == "light"


def test_theme_preserved_after_clear(plot_manager):
    plot_manager.apply_theme("light")

    plot_manager.clear()

    assert plot_manager.theme == "light"


# ============================================================
# AXIS CONFIGURATION TESTS
# ============================================================

def test_set_title(plot_manager):
    plot_manager.set_title("Test Plot")

    assert plot_manager.ax.get_title() == "Test Plot"


def test_set_labels(plot_manager):
    plot_manager.set_labels(
        "Distance",
        "Intensity",
    )

    assert plot_manager.ax.get_xlabel() == "Distance"
    assert plot_manager.ax.get_ylabel() == "Intensity"


def test_set_limits(plot_manager):
    plot_manager.set_limits(
        -10,
        10,
        -5,
        5,
    )

    assert plot_manager.ax.get_xlim() == (-10, 10)
    assert plot_manager.ax.get_ylim() == (-5, 5)


def test_invalid_x_limits(plot_manager):
    with pytest.raises(ValueError):
        plot_manager.set_limits(
            10,
            0,
            -5,
            5,
        )


def test_invalid_y_limits(plot_manager):
    with pytest.raises(ValueError):
        plot_manager.set_limits(
            -10,
            10,
            5,
            -5,
        )


def test_enable_grid(plot_manager):
    plot_manager.set_grid(True)

    assert all(
        line.get_visible()
        for line in plot_manager.ax.get_xgridlines()
    )


def test_disable_grid(plot_manager):
    plot_manager.set_grid(False)

    assert not any(
        line.get_visible()
        for line in plot_manager.ax.get_xgridlines()
    )


# ============================================================
# PLOTTING TESTS
# ============================================================

def test_plot_line(plot_manager):
    plot_manager.plot_line(
        [0, 1, 2],
        [0, 1, 4],
    )

    assert len(plot_manager.ax.lines) == 1


def test_plot_line_data(plot_manager):
    plot_manager.plot_line(
        [0, 1, 2],
        [0, 1, 4],
    )

    line = plot_manager.ax.lines[0]

    assert list(line.get_xdata()) == [0, 1, 2]
    assert list(line.get_ydata()) == [0, 1, 4]


def test_plot_line_label(plot_manager):
    plot_manager.plot_line(
        [0, 1],
        [1, 2],
        label="Test Line",
    )

    assert plot_manager.ax.get_legend() is not None


def test_plot_line_color(plot_manager):
    plot_manager.plot_line(
        [0, 1],
        [1, 2],
        color="red",
    )

    assert plot_manager.ax.lines[0].get_color() == "red"


def test_plot_scatter(plot_manager):
    plot_manager.plot_scatter(
        [0, 1, 2],
        [2, 3, 4],
    )

    assert len(plot_manager.ax.collections) == 1


def test_plot_scatter_label(plot_manager):
    plot_manager.plot_scatter(
        [0, 1],
        [1, 2],
        label="Points",
    )

    assert plot_manager.ax.get_legend() is not None


def test_plot_scatter_size(plot_manager):
    plot_manager.plot_scatter(
        [0, 1],
        [1, 2],
        size=50,
    )

    collection = plot_manager.ax.collections[0]

    assert all(
        size == 50
        for size in collection.get_sizes()
    )


# ============================================================
# CLEARING AND RESET TESTS
# ============================================================

def test_clear_axes(plot_manager):
    plot_manager.plot_line(
        [0, 1],
        [1, 2],
    )

    plot_manager.clear()

    assert len(plot_manager.ax.lines) == 0


def test_clear_figure(plot_manager):
    plot_manager.plot_line(
        [0, 1],
        [1, 2],
    )

    plot_manager.clear_figure()

    assert len(plot_manager.figure.axes) == 1
    assert len(plot_manager.ax.lines) == 0


def test_reset(plot_manager):
    plot_manager.plot_line(
        [0, 1],
        [1, 2],
    )

    plot_manager.reset()

    assert len(plot_manager.ax.lines) == 0
    assert plot_manager.ax.get_xlabel() == "X"
    assert plot_manager.ax.get_ylabel() == "Y"


# ============================================================
# DIAGRAM INTEGRATION TESTS
# ============================================================

def test_display_diagram(plot_manager, sample_figure):
    diagram = SimpleNamespace(
        figure=sample_figure
    )

    plot_manager.display_diagram(diagram)

    assert plot_manager.figure is sample_figure


def test_display_diagram_updates_canvas(
    plot_manager,
    sample_figure,
):
    diagram = SimpleNamespace(
        figure=sample_figure
    )

    plot_manager.display_diagram(diagram)

    assert plot_manager.canvas.figure is sample_figure


def test_display_diagram_invalid_object(plot_manager):
    with pytest.raises(TypeError):
        plot_manager.display_diagram(object())


def test_display_diagram_invalid_figure(plot_manager):
    diagram = SimpleNamespace(
        figure="not a figure"
    )

    with pytest.raises(TypeError):
        plot_manager.display_diagram(diagram)


# ============================================================
# EXPORT TESTS
# ============================================================

@pytest.mark.parametrize(
    "extension",
    [
        ".png",
        ".jpg",
        ".jpeg",
        ".svg",
        ".pdf",
    ],
)
def test_save_plot_supported_formats(
    plot_manager,
    tmp_path,
    extension,
):
    filename = tmp_path / f"test_plot{extension}"

    result = plot_manager.save_plot(
        str(filename)
    )

    assert isinstance(result, Path)
    assert result.exists()
    assert result.stat().st_size > 0


def test_save_plot_creates_directory(
    plot_manager,
    tmp_path,
):
    filename = (
        tmp_path
        / "nested"
        / "plots"
        / "figure.png"
    )

    plot_manager.save_plot(str(filename))

    assert filename.exists()


def test_save_plot_invalid_format(
    plot_manager,
    tmp_path,
):
    filename = tmp_path / "plot.txt"

    with pytest.raises(ValueError):
        plot_manager.save_plot(str(filename))


@pytest.mark.parametrize(
    "invalid_dpi",
    [
        0,
        -1,
        -100,
    ],
)
def test_save_plot_invalid_dpi(
    plot_manager,
    tmp_path,
    invalid_dpi,
):
    filename = tmp_path / "plot.png"

    with pytest.raises(ValueError):
        plot_manager.save_plot(
            str(filename),
            dpi=invalid_dpi,
        )


# ============================================================
# REFRESH TESTS
# ============================================================

def test_refresh(plot_manager):
    plot_manager.refresh()


def test_draw(plot_manager):
    plot_manager.draw()


def test_refresh_after_plot(plot_manager):
    plot_manager.plot_line(
        [0, 1, 2],
        [2, 4, 6],
    )

    plot_manager.draw()

    assert len(plot_manager.ax.lines) == 1
