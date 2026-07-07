"""Core package for MergePDF logic."""

from .engine import (
    MergePDFError,
    MergeSummary,
    ProcessingError,
    ValidationError,
    get_pdf_files_in_directory,
    merge_pdf_pages,
    merge_pdfs,
    validate_files,
)

__all__ = [
    "MergePDFError",
    "MergeSummary",
    "ProcessingError",
    "ValidationError",
    "get_pdf_files_in_directory",
    "merge_pdf_pages",
    "merge_pdfs",
    "validate_files",
]
