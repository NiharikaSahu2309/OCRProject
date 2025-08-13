# Sample Invoice Images

This directory contains sample invoice images for testing the Invoice Data Extractor.

## Files

- `sample_invoice.txt` - Sample text data from an invoice for testing
- `README.md` - This file

## Usage

You can test the extractor with any invoice image you have. Common formats supported:
- JPG/JPEG
- PNG  
- PDF (first page)

## Creating Test Data

To test the text extraction functionality without an actual image, you can use the sample text provided in `sample_invoice.txt`.

Example:
```python
from invoice_extractor import InvoiceExtractor

extractor = InvoiceExtractor()

# Read sample text
with open('samples/sample_invoice.txt', 'r') as f:
    sample_text = f.read()

# Extract data from the text
data = extractor.extract_data_from_text(sample_text)
print(data)
```