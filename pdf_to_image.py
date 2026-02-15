#!/usr/bin/env python3
"""
PDF to Image Converter
Convert PDF pages to images or extract embedded images from PDFs.
Perfect for WeChat Official Account content creation.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple
import io

try:
    from PIL import Image
    import fitz  # PyMuPDF
except ImportError as e:
    print(f"Error: Missing required dependency. Please install: pip install PyMuPDF Pillow")
    print(f"Details: {e}")
    sys.exit(1)


class PDFImageConverter:
    """Convert PDF pages to images and extract embedded images."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize converter with a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        self.pdf_path = pdf_path
        self.pdf_document = fitz.open(pdf_path)
        self.page_count = len(self.pdf_document)
    
    def convert_pages_to_images(
        self, 
        output_dir: str = "output",
        pages: Optional[List[int]] = None,
        dpi: int = 300,
        image_format: str = "png"
    ) -> List[str]:
        """
        Convert PDF pages to images.
        
        Args:
            output_dir: Directory to save images
            pages: List of page numbers to convert (1-based). None for all pages
            dpi: Resolution in DPI (default 300 for high quality)
            image_format: Output format (png, jpg, jpeg)
        
        Returns:
            List of paths to generated images
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Determine which pages to convert
        if pages is None:
            pages_to_convert = range(self.page_count)
        else:
            # Convert to 0-based indexing
            pages_to_convert = [p - 1 for p in pages if 0 < p <= self.page_count]
        
        # Calculate zoom factor for desired DPI (default PDF is 72 DPI)
        zoom = dpi / 72
        matrix = fitz.Matrix(zoom, zoom)
        
        output_paths = []
        base_name = Path(self.pdf_path).stem
        
        for page_num in pages_to_convert:
            page = self.pdf_document[page_num]
            
            # Render page to pixmap
            pix = page.get_pixmap(matrix=matrix)
            
            # Generate output filename
            output_filename = f"{base_name}_page_{page_num + 1}.{image_format}"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save image
            if image_format.lower() in ['jpg', 'jpeg']:
                # Convert to RGB for JPEG
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.save(output_path, "JPEG", quality=95)
            else:
                pix.save(output_path)
            
            output_paths.append(output_path)
            print(f"Saved page {page_num + 1} to {output_path}")
        
        return output_paths
    
    def extract_images(
        self, 
        output_dir: str = "output",
        min_width: int = 100,
        min_height: int = 100
    ) -> List[Tuple[str, int]]:
        """
        Extract all embedded images from the PDF.
        
        Args:
            output_dir: Directory to save extracted images
            min_width: Minimum width to extract (filter small icons)
            min_height: Minimum height to extract (filter small icons)
        
        Returns:
            List of tuples (image_path, page_number)
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        extracted_images = []
        base_name = Path(self.pdf_path).stem
        image_counter = 0
        
        for page_num in range(self.page_count):
            page = self.pdf_document[page_num]
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                
                # Extract image
                base_image = self.pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Load image to check dimensions
                image = Image.open(io.BytesIO(image_bytes))
                width, height = image.size
                
                # Filter by minimum size
                if width < min_width or height < min_height:
                    continue
                
                # Generate output filename
                image_counter += 1
                output_filename = f"{base_name}_image_{image_counter}.{image_ext}"
                output_path = os.path.join(output_dir, output_filename)
                
                # Save image
                with open(output_path, "wb") as f:
                    f.write(image_bytes)
                
                extracted_images.append((output_path, page_num + 1))
                print(f"Extracted image {image_counter} from page {page_num + 1}: {output_path} ({width}x{height})")
        
        return extracted_images
    
    def get_page_info(self, page_num: int = 1) -> dict:
        """
        Get information about a specific page.
        
        Args:
            page_num: Page number (1-based)
        
        Returns:
            Dictionary with page information
        """
        if page_num < 1 or page_num > self.page_count:
            raise ValueError(f"Invalid page number. PDF has {self.page_count} pages.")
        
        page = self.pdf_document[page_num - 1]
        rect = page.rect
        
        return {
            "page_number": page_num,
            "width": rect.width,
            "height": rect.height,
            "rotation": page.rotation,
            "image_count": len(page.get_images())
        }
    
    def close(self):
        """Close the PDF document."""
        if self.pdf_document:
            self.pdf_document.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """Command-line interface for PDF to image conversion."""
    parser = argparse.ArgumentParser(
        description="Convert PDF pages to images or extract embedded images.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert all pages to PNG images
  python pdf_to_image.py document.pdf

  # Convert specific pages
  python pdf_to_image.py document.pdf -p 1 3 5

  # Extract embedded images
  python pdf_to_image.py document.pdf -e

  # Convert to JPEG with custom DPI
  python pdf_to_image.py document.pdf -f jpg -d 150

  # Do both: convert pages AND extract images
  python pdf_to_image.py document.pdf -e -o output_folder
        """
    )
    
    parser.add_argument("pdf_file", help="Path to PDF file")
    parser.add_argument("-o", "--output", default="output", help="Output directory (default: output)")
    parser.add_argument("-p", "--pages", type=int, nargs="+", help="Specific pages to convert (default: all)")
    parser.add_argument("-e", "--extract", action="store_true", help="Extract embedded images")
    parser.add_argument("-d", "--dpi", type=int, default=300, help="DPI for page conversion (default: 300)")
    parser.add_argument("-f", "--format", choices=["png", "jpg", "jpeg"], default="png", 
                        help="Image format (default: png)")
    parser.add_argument("--min-width", type=int, default=100, 
                        help="Minimum width for extracted images (default: 100)")
    parser.add_argument("--min-height", type=int, default=100,
                        help="Minimum height for extracted images (default: 100)")
    parser.add_argument("-i", "--info", action="store_true", help="Show PDF information and exit")
    
    args = parser.parse_args()
    
    try:
        with PDFImageConverter(args.pdf_file) as converter:
            if args.info:
                # Display PDF information
                print(f"\nPDF Information: {args.pdf_file}")
                print(f"Total pages: {converter.page_count}")
                for page_num in range(1, min(6, converter.page_count + 1)):
                    info = converter.get_page_info(page_num)
                    print(f"\nPage {page_num}:")
                    print(f"  Size: {info['width']:.1f} x {info['height']:.1f} points")
                    print(f"  Images: {info['image_count']}")
                if converter.page_count > 5:
                    print(f"\n... and {converter.page_count - 5} more pages")
                return
            
            # Convert pages (default behavior unless only extraction is requested)
            if not args.extract or args.pages is not None:
                # If pages are specified OR extract-only mode is not set, convert pages
                # This allows: 
                #   1. Normal conversion: pdf_to_image.py doc.pdf
                #   2. Specific pages: pdf_to_image.py doc.pdf -p 1 3
                #   3. Both operations: pdf_to_image.py doc.pdf -e (extracts) + converts all pages
                #   4. Both with specific pages: pdf_to_image.py doc.pdf -e -p 1 3
                print(f"\nConverting PDF pages to {args.format.upper()} images...")
                print(f"\nConverting PDF pages to {args.format.upper()} images...")
                paths = converter.convert_pages_to_images(
                    output_dir=args.output,
                    pages=args.pages,
                    dpi=args.dpi,
                    image_format=args.format
                )
                print(f"\nSuccessfully converted {len(paths)} page(s)")
            
            # Extract embedded images
            if args.extract:
                print(f"\nExtracting embedded images...")
                images = converter.extract_images(
                    output_dir=args.output,
                    min_width=args.min_width,
                    min_height=args.min_height
                )
                print(f"\nSuccessfully extracted {len(images)} image(s)")
            
            print(f"\nAll files saved to: {args.output}/")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
