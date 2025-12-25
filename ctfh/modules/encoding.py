"""Encoding/Decoding module for CTF-H"""

import base64
import binascii
import urllib.parse
from typing import Optional
from ctfh.utils import (
    print_section, print_colored, Fore, Style, get_input,
    ask_copy_to_clipboard, ask_save_to_file, add_to_history,
    get_input_with_example
)
from ctfh.menu import Menu

try:
    import base58
    HAS_BASE58 = True
except ImportError:
    HAS_BASE58 = False

try:
    import base91
    HAS_BASE91 = False  # base85 is standard, base91 is less common
except ImportError:
    pass


def base64_encode(text: str) -> None:
    """Base64 encode"""
    print_section("Base64 Encode")
    try:
        result = base64.b64encode(text.encode()).decode()
        print_colored(f"Encoded: {result}", Fore.GREEN)
        
        add_to_history("encode", {"type": "base64", "input": text, "output": result})
        ask_copy_to_clipboard(result)
        ask_save_to_file(f"Input: {text}\nBase64: {result}", "base64_encoded", "txt")
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def base64_decode(text: str) -> None:
    """Base64 decode"""
    print_section("Base64 Decode")
    try:
        result = base64.b64decode(text.encode()).decode('utf-8', errors='ignore')
        print_colored(f"Decoded: {result}", Fore.GREEN)
        
        add_to_history("decode", {"type": "base64", "input": text, "output": result})
        ask_copy_to_clipboard(result)
        ask_save_to_file(f"Input: {text}\nDecoded: {result}", "base64_decoded", "txt")
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def base32_encode(text: str) -> None:
    """Base32 encode"""
    print_section("Base32 Encode")
    try:
        result = base64.b32encode(text.encode()).decode()
        print_colored(f"Encoded: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def base32_decode(text: str) -> None:
    """Base32 decode"""
    print_section("Base32 Decode")
    try:
        result = base64.b32decode(text.encode()).decode('utf-8', errors='ignore')
        print_colored(f"Decoded: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def base58_encode(text: str) -> None:
    """Base58 encode"""
    print_section("Base58 Encode")
    if not HAS_BASE58:
        print_colored("base58 library not installed. Install with: pip install base58", Fore.RED)
        input("\nPress Enter to continue...")
        return
    try:
        result = base58.b58encode(text.encode()).decode()
        print_colored(f"Encoded: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def base58_decode(text: str) -> None:
    """Base58 decode"""
    print_section("Base58 Decode")
    if not HAS_BASE58:
        print_colored("base58 library not installed. Install with: pip install base58", Fore.RED)
        input("\nPress Enter to continue...")
        return
    try:
        result = base58.b58decode(text).decode('utf-8', errors='ignore')
        print_colored(f"Decoded: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def base85_encode(text: str) -> None:
    """Base85 encode"""
    print_section("Base85 Encode")
    try:
        result = base64.b85encode(text.encode()).decode()
        print_colored(f"Encoded: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def base85_decode(text: str) -> None:
    """Base85 decode"""
    print_section("Base85 Decode")
    try:
        result = base64.b85decode(text.encode()).decode('utf-8', errors='ignore')
        print_colored(f"Decoded: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def hex_encode(text: str) -> None:
    """Hex encode"""
    print_section("Hex Encode")
    try:
        result = text.encode().hex()
        print_colored(f"Encoded: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def hex_decode(text: str) -> None:
    """Hex decode"""
    print_section("Hex Decode")
    try:
        # Remove spaces and common hex prefixes
        text = text.replace(' ', '').replace('0x', '').replace('\\x', '')
        result = bytes.fromhex(text).decode('utf-8', errors='ignore')
        print_colored(f"Decoded: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def url_encode(text: str) -> None:
    """URL encode"""
    print_section("URL Encode")
    try:
        result = urllib.parse.quote(text, safe='')
        print_colored(f"Encoded: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def url_decode(text: str) -> None:
    """URL decode"""
    print_section("URL Decode")
    try:
        result = urllib.parse.unquote(text)
        print_colored(f"Decoded: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def rot13(text: str) -> None:
    """ROT13 cipher"""
    print_section("ROT13")
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + 13) % 26 + base))
        else:
            result.append(char)
    print_colored(f"Result: {''.join(result)}", Fore.GREEN)
    input("\nPress Enter to continue...")


def rot_n(text: str, n: int) -> None:
    """ROT-N cipher"""
    print_section(f"ROT-{n}")
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + n) % 26 + base))
        else:
            result.append(char)
    print_colored(f"Result: {''.join(result)}", Fore.GREEN)
    input("\nPress Enter to continue...")


def binary_encode(text: str) -> None:
    """Binary encode"""
    print_section("Binary Encode")
    try:
        result = ' '.join(format(ord(c), '08b') for c in text)
        print_colored(f"Encoded: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def binary_decode(text: str) -> None:
    """Binary decode"""
    print_section("Binary Decode")
    try:
        # Remove spaces and split into 8-bit chunks
        text = text.replace(' ', '')
        result = ''.join(chr(int(text[i:i+8], 2)) for i in range(0, len(text), 8))
        print_colored(f"Decoded: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def ascii_encode(text: str) -> None:
    """ASCII encode (show decimal values)"""
    print_section("ASCII Encode")
    try:
        result = ' '.join(str(ord(c)) for c in text)
        print_colored(f"ASCII values: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def ascii_decode(text: str) -> None:
    """ASCII decode (from decimal values)"""
    print_section("ASCII Decode")
    try:
        values = text.split()
        result = ''.join(chr(int(v)) for v in values)
        print_colored(f"Decoded: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def xor_encode(text: str, key: str) -> None:
    """XOR encode"""
    print_section("XOR Encode")
    try:
        key_bytes = key.encode()
        text_bytes = text.encode()
        result = bytearray()
        for i, byte in enumerate(text_bytes):
            result.append(byte ^ key_bytes[i % len(key_bytes)])
        hex_result = result.hex()
        print_colored(f"Encoded (hex): {hex_result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def xor_decode(hex_str: str, key: str) -> None:
    """XOR decode"""
    print_section("XOR Decode")
    try:
        text_bytes = bytes.fromhex(hex_str.replace(' ', ''))
        key_bytes = key.encode()
        result = bytearray()
        for i, byte in enumerate(text_bytes):
            result.append(byte ^ key_bytes[i % len(key_bytes)])
        print_colored(f"Decoded: {result.decode('utf-8', errors='ignore')}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def encoding_menu() -> None:
    """Encoding/Decoding module menu"""
    def handle_base64_encode():
        text = get_input("Enter text to encode")
        if text:
            base64_encode(text)
    
    def handle_base64_decode():
        text = get_input("Enter text to decode")
        if text:
            base64_decode(text)
    
    def handle_base32_encode():
        text = get_input("Enter text to encode")
        if text:
            base32_encode(text)
    
    def handle_base32_decode():
        text = get_input("Enter text to decode")
        if text:
            base32_decode(text)
    
    def handle_base58_encode():
        text = get_input("Enter text to encode")
        if text:
            base58_encode(text)
    
    def handle_base58_decode():
        text = get_input("Enter text to decode")
        if text:
            base58_decode(text)
    
    def handle_base85_encode():
        text = get_input("Enter text to encode")
        if text:
            base85_encode(text)
    
    def handle_base85_decode():
        text = get_input("Enter text to decode")
        if text:
            base85_decode(text)
    
    def handle_hex_encode():
        text = get_input("Enter text to encode")
        if text:
            hex_encode(text)
    
    def handle_hex_decode():
        text = get_input("Enter hex string to decode")
        if text:
            hex_decode(text)
    
    def handle_url_encode():
        text = get_input("Enter text to encode")
        if text:
            url_encode(text)
    
    def handle_url_decode():
        text = get_input("Enter URL-encoded text to decode")
        if text:
            url_decode(text)
    
    def handle_rot13():
        text = get_input("Enter text")
        if text:
            rot13(text)
    
    def handle_rot_n():
        text = get_input("Enter text")
        try:
            n = int(get_input("Enter ROT value (0-25)", "13"))
            if text:
                rot_n(text, n)
        except ValueError:
            print_colored("Invalid ROT value.", Fore.RED)
            input("\nPress Enter to continue...")
    
    def handle_binary_encode():
        text = get_input("Enter text to encode")
        if text:
            binary_encode(text)
    
    def handle_binary_decode():
        text = get_input("Enter binary string to decode")
        if text:
            binary_decode(text)
    
    def handle_ascii_encode():
        text = get_input("Enter text to encode")
        if text:
            ascii_encode(text)
    
    def handle_ascii_decode():
        text = get_input("Enter ASCII decimal values (space-separated)")
        if text:
            ascii_decode(text)
    
    def handle_xor_encode():
        text = get_input("Enter text to encode")
        key = get_input("Enter key")
        if text and key:
            xor_encode(text, key)
    
    def handle_xor_decode():
        hex_str = get_input("Enter hex string to decode")
        key = get_input("Enter key")
        if hex_str and key:
            xor_decode(hex_str, key)
    
    options = [
        (1, "Base64 Encode", handle_base64_encode),
        (2, "Base64 Decode", handle_base64_decode),
        (3, "Base32 Encode", handle_base32_encode),
        (4, "Base32 Decode", handle_base32_decode),
        (5, "Base58 Encode", handle_base58_encode),
        (6, "Base58 Decode", handle_base58_decode),
        (7, "Base85 Encode", handle_base85_encode),
        (8, "Base85 Decode", handle_base85_decode),
        (9, "Hex Encode", handle_hex_encode),
        (10, "Hex Decode", handle_hex_decode),
        (11, "URL Encode", handle_url_encode),
        (12, "URL Decode", handle_url_decode),
        (13, "ROT13", handle_rot13),
        (14, "ROT-N", handle_rot_n),
        (15, "Binary Encode", handle_binary_encode),
        (16, "Binary Decode", handle_binary_decode),
        (17, "ASCII Encode", handle_ascii_encode),
        (18, "ASCII Decode", handle_ascii_decode),
        (19, "XOR Encode", handle_xor_encode),
        (20, "XOR Decode", handle_xor_decode),
        (0, "Back to Main Menu", lambda: None),
    ]
    
    menu = Menu("Encoding / Decoding Module", options)
    result = menu.run()
    # Return None to signal "go back to main menu" when submenu exits
    return None if result else False

