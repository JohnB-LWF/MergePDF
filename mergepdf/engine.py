"""Core PDF processing functions for MergePDF."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError


class MergePDFError(Exception):
    """Base exception for mergePDF operations."""


class ValidationError(MergePDFError):
    """Raised when file inputs are invalid."""


class ProcessingError(MergePDFError):
    """Raised when PDF reading/writing fails."""


@dataclass(frozen=True)
class MergeSummary:
    """Summary of a merge operation."""

    output_path: Path
    files_merged: int
    pages_written: int


def validate_files(inputs: Sequence[str | Path]) -> list[Path]:
    """Validate input file paths and return normalized paths in original order."""
    if not inputs:
        raise ValidationError("No input PDFs were provided.")

    validated: list[Path] = []
    for raw_path in inputs:
        file_path = Path(raw_path).expanduser()

        if file_path.suffix.lower() != ".pdf":
            raise ValidationError(f"Input is not a PDF file: {file_path}")
        if not file_path.exists():
            raise ValidationError(f"Input file does not exist: {file_path}")
        if not file_path.is_file():
            raise ValidationError(f"Input path is not a file: {file_path}")

        validated.append(file_path)

    return validated


def get_pdf_files_in_directory(directory: str | Path) -> list[Path]:
    """Return sorted PDF files in a directory."""
    directory_path = Path(directory).expanduser()

    if not directory_path.exists():
        raise ValidationError(f"Directory does not exist: {directory_path}")
    if not directory_path.is_dir():
        raise ValidationError(f"Path is not a directory: {directory_path}")

    pdf_files = sorted(
        file_path for file_path in directory_path.iterdir() if file_path.is_file() and file_path.suffix.lower() == ".pdf"
    )
    if not pdf_files:
        raise ValidationError(f"No PDF files found in directory: {directory_path}")

    return pdf_files


def merge_pdfs(output: str | Path, inputs: Sequence[str | Path]) -> MergeSummary:
    """Merge multiple PDFs into a single output file."""
    validated_inputs = validate_files(inputs)
    output_path = Path(output).expanduser()

    if output_path.suffix.lower() != ".pdf":
        raise ValidationError(f"Output must be a .pdf file: {output_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    page_count = 0

    for pdf_path in validated_inputs:
        try:
            reader = PdfReader(str(pdf_path))
        except PdfReadError as exc:
            raise ProcessingError(f"Failed to read PDF: {pdf_path}") from exc

        for page in reader.pages:
            writer.add_page(page)
            page_count += 1

    if page_count == 0:
        raise ProcessingError("No pages were found in the provided PDFs.")

    try:
        with output_path.open("wb") as output_file:
            writer.write(output_file)
    except OSError as exc:
        raise ProcessingError(f"Failed to write output PDF: {output_path}") from exc

    return MergeSummary(
        output_path=output_path,
        files_merged=len(validated_inputs),
        pages_written=page_count,
    )


def merge_pdf_pages(output: str | Path, pdf: str | Path, start: int, end: int) -> MergeSummary:
    """Extract and save a page range [start, end) from a PDF."""
    validated_input = validate_files([pdf])[0]
    output_path = Path(output).expanduser()

    if output_path.suffix.lower() != ".pdf":
        raise ValidationError(f"Output must be a .pdf file: {output_path}")

    try:
        reader = PdfReader(str(validated_input))
    except PdfReadError as exc:
        raise ProcessingError(f"Failed to read PDF: {validated_input}") from exc

    total_pages = len(reader.pages)
    if start < 0 or end > total_pages or start >= end:
        raise ValidationError(
            f"Invalid page range {start}:{end}. PDF has {total_pages} pages."
        )

    writer = PdfWriter()
    for page_num in range(start, end):
        writer.add_page(reader.pages[page_num])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output_path.open("wb") as output_file:
            writer.write(output_file)
    except OSError as exc:
        raise ProcessingError(f"Failed to write output PDF: {output_path}") from exc

    return MergeSummary(
        output_path=output_path,
        files_merged=1,
        pages_written=end - start,
    )
