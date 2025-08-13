#!/usr/bin/env python3
"""
Command line interface for Invoice Data Extractor

Usage:
    python extract_invoice.py --input image.jpg --output data.json
    python extract_invoice.py --input image.jpg --output data.csv --format csv
"""

import argparse
import json
import sys
from pathlib import Path
from invoice_extractor import InvoiceExtractor


def main():
    """Main function for command line interface."""
    parser = argparse.ArgumentParser(
        description='Extract structured data from invoice images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Extract to JSON:
    python extract_invoice.py --input invoice.jpg --output data.json
    
  Extract to CSV:
    python extract_invoice.py --input invoice.jpg --output data.csv --format csv
    
  Print to console:
    python extract_invoice.py --input invoice.jpg
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to invoice image file (JPG, PNG, PDF)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file path (optional, prints to console if not specified)'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['json', 'csv'],
        default='json',
        help='Output format (default: json)'
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
        # Initialize extractor
        if args.verbose:
            print(f"Processing: {args.input}")
            
        extractor = InvoiceExtractor()
        
        # Extract data
        data = extractor.extract_from_image(str(input_path))
        
        if args.verbose:
            print("Extraction completed successfully!")
        
        # Output results
        if args.output:
            output_path = Path(args.output)
            
            if args.format == 'csv':
                extractor.save_to_csv(str(output_path))
                if args.verbose:
                    print(f"Data saved to: {output_path}")
            else:
                extractor.save_to_json(str(output_path))
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