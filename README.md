# MergePDF

MergePDF is a modular PDF utility with both a CLI and a Streamlit GUI.

## Use it Now

You can use the app right now on the Streamlit website [here](https://mpdfapp.streamlit.app/)!

## Architecture

```text
MergePDF/
├── mergepdf/          # Core engine (pure PDF logic)
│   ├── __init__.py
│   └── engine.py
├── cli/               # CLI interface
│   └── main.py
├── gui/               # Streamlit GUI
│   ├── app.py
│   ├── controller.py
│   ├── components.py
│   └── theme.py
├── tests/
│   └── test_engine.py
└── mergePDF.py        # Backward-compatible CLI launcher
```

The engine (`mergepdf/engine.py`) is the single source of truth for merge behavior.  
CLI and GUI both delegate to the engine.

## Requirements

- Python 3.8+
- Dependencies in `requirements.txt`:
  - `pypdf>=6.14.2,<7.0.0`
  - `streamlit>=1.37.0,<2.0.0`

## Installation

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## CLI Usage

Show help:

```powershell
python mergePDF.py --help
```

Merge specific files:

```powershell
python mergePDF.py files -o combined.pdf -i a.pdf b.pdf c.pdf
```

Merge all PDFs in a directory:

```powershell
python mergePDF.py dir -o merged.pdf -d .\reports
```

Extract page range:

```powershell
python mergePDF.py pages -o extract.pdf -p big.pdf -s 0 -e 4
```

## Streamlit GUI

Run the GUI:

```powershell
streamlit run gui/app.py
```

GUI features:

- Drag-and-drop multi-file PDF uploader.
- SOC-style terminal console with merge progress.
- Neon-accent merge action.
- Download button for merged output.

## Tests

Run tests:

```powershell
python -m unittest discover -s tests -v
```

Current tests cover:

- File validation
- Directory ordering
- Merge ordering
- Page extraction correctness
- Error handling for invalid PDF content

## Agent Skill

This repository includes a Copilot architecture skill:

- `.github/skills/mergepdf-architecture-skill/SKILL.md`

Use it to preserve engine/controller/interface boundaries and theme consistency.
