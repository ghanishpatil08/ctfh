"""Steganography module for CTF-H"""

import os
from typing import Optional
from ctfh.utils import print_section, print_colored, Fore, get_file_path, get_input
from ctfh.menu import Menu

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def png_lsb_extract(image_path: str) -> None:
    """Extract LSB data from PNG"""
    print_section("PNG LSB Extraction")
    if not HAS_PIL:
        print_colored("PIL/Pillow not installed. Install with: pip install Pillow", Fore.RED)
        input("\nPress Enter to continue...")
        return
    
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = img.load()
        width, height = img.size
        
        binary_data = []
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                # Extract LSB from each channel
                binary_data.append(str(r & 1))
                binary_data.append(str(g & 1))
                binary_data.append(str(b & 1))
        
        # Convert binary to text (stop at null byte or reasonable length)
        binary_str = ''.join(binary_data)
        text = ""
        for i in range(0, min(len(binary_str), 10000), 8):
            byte = binary_str[i:i+8]
            if len(byte) == 8:
                char = chr(int(byte, 2))
                if char == '\x00':
                    break
                if char.isprintable() or char in '\n\r\t':
                    text += char
                else:
                    break
        
        if text:
            print_colored("Extracted text:", Fore.GREEN)
            print_colored(text[:500], Fore.CYAN)  # Show first 500 chars
            if len(text) > 500:
                print_colored(f"\n... (truncated, total length: {len(text)} chars)", Fore.YELLOW)
        else:
            print_colored("No readable text found in LSB.", Fore.YELLOW)
        
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def png_lsb_embed(image_path: str, text: str, output_path: str) -> None:
    """Embed text in PNG using LSB"""
    print_section("PNG LSB Embedding")
    if not HAS_PIL:
        print_colored("PIL/Pillow not installed. Install with: pip install Pillow", Fore.RED)
        input("\nPress Enter to continue...")
        return
    
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = img.load()
        width, height = img.size
        
        # Convert text to binary
        binary_text = ''.join(format(ord(c), '08b') for c in text)
        binary_text += '00000000'  # Null terminator
        
        # Check if image is large enough
        max_bits = width * height * 3
        if len(binary_text) > max_bits:
            print_colored(f"Error: Text too long for image. Max: {max_bits//8} chars", Fore.RED)
            input("\nPress Enter to continue...")
            return
        
        # Embed data
        bit_index = 0
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                
                if bit_index < len(binary_text):
                    r = (r & 0xFE) | int(binary_text[bit_index])
                    bit_index += 1
                if bit_index < len(binary_text):
                    g = (g & 0xFE) | int(binary_text[bit_index])
                    bit_index += 1
                if bit_index < len(binary_text):
                    b = (b & 0xFE) | int(binary_text[bit_index])
                    bit_index += 1
                
                pixels[x, y] = (r, g, b)
                
                if bit_index >= len(binary_text):
                    break
            if bit_index >= len(binary_text):
                break
        
        # Save output
        img.save(output_path, 'PNG')
        print_colored(f"Data embedded successfully! Saved to: {output_path}", Fore.GREEN)
        
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def bmp_extract(image_path: str) -> None:
    """Extract data from BMP (simple approach)"""
    print_section("BMP Data Extraction")
    if not HAS_PIL:
        print_colored("PIL/Pillow not installed. Install with: pip install Pillow", Fore.RED)
        input("\nPress Enter to continue...")
        return
    
    try:
        with open(image_path, 'rb') as f:
            data = f.read()
        
        # Look for text patterns in the file
        text_data = ""
        current_text = ""
        for byte in data:
            if 32 <= byte <= 126 or byte in [9, 10, 13]:  # Printable ASCII
                current_text += chr(byte)
            else:
                if len(current_text) >= 4:  # Minimum 4 chars to be interesting
                    text_data += current_text + "\n"
                current_text = ""
        
        if current_text and len(current_text) >= 4:
            text_data += current_text
        
        if text_data:
            print_colored("Extracted text from BMP:", Fore.GREEN)
            print_colored(text_data[:1000], Fore.CYAN)
            if len(text_data) > 1000:
                print_colored(f"\n... (truncated)", Fore.YELLOW)
        else:
            print_colored("No readable text found in BMP.", Fore.YELLOW)
        
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def exif_metadata(image_path: str) -> None:
    """Extract EXIF metadata"""
    print_section("EXIF Metadata Extraction")
    if not HAS_PIL:
        print_colored("PIL/Pillow not installed. Install with: pip install Pillow", Fore.RED)
        input("\nPress Enter to continue...")
        return
    
    try:
        img = Image.open(image_path)
        exifdata = img.getexif()
        
        if not exifdata:
            print_colored("No EXIF data found in image.", Fore.YELLOW)
            input("\nPress Enter to continue...")
            return
        
        print_colored("EXIF Metadata:", Fore.GREEN)
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            print_colored(f"  {tag}: {data}", Fore.CYAN)
        
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def steganography_menu() -> None:
    """Steganography module menu"""
    def handle_png_lsb_extract():
        path = get_file_path("Enter PNG file path")
        if path:
            png_lsb_extract(path)
    
    def handle_png_lsb_embed():
        path = get_file_path("Enter PNG file path")
        text = get_input("Enter text to embed")
        output = get_input("Enter output file path", "output_stego.png")
        if path and text and output:
            png_lsb_embed(path, text, output)
    
    def handle_bmp_extract():
        path = get_file_path("Enter BMP file path")
        if path:
            bmp_extract(path)
    
    def handle_exif():
        path = get_file_path("Enter image file path")
        if path:
            exif_metadata(path)
    
    options = [
        (1, "PNG LSB Extract", handle_png_lsb_extract),
        (2, "PNG LSB Embed", handle_png_lsb_embed),
        (3, "BMP Extract", handle_bmp_extract),
        (4, "EXIF Metadata", handle_exif),
        (0, "Back to Main Menu", lambda: None),
    ]
    
    menu = Menu("Steganography Module", options)
    menu.run()

