# Invoice Data Extractor

A Python-based OCR tool for extracting structured data from invoice images and PDFs.

## Features

- Extract text from invoice images using OCR (Tesseract)
- Parse common invoice fields (date, amount, vendor, etc.)
- Support for multiple image formats (PNG, JPG, PDF)
- Export extracted data to JSON and CSV formats

## Installation

```bash
pip install -r requirements.txt
```

Note: You'll also need to install Tesseract OCR:
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Usage

### Basic Usage

```python
from invoice_extractor import InvoiceExtractor

# Initialize the extractor
extractor = InvoiceExtractor()

# Extract data from an invoice
data = extractor.extract_from_image('path/to/invoice.jpg')
print(data)
```

### Command Line Usage

```bash
python extract_invoice.py --input invoice.jpg --output data.json
```

## Sample Output

```json
{
  "invoice_number": "INV-2024-001",
  "date": "2024-01-15",
  "vendor": "ABC Company Ltd",
  "total_amount": "1250.00",
  "currency": "USD",
  "items": [
    {
      "description": "Product A",
      "quantity": 2,
      "unit_price": "500.00",
      "total": "1000.00"
    }
  ]
}
```

## Files

- `invoice_extractor.py` - Main extractor class
- `extract_invoice.py` - Command line interface
- `requirements.txt` - Python dependencies
- `test_extractor.py` - Unit tests
- `samples/` - Sample invoice images for testing