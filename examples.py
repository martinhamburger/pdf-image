#!/usr/bin/env python3
"""
Example: Basic usage of PDF to Image converter
"""

from pdf_to_image import PDFImageConverter

def example_1_convert_all_pages(pdf_path):
    """Convert all pages of a PDF to images."""
    print("Example 1: Converting all pages to images")
    print("-" * 50)
    
    with PDFImageConverter(pdf_path) as converter:
        print(f"PDF has {converter.page_count} pages")
        
        # Convert all pages
        image_paths = converter.convert_pages_to_images(
            output_dir="example_output/all_pages",
            dpi=300,
            image_format="png"
        )
        
        print(f"\nConverted {len(image_paths)} pages")
        for path in image_paths:
            print(f"  - {path}")


def example_2_convert_specific_pages(pdf_path):
    """Convert only specific pages."""
    print("\nExample 2: Converting specific pages")
    print("-" * 50)
    
    with PDFImageConverter(pdf_path) as converter:
        # Select pages that exist in the PDF
        pages_to_convert = [1]
        if converter.page_count >= 3:
            pages_to_convert.append(3)
        if converter.page_count >= 5:
            pages_to_convert.append(5)
        
        print(f"Converting pages: {pages_to_convert}")
        
        # Convert only selected pages
        image_paths = converter.convert_pages_to_images(
            output_dir="example_output/selected_pages",
            pages=pages_to_convert,
            dpi=300,
            image_format="png"
        )
        
        print(f"\nConverted {len(image_paths)} pages")


def example_3_extract_images(pdf_path):
    """Extract embedded images from PDF."""
    print("\nExample 3: Extracting embedded images")
    print("-" * 50)
    
    with PDFImageConverter(pdf_path) as converter:
        # Extract all embedded images
        extracted = converter.extract_images(
            output_dir="example_output/extracted_images",
            min_width=100,
            min_height=100
        )
        
        print(f"\nExtracted {len(extracted)} images")
        for image_path, page_num in extracted:
            print(f"  - {image_path} (from page {page_num})")


def example_4_get_pdf_info(pdf_path):
    """Get information about PDF pages."""
    print("\nExample 4: Getting PDF information")
    print("-" * 50)
    
    with PDFImageConverter(pdf_path) as converter:
        print(f"Total pages: {converter.page_count}\n")
        
        # Get info for first few pages
        for page_num in range(1, min(4, converter.page_count + 1)):
            info = converter.get_page_info(page_num)
            print(f"Page {page_num}:")
            print(f"  Size: {info['width']:.1f} x {info['height']:.1f} points")
            print(f"  Rotation: {info['rotation']}°")
            print(f"  Embedded images: {info['image_count']}\n")


def example_5_custom_quality(pdf_path):
    """Convert pages with custom quality settings."""
    print("\nExample 5: Custom quality settings")
    print("-" * 50)
    
    with PDFImageConverter(pdf_path) as converter:
        # High quality PNG (300 DPI)
        print("Creating high-quality PNG...")
        converter.convert_pages_to_images(
            output_dir="example_output/high_quality",
            pages=[1],
            dpi=300,
            image_format="png"
        )
        
        # Lower quality JPEG for web (150 DPI)
        print("Creating web-optimized JPEG...")
        converter.convert_pages_to_images(
            output_dir="example_output/web_quality",
            pages=[1],
            dpi=150,
            image_format="jpg"
        )


def example_6_wechat_workflow(pdf_path):
    """Complete workflow for WeChat Official Account content."""
    print("\nExample 6: WeChat Official Account workflow")
    print("-" * 50)
    
    with PDFImageConverter(pdf_path) as converter:
        print(f"Processing PDF for WeChat Official Account...")
        print(f"PDF has {converter.page_count} pages\n")
        
        # Convert first page as cover image
        print("1. Creating cover image from page 1...")
        cover = converter.convert_pages_to_images(
            output_dir="example_output/wechat",
            pages=[1],
            dpi=300,
            image_format="png"
        )
        print(f"   Cover: {cover[0]}")
        
        # Extract all embedded images
        print("\n2. Extracting embedded images...")
        images = converter.extract_images(
            output_dir="example_output/wechat",
            min_width=150,
            min_height=150
        )
        print(f"   Extracted {len(images)} images")
        
        # Convert specific content pages if available
        if converter.page_count >= 3:
            print("\n3. Converting content pages...")
            # Convert up to 2 additional pages
            content_pages = list(range(2, min(4, converter.page_count + 1)))
            if content_pages:
                content = converter.convert_pages_to_images(
                    output_dir="example_output/wechat",
                    pages=content_pages,
                    dpi=300,
                    image_format="png"
                )
                print(f"   Content pages: {len(content)}")
        else:
            print("\n3. PDF has only 1-2 pages, skipping additional content pages")
        
        print("\n✓ All images ready for WeChat Official Account!")
        print(f"   Check folder: example_output/wechat/")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python examples.py <pdf_file>")
        print("\nThis script demonstrates various ways to use the PDF to Image converter.")
        print("You'll need a PDF file to run the examples.")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    try:
        # Run all examples
        example_1_convert_all_pages(pdf_file)
        example_2_convert_specific_pages(pdf_file)
        example_3_extract_images(pdf_file)
        example_4_get_pdf_info(pdf_file)
        example_5_custom_quality(pdf_file)
        example_6_wechat_workflow(pdf_file)
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        print("Check the 'example_output' directory for results.")
        
    except FileNotFoundError:
        print(f"Error: PDF file not found: {pdf_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
