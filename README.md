# File Conversion Utilities

This repository provides a simple command line script to convert PDF, Excel or CSV files into JSON.

## Usage

Install dependencies:

```bash
pip install pandas openpyxl pdfplumber
```

Run the converter specifying the input file and the desired output JSON file:

```bash
python convert_to_json.py <input_file> <output_file.json>
```

The input file may be a `.csv`, `.xls`, `.xlsx` or `.pdf` file. PDF files are converted to JSON containing the extracted text of each page. Excel files export each sheet under its sheet name, while CSV files are converted to a list of row objects.

