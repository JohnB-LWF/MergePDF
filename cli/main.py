"""Command-line interface for MergePDF."""

from __future__ import annotations

import argparse
from pathlib import Path

from mergepdf.engine import (
    MergePDFError,
    get_pdf_files_in_directory,
    merge_pdf_pages,
    merge_pdfs,
)


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level CLI parser."""
    parser = argparse.ArgumentParser(description="MergePDF CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    files_parser = subparsers.add_parser("files", help="Merge specific PDF files")
    files_parser.add_argument("-o", "--output", required=True, help="Output PDF file")
    files_parser.add_argument("-i", "--inputs", nargs="+", required=True, help="Input PDF files")

    directory_parser = subparsers.add_parser("dir", help="Merge all PDFs in a directory")
    directory_parser.add_argument("-o", "--output", required=True, help="Output PDF file")
    directory_parser.add_argument("-d", "--directory", required=True, help="Directory containing PDFs")

    pages_parser = subparsers.add_parser("pages", help="Extract pages from a single PDF")
    pages_parser.add_argument("-o", "--output", required=True, help="Output PDF file")
    pages_parser.add_argument("-p", "--pdf", required=True, help="Input PDF file")
    pages_parser.add_argument("-s", "--start", type=int, required=True, help="Start page index")
    pages_parser.add_argument("-e", "--end", type=int, required=True, help="End page index (exclusive)")

    return parser


def run(args: argparse.Namespace) -> int:
    """Execute CLI command from parsed args."""
    try:
        if args.command == "files":
            summary = merge_pdfs(output=args.output, inputs=args.inputs)
        elif args.command == "dir":
            pdf_files = get_pdf_files_in_directory(Path(args.directory))
            summary = merge_pdfs(output=args.output, inputs=pdf_files)
        else:
            summary = merge_pdf_pages(
                output=args.output,
                pdf=args.pdf,
                start=args.start,
                end=args.end,
            )
    except MergePDFError as exc:
        print(f"[-] {exc}")
        return 1

    print(
        f"[+] Wrote {summary.pages_written} pages from {summary.files_merged} file(s) to {summary.output_path}"
    )
    return 0


def main() -> int:
    """CLI entrypoint."""
    parser = build_parser()
    return run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
