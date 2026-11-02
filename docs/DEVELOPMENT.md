# Optik — Development Guide

**Version:** 0.1.0  
**Project:** Optik  
**Language:** Python  
**GUI Framework:** PySide6  
**License:** MIT  
**Development Status:** Initial Release Candidate

---

## 1. Introduction

Optik is an open-source desktop application for optics and photonics calculations and visualization.

The project is developed using Python and PySide6, with Matplotlib providing graphical representations of optical ray behavior.

This guide describes the development environment, project structure, architecture, testing procedures, and contribution workflow.

## 2. Development Environment

### 2.1 Recommended Tools

- Python 3.14 or a compatible Python 3 version
- Visual Studio Code or another Python-compatible IDE
- Git
- GitHub
- Windows PowerShell or another supported terminal

### 2.2 Python Dependencies

The primary development dependencies include:

| Package | Purpose |
|---|---|
| PySide6 | Desktop graphical interface |
| NumPy | Numerical computation |
| SciPy | Scientific computing |
| Matplotlib | Optical ray visualization |
| pytest | Automated testing |
| pytest-qt | Qt GUI testing |

The initial optical calculation modules primarily use Python's built-in `math` library.

## 3. Setting Up the Development Environment

### 3.1 Clone the Repository

```bash
git clone <repository-url>
cd Optik
```

Replace `<repository-url>` with the actual Optik repository address.

### 3.2 Create a Virtual Environment

```powershell
python -m venv .venv
```

### 3.3 Activate the Environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3.4 Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Install the testing dependencies if they are not already included:

```bash
python -m pip install pytest pytest-qt
```

### 3.5 Launch the Application

```bash
python main.py
```

The Optik desktop interface should open.

## 4. Project Architecture

Optik follows a modular architecture that separates the user interface, optical calculations, and visualization components.

```text
Optik/
│
├── main.py
├── pyproject.toml
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
│
├── app/
│   ├── __init__.py
│   ├── main_window.py
│   └── config.py
│
├── ui/
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── home_page.py
│   │   ├── reflection_page.py
│   │   ├── refraction_page.py
│   │   └── settings_page.py
│   │
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── sidebar.py
│   │   ├── metric_card.py
│   │   └── input_panel.py
│   │
│   └── styles/
│       └── main.qss
│
├── optics/
│   ├── __init__.py
│   ├── reflection.py
│   ├── refraction.py
│   ├── snells_law.py
│   └── total_internal_reflection.py
│
├── visualization/
│   ├── __init__.py
│   ├── ray_diagram.py
│   └── plot_manager.py
│
├── utils/
│   ├── __init__.py
│   ├── validators.py
│   └── constants.py
│
├── tests/
│   ├── __init__.py
│   ├── test_reflection.py
│   ├── test_refraction.py
│   ├── test_snells_law.py
│   ├── test_total_internal_reflection.py
│   ├── test_main_window.py
│   ├── test_reflection_page.py
│   ├── test_refraction_page.py
│   └── test_ray_diagram.py
│
└── docs/
    ├── SRS.md
    ├── SDD.md
    ├── USER_GUIDE.md
    └── DEVELOPMENT.md
```

Some files are placeholders for future functionality.

## 5. Application Components

### 5.1 Application Entry Point

**File:** `main.py`

Responsibilities:

- Initialize `QApplication`.
- Configure application metadata.
- Load the application stylesheet.
- Initialize the main window.
- Start the Qt event loop.

### 5.2 Main Window

**File:** `app/main_window.py`

The `MainWindow` class manages the main application interface.

It provides:

- Sidebar navigation
- Page initialization
- Page switching
- Main application layout

The implementation uses `QMainWindow` and `QStackedWidget`.

### 5.3 User Interface Pages

The `ui/pages/` directory contains the main application pages.

**Home Page**

Provides the application's landing interface.

**Reflection Page**

Accepts incident angles, calculates reflected angles, and displays optical ray diagrams.

**Refraction Page**

Calculates refracted angles, critical angles, and