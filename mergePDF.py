#!/usr/bin/env python3
"""
Script for merging PDF files using command line interface.

Usage:

Combine two PDF files:
    python mergePDF.py files -o combined.pdf -i a.pdf b.pdf c.pdf

Merge all PDF files in a directory:
    python mergePDF.py dir -o merged.pdf -d ./reports/

Merge specific pages from a PDF:
    python mergePDF.py pages -o extract.pdf -p big.pdf -s 0 -e 4

Verbose mode:
    python mergePDF.py files -o out.pdf -i *.pdf -v
"""
import argparse
from pypdf import PdfReader, PdfWriter
import os
import sys

def merge_pdfs(output, inputs, verbose=False):
    writer = PdfWriter()

    for pdf in inputs:
        if verbose:
            print(f"[+] Adding: {pdf}")

        try:
            reader = PdfReader(pdf)
        except Exception as e:
            print(f"[-] Failed to read {pdf}: {e}")
            sys.exit(1)

        for page in reader.pages:
            writer.add_page(page)

    with open(output, "wb") as f:
        writer.write(f)

    if verbose:
        print(f"[+] Successfully wrote: {output}")


def merge_directory(output, directory, verbose=False):
    writer = PdfWriter()

    try:
        pdfs = sorted(
            [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(".pdf")]
        )
    except OSError as e:
        print(f"[-] Failed to read directory {directory}: {e}")
        sys.exit(1)

    if not pdfs:
        print("[-] No PDFs found in directory.")
        sys.exit(1)

    for pdf in pdfs:
        if verbose:
            print(f"[+] Adding: {pdf}")

        try:
            reader = PdfReader(pdf)
        except Exception as e:
            print(f"[-] Failed to read {pdf}: {e}")
            sys.exit(1)

        for page in reader.pages:
            writer.add_page(page)

    with open(output, "wb") as f:
        writer.write(f)

    if verbose:
        print(f"[+] Successfully wrote: {output}")


def merge_pages(output, pdf, start, end, verbose=False):
    writer = PdfWriter()

    if verbose:
        print(f"[+] Extracting pages {start}–{end} from {pdf}")

    try:
        reader = PdfReader(pdf)
    except Exception as e:
        print(f"[-] Failed to read {pdf}: {e}")
        sys.exit(1)

    total_pages = len(reader.pages)

    if start < 0 or end > total_pages or start >= end:
        print(f"[-] Invalid page range. PDF has {total_pages} pages.")
        sys.exit(1)

    for page_num in range(start, end):
        writer.add_page(reader.pages[page_num])

    with open(output, "wb") as f:
        writer.write(f)

    if verbose:
        print(f"[+] Successfully wrote: {output}")


def main():
    parser = argparse.ArgumentParser(
        description="MergePDF — A CLI tool for merging PDF files (pypdf modern API)."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # merge files
    merge_files = subparsers.add_parser("files", help="Merge specific PDF files")
    merge_files.add_argument("-o", "--output", required=True, help="Output PDF file")
    merge_files.add_argument("-i", "--inputs", nargs="+", required=True, help="Input PDF files")
    merge_files.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # merge directory
    merge_dir = subparsers.add_parser("dir", help="Merge all PDFs in a directory")
    merge_dir.add_argument("-o", "--output", required=True, help="Output PDF file")
    merge_dir.add_argument("-d", "--directory", required=True, help="Directory containing PDFs")
    merge_dir.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # merge pages
    merge_pages_cmd = subparsers.add_parser("pages", help="Merge specific pages from a PDF")
    merge_pages_cmd.add_argument("-o", "--output", required=True, help="Output PDF file")
    merge_pages_cmd.add_argument("-p", "--pdf", required=True, help="Input PDF file")
    merge_pages_cmd.add_argument("-s", "--start", type=int, required=True, help="Start page (0-indexed)")
    merge_pages_cmd.add_argument("-e", "--end", type=int, required=True, help="End page (exclusive)")
    merge_pages_cmd.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.command == "files":
        merge_pdfs(args.output, args.inputs, args.verbose)

    elif args.command == "dir":
        merge_directory(args.output, args.directory, args.verbose)

    elif args.command == "pages":
        merge_pages(args.output, args.pdf, args.start, args.end, args.verbose)


if __name__ == "__main__":
    main()
