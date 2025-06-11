import sys
import json
import os
from typing import Any

try:
    import pandas as pd
except ImportError:  # Should not happen if dependencies are installed
    pd = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


def convert_csv(path: str) -> Any:
    if pd is None:
        raise RuntimeError("pandas is required for csv conversion")
    df = pd.read_csv(path)
    return df.to_dict(orient="records")


def convert_excel(path: str) -> Any:
    if pd is None:
        raise RuntimeError("pandas is required for excel conversion")
    excel = pd.read_excel(path, sheet_name=None)  # all sheets
    result = {}
    for sheet_name, df in excel.items():
        result[sheet_name] = df.to_dict(orient="records")
    return result


def convert_pdf(path: str) -> Any:
    if pdfplumber is None:
        raise RuntimeError("pdfplumber is required for pdf conversion")
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text())
    return {"pages": pages}


def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_to_json.py <input_file> <output_json>")
        sys.exit(1)
    input_path, output_path = sys.argv[1], sys.argv[2]
    if not os.path.isfile(input_path):
        print(f"Input file '{input_path}' does not exist")
        sys.exit(1)

    ext = os.path.splitext(input_path)[1].lower()
    if ext == ".csv":
        data = convert_csv(input_path)
    elif ext in {".xls", ".xlsx"}:
        data = convert_excel(input_path)
    elif ext == ".pdf":
        data = convert_pdf(input_path)
    else:
        print(f"Unsupported file extension: {ext}")
        sys.exit(1)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Written JSON to {output_path}")


if __name__ == "__main__":
    main()
