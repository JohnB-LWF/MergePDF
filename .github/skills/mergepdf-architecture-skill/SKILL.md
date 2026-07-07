---
name: mergepdf-architecture-skill
description: "Use when working in the MergePDF repository to enforce architecture boundaries, coding standards, Streamlit theming rules, and feature implementation workflow. Triggers: merge pdf logic changes, GUI updates, CLI updates, controller wiring, theme updates, and test planning. Do not use for unrelated repositories or generic Python questions outside this codebase."
user-invocable: false
---

# MergePDF Architecture Skill

This skill defines the rules and expectations that human contributors and AI agents must follow when working on this project.

## Agent Goal

Produce maintainable, modular changes while preserving a strict three-layer architecture:

1. Engine layer for pure PDF logic.
2. Interface layer for CLI and Streamlit GUI.
3. Controller bridge between GUI interactions and engine calls.

## Required Agent Behavior

1. Read the current file structure before adding modules.
2. Keep business logic in the engine layer.
3. Route GUI operations through the controller layer.
4. Reuse theme tokens for styling decisions.
5. Add or update tests for behavior changes.
6. Update README for user-visible feature changes.

## Tooling Guidance

1. Prefer small, focused edits over large refactors unless requested.
2. Preserve public interfaces unless the task requires breaking changes.
3. If architecture conflicts exist, propose a minimal migration path instead of duplicating logic.

## Scope

The project has three layers:

1. Core engine for PDF logic.
2. CLI interface for terminal use.
3. Streamlit GUI with a dark SOC-style aesthetic.

## Canonical Project Structure

```text
mergepdf/
├── mergepdf/                # Core library (pure logic)
│   ├── __init__.py
│   └── engine.py            # merge_pdfs(), validate_files(), etc.
├── cli/                     # CLI interface
│   └── main.py              # argparse, terminal UX
├── gui/                     # Streamlit GUI interface
│   ├── app.py               # layout and event flow
│   ├── controller.py        # bridge between GUI and engine
│   ├── components.py        # reusable UI components
│   └── theme.py             # dark SOC-style theme variables
├── tests/                   # Unit tests for core logic
│   └── test_engine.py
├── assets/                  # Icons, backgrounds, logos
│   └── logo.png
└── README.md
```

## Non-Negotiable Architecture Rules

1. Single source of truth: all PDF merge logic must live in `mergepdf/engine.py`.
2. No duplicate merge logic in `gui/` or `cli/`.
3. `gui/app.py` handles layout and user interaction flow only.
4. `gui/controller.py` translates GUI actions into engine calls.
5. `gui/components.py` contains reusable UI blocks only.
6. `gui/theme.py` defines styling tokens and theme values only.
7. No business logic inside Streamlit callbacks.
8. No UI code in the engine layer.
9. No inline styling constants in components when a theme token should be used.

## File Boundary Contract

1. `mergepdf/engine.py`: pure logic, validation, merge and PDF processing helpers.
2. `cli/main.py`: argument parsing and terminal UX; delegates work to engine.
3. `gui/app.py`: layout composition and event wiring only.
4. `gui/controller.py`: GUI-to-engine orchestration and error translation.
5. `gui/components.py`: reusable UI elements only; no business logic.
6. `gui/theme.py`: style tokens and theme configuration only.
7. `tests/`: behavior-focused tests for engine and integration boundaries.

## Coding Standards

### General

1. Use type hints throughout.
2. Write readable functions with concise docstrings.
3. Prefer pure functions in the engine layer.
4. Limit side effects to necessary file I/O boundaries.

### CLI

1. Use `argparse`.
2. Call the same engine functions used by the GUI.

### GUI (Streamlit)

1. Keep `app.py` minimal and orchestration-focused.
2. Build UI blocks in `components.py`.
3. Execute merge operations through `controller.py`.
4. Define or reuse style tokens in `theme.py`.

### Testing

At minimum, tests must cover:

1. File validation.
2. Merge ordering.
3. Error handling.
4. Output correctness.

## Theme Contract (SOC-Lab Aesthetic)

Use these tokens consistently:

1. Background: `#0D0F12`
2. Panels: `#111418`
3. Accent: `#00E0FF`
4. Soft accent: `#0099B8`
5. Text primary: `#E8E8E8`
6. Text secondary: `#9AA0A6`

UI direction:

1. Monospaced typography only (for example: JetBrains Mono, Fira Code, Hack).
2. Minimal, terminal-inspired, cold-tone visual style.
3. No rounded corners.
4. Subtle gridlines are allowed.
5. Buttons should have a slight glow on hover.

## AI Agent Responsibilities

AI agents must:

1. Preserve architecture boundaries.
2. Import merge logic from `mergepdf.engine` instead of reimplementing it.
3. Keep new GUI features modular by updating the right files.
4. Use theme variables rather than hardcoded visual values.
5. Prefer clarity over clever abstractions.
6. Suggest refactors and improvements only when they do not violate architecture.

## Decision Rules

When implementing a request, use these decisions:

1. If it changes PDF behavior, edit engine first.
2. If it changes GUI behavior, add or update controller wiring.
3. If it changes presentation only, keep changes in components and theme.
4. If CLI and GUI need the same behavior, expose one engine function and call it from both.
5. If a new style value is introduced repeatedly, promote it to a theme token.

## Feature Implementation Workflow (Required)

When adding a GUI feature (for example, rotate/split/compress):

1. Update `mergepdf/engine.py` with pure core logic.
2. Update `gui/controller.py` with a wrapper/orchestration function.
3. Update `gui/components.py` with reusable UI elements.
4. Update `gui/app.py` to wire event flow.
5. Update `gui/theme.py` only if new style tokens are necessary.
6. Add or update tests in `tests/`.
7. Document user-facing behavior in `README.md`.

## Validation Checklist For Agents

Before finalizing, verify all items:

1. No merge logic was added to `gui/` or `cli/`.
2. Streamlit callbacks do not contain business logic.
3. New UI code uses theme values.
4. Existing workflows were not broken.
5. Tests were added or updated for changed behavior.
6. Error paths are handled with clear messages.
7. README reflects user-visible changes.

## Contribution Checklist

Before considering work complete, verify:

1. Architecture rules are respected.
2. No duplicated business logic exists across layers.
3. Tests pass and include meaningful coverage for new behavior.
4. README is updated for user-visible changes.
5. New modules include docstrings.

## Planned Extension Areas

The architecture is designed to support:

1. PDF splitting.
2. PDF compression.
3. PDF metadata editing.
4. Multi-page GUI flows.
5. Desktop packaging (Streamlit App Mode).

Any expansion must follow all rules in this file.
