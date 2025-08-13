#!/usr/bin/env python3
"""
Text-only Invoice Data Extractor (for testing without OCR dependencies)

Usage:
    python extract_text.py --input sample_text.txt --output data.json
"""

import argparse
import json
import sys
from pathlib import Path
from simple_test import SimpleInvoiceExtractor


def main():
    """Main function for text-only extraction."""
    parser = argparse.ArgumentParser(
        description='Extract structured data from invoice text files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Extract from text file to JSON:
    python extract_text.py --input samples/sample_invoice.txt --output data.json
    
  Print to console:
    python extract_text.py --input samples/sample_invoice.txt
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to text file containing invoice data'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file path (optional, prints to console if not specified)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' does not exist.", file=sys.stderr)
        return 1
    
    try:
        # Read input text
        with open(input_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
            
        if args.verbose:
            print(f"Processing: {args.input}")
            print(f"Text length: {len(text_content)} characters")
            
        # Initialize extractor
        extractor = SimpleInvoiceExtractor()
        
        # Extract data
        data = extractor.extract_data_from_text(text_content)
        
        if args.verbose:
            print("Extraction completed successfully!")
        
        # Output results
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            if args.verbose:
                print(f"Data saved to: {output_path}")
        else:
            # Print to console
            print(json.dumps(data, indent=2, default=str))
            
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())