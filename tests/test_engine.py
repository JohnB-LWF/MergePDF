"""Unit tests for mergepdf.engine."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from mergepdf.engine import (
    ProcessingError,
    ValidationError,
    get_pdf_files_in_directory,
    merge_pdf_pages,
    merge_pdfs,
    validate_files,
)


def create_pdf(path: Path, width: int = 72, height: int = 72, pages: int = 1) -> None:
    """Create a simple PDF for tests."""
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=width, height=height)
    with path.open("wb") as file_obj:
        writer.write(file_obj)


class TestEngine(unittest.TestCase):
    """Behavior tests for PDF engine functions."""

    def test_validate_files_requires_input(self) -> None:
        with self.assertRaises(ValidationError):
            validate_files([])

    def test_validate_files_rejects_non_pdf_extension(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            text_path = Path(temp_dir) / "notes.txt"
            text_path.write_text("not a pdf", encoding="utf-8")
            with self.assertRaises(ValidationError):
                validate_files([text_path])

    def test_directory_scan_sorts_pdf_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            create_pdf(folder / "b.pdf")
            create_pdf(folder / "a.pdf")
            sorted_files = get_pdf_files_in_directory(folder)
            self.assertEqual([file_path.name for file_path in sorted_files], ["a.pdf", "b.pdf"])

    def test_merge_pdfs_preserves_input_order(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            first_pdf = folder / "first.pdf"
            second_pdf = folder / "second.pdf"
            output_pdf = folder / "merged.pdf"

            create_pdf(first_pdf, width=100, height=100, pages=1)
            create_pdf(second_pdf, width=220, height=100, pages=1)

            summary = merge_pdfs(output=output_pdf, inputs=[first_pdf, second_pdf])
            self.assertEqual(summary.pages_written, 2)
            self.assertTrue(output_pdf.exists())

            merged_reader = PdfReader(str(output_pdf))
            first_width = float(merged_reader.pages[0].mediabox.width)
            second_width = float(merged_reader.pages[1].mediabox.width)
            self.assertEqual(first_width, 100.0)
            self.assertEqual(second_width, 220.0)

    def test_merge_pdf_pages_extracts_expected_count(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            source_pdf = folder / "source.pdf"
            output_pdf = folder / "extract.pdf"
            create_pdf(source_pdf, pages=5)

            summary = merge_pdf_pages(output=output_pdf, pdf=source_pdf, start=1, end=4)
            self.assertEqual(summary.pages_written, 3)

            extracted = PdfReader(str(output_pdf))
            self.assertEqual(len(extracted.pages), 3)

    def test_merge_pdfs_raises_processing_error_for_invalid_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            fake_pdf = folder / "invalid.pdf"
            output_pdf = folder / "out.pdf"
            fake_pdf.write_text("this is not a real pdf", encoding="utf-8")

            with self.assertRaises(ProcessingError):
                merge_pdfs(output=output_pdf, inputs=[fake_pdf])


if __name__ == "__main__":
    unittest.main()
