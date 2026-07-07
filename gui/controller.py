"""Controller bridge between Streamlit UI and mergepdf engine."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Protocol, Sequence

from mergepdf.engine import MergePDFError, merge_pdfs


@dataclass(frozen=True)
class MergeControllerResult:
    """Result payload for GUI merge actions."""

    success: bool
    messages: list[str]
    output_bytes: bytes | None = None
    output_name: str | None = None


class UploadedPDF(Protocol):
    """Typing protocol for Streamlit uploaded files."""

    name: str

    def getvalue(self) -> bytes:
        """Return in-memory bytes."""


def merge_uploaded_pdfs(
    uploaded_files: Sequence[UploadedPDF],
    output_name: str = "merged.pdf",
) -> MergeControllerResult:
    """Merge uploaded Streamlit files using engine functions."""
    if not uploaded_files:
        return MergeControllerResult(
            success=False,
            messages=["> No PDFs selected. Add files and try again."],
        )

    messages = [
        "> Validating files...",
        "> Writing upload buffer to temporary workspace...",
    ]

    try:
        with TemporaryDirectory(prefix="mergepdf-") as temp_dir:
            temp_dir_path = Path(temp_dir)
            input_paths: list[Path] = []

            for index, uploaded_file in enumerate(uploaded_files):
                file_name = uploaded_file.name if uploaded_file.name else f"input-{index + 1}.pdf"
                temp_input_path = temp_dir_path / f"{index + 1:02d}-{file_name}"
                file_bytes = uploaded_file.getvalue()
                temp_input_path.write_bytes(file_bytes)
                input_paths.append(temp_input_path)

            messages.append("> Merging PDFs...")
            temp_output_path = temp_dir_path / output_name
            summary = merge_pdfs(output=temp_output_path, inputs=input_paths)
            output_bytes = temp_output_path.read_bytes()
    except MergePDFError as exc:
        return MergeControllerResult(
            success=False,
            messages=[*messages, f"> Error: {exc}"],
        )
    except OSError as exc:
        return MergeControllerResult(
            success=False,
            messages=[*messages, f"> Error: temporary file operation failed ({exc})."],
        )

    success_messages = [
        *messages,
        f"> Output ready: {summary.output_path.name}",
        f"> Files merged: {summary.files_merged}",
        f"> Pages written: {summary.pages_written}",
    ]
    return MergeControllerResult(
        success=True,
        messages=success_messages,
        output_bytes=output_bytes,
        output_name=output_name,
    )
