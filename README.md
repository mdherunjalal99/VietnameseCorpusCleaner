# Vietnamese Corpus Filter

A Python tool for filtering Vietnamese text corpora by removing sentences that contain:
- Abbreviations (e.g., "NBA", "GTVT", "U.S.A")
- English words

## Features

- Reads text files in UTF-8 encoding (required for Vietnamese characters)
- Preserves document structure (paragraphs)
- Intelligently detects abbreviations and English words
- Creates a filtered output file with unwanted sentences removed

## Installation

No additional libraries are required. This script uses only Python 3 standard libraries.

## Usage

Basic usage:

```bash
python vietnamese_corpus_filter.py input_file.txt
