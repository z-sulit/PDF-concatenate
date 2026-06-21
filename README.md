# PDF Concatenator

A simple GUI tool to merge multiple PDF files into one. Built with **Tkinter** and **pypdf**.

## Features

- Add, remove, and reorder PDF files via drag-order list
- Merge all selected PDFs into a single output file
- Page count summary on completion
- Lightweight — no heavy dependencies

## Prerequisites

- **Python 3.10+**

## Setup

### 1. Create a Virtual Environment (Required)

You **must** create a virtual environment before installing dependencies.

```bash
# Navigate to the project directory
cd PDF_Concatenate

# Create the virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate

# macOS / Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
python pdf_concatenate.py
```

### How to Use the App

1. Click **Add PDFs…** to select one or more PDF files.
2. Use **↑ Up** / **↓ Down** to reorder them — the merge follows this order.
3. Click **Remove** to delete a selected entry, or **Clear All** to start over.
4. Click **Merge & Save As…** to pick a destination and combine the PDFs.
5. A confirmation dialog shows the total page count and output path.

## Project Structure

```
PDF_Concatenate/
├── pdf_concatenate.py   # Main application
├── requirements.txt     # Python dependencies
├── .gitignore
└── .venv/               # Virtual environment (not tracked)
```

## Dependencies

| Package | Version  | Purpose              |
|---------|----------|----------------------|
| pypdf   | >= 4.0.0 | PDF reading & writing |

