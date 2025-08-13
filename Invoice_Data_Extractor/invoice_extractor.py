"""
Invoice Data Extractor

A Python class for extracting structured data from invoice images using OCR.
"""

import cv2
import pytesseract
import re
import json
from PIL import Image
import numpy as np
from datetime import datetime
from dateutil import parser as date_parser


class InvoiceExtractor:
    """Main class for extracting data from invoice images."""
    
    def __init__(self):
        """Initialize the Invoice Extractor."""
        self.text_data = ""
        self.extracted_data = {}
        
    def preprocess_image(self, image_path):
        """
        Preprocess the image for better OCR results.
        
        Args:
            image_path (str): Path to the invoice image
            
        Returns:
            numpy.ndarray: Preprocessed image
        """
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")
            
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply threshold to get a binary image
        _, threshold = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return threshold
    
    def extract_text_from_image(self, image_path):
        """
        Extract text from invoice image using OCR.
        
        Args:
            image_path (str): Path to the invoice image
            
        Returns:
            str: Extracted text from the image
        """
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image_path)
            
            # Use pytesseract to extract text
            text = pytesseract.image_to_string(processed_image, config='--psm 6')
            
            self.text_data = text
            return text
            
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")
    
    def extract_invoice_number(self, text):
        """Extract invoice number from text."""
        patterns = [
            r'invoice\s*(?:number|no\.?|#)\s*:?\s*([A-Za-z0-9\-]+)',
            r'inv\s*(?:no\.?|#)\s*:?\s*([A-Za-z0-9\-]+)',
            r'invoice\s*([A-Za-z0-9\-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def extract_date(self, text):
        """Extract date from text."""
        # Common date patterns
        date_patterns = [
            r'(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
            r'(\d{2,4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2})',
            r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4})',
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    # Try to parse the date
                    parsed_date = date_parser.parse(match, fuzzy=True)
                    return parsed_date.strftime('%Y-%m-%d')
                except:
                    continue
        return None
    
    def extract_total_amount(self, text):
        """Extract total amount from text."""
        # Look for common total patterns (prioritize TOTAL over subtotal)
        patterns = [
            r'(?:^|\s)total\s*:?\s*\$?([0-9,]+\.?\d*)',  # Final total
            r'grand\s*total\s*:?\s*\$?([0-9,]+\.?\d*)',
            r'amount\s*due\s*:?\s*\$?([0-9,]+\.?\d*)',
            r'balance\s*due\s*:?\s*\$?([0-9,]+\.?\d*)',
        ]
        
        # Find all matches and take the largest one (usually the final total)
        all_amounts = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                amount_str = match.group(1).replace(',', '')
                try:
                    amount = float(amount_str)
                    all_amounts.append(amount)
                except ValueError:
                    continue
        
        # Return the largest amount found (usually the final total)
        return max(all_amounts) if all_amounts else None
    
    def extract_vendor_info(self, text):
        """Extract vendor information from text."""
        # Split text into lines and look for company-like patterns
        lines = text.split('\n')
        
        # Look for the first meaningful line that looks like a company name
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if len(line) > 5 and len(line) < 50:  # Reasonable company name length
                # Check if it contains typical company indicators or is all caps
                if ('INC' in line.upper() or 'LLC' in line.upper() or 'CORP' in line.upper() or 
                    'COMPANY' in line.upper() or 'LTD' in line.upper() or
                    (line.isupper() and ' ' in line and not any(char.isdigit() for char in line))):
                    return line
        
        return None
    
    def extract_data_from_text(self, text):
        """
        Extract structured data from the OCR text.
        
        Args:
            text (str): Raw text extracted from invoice
            
        Returns:
            dict: Extracted structured data
        """
        data = {
            'extraction_timestamp': datetime.now().isoformat(),
            'invoice_number': self.extract_invoice_number(text),
            'date': self.extract_date(text),
            'vendor': self.extract_vendor_info(text),
            'total_amount': self.extract_total_amount(text),
            'currency': 'USD',  # Default, could be enhanced to detect currency
            'raw_text': text
        }
        
        self.extracted_data = data
        return data
    
    def extract_from_image(self, image_path):
        """
        Complete extraction process from image to structured data.
        
        Args:
            image_path (str): Path to the invoice image
            
        Returns:
            dict: Extracted structured data
        """
        # Extract text from image
        text = self.extract_text_from_image(image_path)
        
        # Extract structured data from text
        data = self.extract_data_from_text(text)
        
        return data
    
    def save_to_json(self, output_path):
        """Save extracted data to JSON file."""
        if not self.extracted_data:
            raise ValueError("No data to save. Run extraction first.")
            
        with open(output_path, 'w') as f:
            json.dump(self.extracted_data, f, indent=2, default=str)
    
    def save_to_csv(self, output_path):
        """Save extracted data to CSV file."""
        if not self.extracted_data:
            raise ValueError("No data to save. Run extraction first.")
            
        import pandas as pd
        
        # Flatten the data for CSV
        flattened_data = {}
        for key, value in self.extracted_data.items():
            if isinstance(value, (list, dict)):
                flattened_data[key] = str(value)
            else:
                flattened_data[key] = value
        
        df = pd.DataFrame([flattened_data])
        df.to_csv(output_path, index=False)


if __name__ == "__main__":
    # Example usage
    extractor = InvoiceExtractor()
    
    # This would work if you have an invoice image
    # data = extractor.extract_from_image('sample_invoice.jpg')
    # print(json.dumps(data, indent=2))
    
    print("Invoice Data Extractor initialized successfully!")
    print("Use extract_from_image(image_path) to extract data from an invoice.")