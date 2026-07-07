# MergePDF

A lightweight command-line tool for merging PDF files using Python and `pypdf`.

`MergePDF` supports three common workflows:

- Merge specific PDF files in the order you provide.
- Merge all PDF files found in a directory (sorted by filename).
- Extract a page range from a single PDF into a new output PDF.

## Features

- Simple CLI with subcommands.
- Uses modern `pypdf` APIs (`PdfReader`, `PdfWriter`).
- Verbose mode for progress output.
- Basic validation and clear error messages.

## Requirements

- Python 3.8+
- Dependency listed in [requirements.txt](requirements.txt):
	- `pypdf>=6.14.2,<7.0.0`

## Installation

1. Clone this repository:

```bash
git clone https://github.com/JohnB-LWF/MergePDF.git
cd MergePDF
```

2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

Show help:

```bash
python mergePDF.py --help
```

Merge multiple files:

```bash
python mergePDF.py files -o combined.pdf -i a.pdf b.pdf c.pdf
```

Merge all PDFs in a folder:

```bash
python mergePDF.py dir -o merged.pdf -d ./reports/
```

Extract pages from a PDF:

```bash
python mergePDF.py pages -o extract.pdf -p big.pdf -s 0 -e 4
```

## Command Reference

### Global Structure

```bash
python mergePDF.py <command> [options]
```

Available commands:

- `files` - Merge specific input PDF files.
- `dir` - Merge all `.pdf` files in a directory.
- `pages` - Extract a page range from one PDF.

### `files` Command

Merge specific PDF files in the exact order provided.

```bash
python mergePDF.py files -o <output.pdf> -i <input1.pdf> <input2.pdf> [...] [-v]
```

Options:

- `-o, --output` (required): Output PDF file path.
- `-i, --inputs` (required): One or more input PDF files.
- `-v, --verbose` (optional): Print progress messages.

Example:

```bash
python mergePDF.py files -o final.pdf -i intro.pdf chapter1.pdf chapter2.pdf -v
```

### `dir` Command

Merge all `.pdf` files in a directory. Files are sorted alphabetically before merging.

```bash
python mergePDF.py dir -o <output.pdf> -d <directory> [-v]
```

Options:

- `-o, --output` (required): Output PDF file path.
- `-d, --directory` (required): Directory containing PDF files.
- `-v, --verbose` (optional): Print progress messages.

Example:

```bash
python mergePDF.py dir -o monthly-report.pdf -d ./monthly-pdfs -v
```

### `pages` Command

Extract a page range from a single PDF into a new output file.

```bash
python mergePDF.py pages -o <output.pdf> -p <input.pdf> -s <start> -e <end> [-v]
```

Options:

- `-o, --output` (required): Output PDF file path.
- `-p, --pdf` (required): Source PDF file.
- `-s, --start` (required): Start page index (0-based, inclusive).
- `-e, --end` (required): End page index (0-based, exclusive).
- `-v, --verbose` (optional): Print progress messages.

Example:

```bash
python mergePDF.py pages -o chapter-extract.pdf -p full-book.pdf -s 10 -e 25 -v
```

## Page Indexing Notes

The `pages` command uses zero-based indexing and an exclusive end bound:

- `-s 0 -e 1` extracts only page 1 (human-readable).
- `-s 0 -e 4` extracts pages 1 through 4.

This follows Python slicing semantics: `range(start, end)`.

## Error Handling

The script exits with a non-zero status (`exit code 1`) for failures such as:

- An input PDF cannot be opened/read.
- A directory path is invalid or inaccessible.
- No PDFs are found in a directory for the `dir` command.
- An invalid page range is provided for the `pages` command.

## Common Tips

- Quote file paths that contain spaces.
- In `files` mode, input order determines output order.
- In `dir` mode, file order is alphabetical.
- Use `-v` while debugging to see exactly what is being processed.

## Project Files

- [mergePDF.py](mergePDF.py) - Main CLI script.
- [requirements.txt](requirements.txt) - Python dependencies.

## License

This project is licensed under the MIT License.
