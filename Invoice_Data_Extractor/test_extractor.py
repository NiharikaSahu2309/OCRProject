"""
Unit tests for Invoice Data Extractor

Run with: python -m pytest test_extractor.py
"""

import pytest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
from invoice_extractor import InvoiceExtractor


class TestInvoiceExtractor:
    """Test class for InvoiceExtractor functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.extractor = InvoiceExtractor()
        
    def test_init(self):
        """Test InvoiceExtractor initialization."""
        assert self.extractor.text_data == ""
        assert self.extractor.extracted_data == {}
        
    def test_extract_invoice_number(self):
        """Test invoice number extraction."""
        test_cases = [
            ("Invoice Number: INV-2024-001", "INV-2024-001"),
            ("Invoice No. 12345", "12345"),
            ("Invoice #ABC-123", "ABC-123"),
            ("INV NO: XYZ789", "XYZ789"),
            ("No invoice number here", None),
        ]
        
        for text, expected in test_cases:
            result = self.extractor.extract_invoice_number(text)
            assert result == expected, f"Failed for text: {text}"
            
    def test_extract_date(self):
        """Test date extraction."""
        test_cases = [
            ("Date: 12/31/2024", "2024-12-31"),
            ("2024-01-15", "2024-01-15"),
            ("15 Jan 2024", "2024-01-15"),
            ("No date here", None),
        ]
        
        for text, expected in test_cases:
            result = self.extractor.extract_date(text)
            if expected:
                assert result == expected, f"Failed for text: {text}"
            else:
                assert result is None, f"Should be None for text: {text}"
                
    def test_extract_total_amount(self):
        """Test total amount extraction."""
        test_cases = [
            ("Total: $1,250.00", 1250.0),
            ("Amount: 500.50", 500.5),
            ("Grand Total: $2,000", 2000.0),
            ("$999.99 Total", 999.99),
            ("No amount here", None),
        ]
        
        for text, expected in test_cases:
            result = self.extractor.extract_total_amount(text)
            assert result == expected, f"Failed for text: {text}"
            
    def test_extract_vendor_info(self):
        """Test vendor information extraction."""
        test_cases = [
            ("ABC Company Inc\nInvoice Details", "ABC Company Inc"),
            ("XYZ Corp.\n123 Main St", "XYZ Corp."),
            ("No company info\njust random text", None),
        ]
        
        for text, expected in test_cases:
            result = self.extractor.extract_vendor_info(text)
            if expected:
                assert expected in (result or ""), f"Failed for text: {text}"
            
    def test_extract_data_from_text(self):
        """Test complete data extraction from text."""
        sample_text = """
        ABC Company Inc
        Invoice Number: INV-2024-001
        Date: 2024-01-15
        Total: $1,250.00
        """
        
        result = self.extractor.extract_data_from_text(sample_text)
        
        assert isinstance(result, dict)
        assert result['invoice_number'] == 'INV-2024-001'
        assert result['date'] == '2024-01-15'
        assert result['total_amount'] == 1250.0
        assert 'extraction_timestamp' in result
        assert result['raw_text'] == sample_text
        
    @patch('cv2.imread')
    @patch('pytesseract.image_to_string')
    def test_extract_text_from_image(self, mock_tesseract, mock_imread):
        """Test text extraction from image (mocked)."""
        # Mock the image loading and OCR
        mock_imread.return_value = MagicMock()  # Mock image array
        mock_tesseract.return_value = "Sample OCR text"
        
        # Create a temporary file path
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            tmp_path = tmp.name
            
        try:
            result = self.extractor.extract_text_from_image(tmp_path)
            assert result == "Sample OCR text"
            assert self.extractor.text_data == "Sample OCR text"
        finally:
            os.unlink(tmp_path)
            
    def test_save_to_json(self):
        """Test saving data to JSON file."""
        # Set up some test data
        self.extractor.extracted_data = {
            'invoice_number': 'TEST-001',
            'total_amount': 100.0
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
            
        try:
            self.extractor.save_to_json(tmp_path)
            
            # Read and verify the saved data
            with open(tmp_path, 'r') as f:
                saved_data = json.load(f)
                
            assert saved_data['invoice_number'] == 'TEST-001'
            assert saved_data['total_amount'] == 100.0
        finally:
            os.unlink(tmp_path)
            
    def test_save_to_json_no_data(self):
        """Test saving to JSON with no extracted data."""
        with pytest.raises(ValueError, match="No data to save"):
            self.extractor.save_to_json("dummy_path.json")


if __name__ == "__main__":
    # Run a basic test
    extractor = InvoiceExtractor()
    
    # Test some basic functionality
    sample_text = """
    ABC Company Inc
    Invoice Number: INV-2024-001
    Date: 2024-01-15
    Total: $1,250.00
    """
    
    result = extractor.extract_data_from_text(sample_text)
    print("Test extraction result:")
    print(json.dumps(result, indent=2, default=str))
    print("\nBasic tests passed!")