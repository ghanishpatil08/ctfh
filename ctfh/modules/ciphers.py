"""Cipher module for CTF-H"""

import string
from collections import Counter
from typing import Optional
from ctfh.utils import print_section, print_colored, Fore, get_input
from ctfh.menu import Menu


def caesar_encrypt(text: str, shift: int) -> str:
    """Encrypt text using Caesar cipher"""
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    """Decrypt text using Caesar cipher"""
    return caesar_encrypt(text, -shift)


def caesar_bruteforce(text: str) -> None:
    """Bruteforce Caesar cipher"""
    print_section("Caesar Cipher Bruteforce")
    print_colored("Trying all 26 shifts:\n", Fore.YELLOW)
    for shift in range(26):
        decrypted = caesar_decrypt(text, shift)
        print_colored(f"Shift {shift:2d}: {decrypted}", Fore.CYAN)
    input("\nPress Enter to continue...")


def vigenere_encrypt(text: str, key: str) -> str:
    """Encrypt text using Vigenère cipher"""
    key = key.upper()
    key_index = 0
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('A')
            result.append(chr((ord(char) - base + shift) % 26 + base))
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)


def vigenere_decrypt(text: str, key: str) -> str:
    """Decrypt text using Vigenère cipher"""
    key = key.upper()
    key_index = 0
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('A')
            result.append(chr((ord(char) - base - shift) % 26 + base))
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)


def atbash_cipher(text: str) -> str:
    """Apply Atbash cipher"""
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr(25 - (ord(char) - base) + base))
        else:
            result.append(char)
    return ''.join(result)


def xor_cipher(text: str, key: str) -> str:
    """XOR cipher"""
    key_bytes = key.encode()
    text_bytes = text.encode()
    result = bytearray()
    for i, byte in enumerate(text_bytes):
        result.append(byte ^ key_bytes[i % len(key_bytes)])
    return result.hex()


def xor_decipher(hex_str: str, key: str) -> str:
    """XOR decipher"""
    try:
        text_bytes = bytes.fromhex(hex_str)
        key_bytes = key.encode()
        result = bytearray()
        for i, byte in enumerate(text_bytes):
            result.append(byte ^ key_bytes[i % len(key_bytes)])
        return result.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Error: {e}"


def rail_fence_encrypt(text: str, rails: int) -> str:
    """Rail Fence cipher encryption"""
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    
    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction = -direction
    
    return ''.join(''.join(row) for row in fence)


def rail_fence_decrypt(cipher: str, rails: int) -> str:
    """Rail Fence cipher decryption"""
    fence = [[''] * len(cipher) for _ in range(rails)]
    rail = 0
    direction = 1
    
    # Mark positions
    for i in range(len(cipher)):
        fence[rail][i] = '*'
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction = -direction
    
    # Fill in the cipher text
    index = 0
    for row in fence:
        for j in range(len(cipher)):
            if row[j] == '*' and index < len(cipher):
                row[j] = cipher[index]
                index += 1
    
    # Read the result
    rail = 0
    direction = 1
    result = []
    for i in range(len(cipher)):
        result.append(fence[rail][i])
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction = -direction
    
    return ''.join(result)


def frequency_analysis(text: str) -> None:
    """Perform frequency analysis on text"""
    print_section("Frequency Analysis")
    text_upper = text.upper()
    letters = [c for c in text_upper if c.isalpha()]
    
    if not letters:
        print_colored("No letters found in text.", Fore.RED)
        input("\nPress Enter to continue...")
        return
    
    counter = Counter(letters)
    total = len(letters)
    
    print_colored("Letter frequencies:\n", Fore.YELLOW)
    for letter, count in counter.most_common():
        percentage = (count / total) * 100
        bar = '█' * int(percentage / 2)
        print_colored(f"{letter}: {count:4d} ({percentage:5.2f}%) {bar}", Fore.CYAN)
    
    # English letter frequency order (most common)
    english_order = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
    print_colored("\nMost common letters (English order: ETAOINSHRDLCUMWFGYPBVKJXQZ)", Fore.YELLOW)
    input("\nPress Enter to continue...")


def ciphers_menu() -> None:
    """Cipher module menu"""
    def handle_caesar_encrypt():
        print_section("Caesar Cipher - Encrypt")
        text = get_input("Enter text to encrypt")
        try:
            shift = int(get_input("Enter shift (0-25)", "13"))
            result = caesar_encrypt(text, shift)
            print_colored(f"\nEncrypted: {result}", Fore.GREEN)
        except ValueError:
            print_colored("Invalid shift value.", Fore.RED)
        input("\nPress Enter to continue...")
    
    def handle_caesar_decrypt():
        print_section("Caesar Cipher - Decrypt")
        text = get_input("Enter text to decrypt")
        try:
            shift = int(get_input("Enter shift (0-25)", "13"))
            result = caesar_decrypt(text, shift)
            print_colored(f"\nDecrypted: {result}", Fore.GREEN)
        except ValueError:
            print_colored("Invalid shift value.", Fore.RED)
        input("\nPress Enter to continue...")
    
    def handle_caesar_bruteforce():
        text = get_input("Enter text to bruteforce")
        if text:
            caesar_bruteforce(text)
    
    def handle_vigenere_encrypt():
        print_section("Vigenère Cipher - Encrypt")
        text = get_input("Enter text to encrypt")
        key = get_input("Enter key")
        if text and key:
            result = vigenere_encrypt(text, key)
            print_colored(f"\nEncrypted: {result}", Fore.GREEN)
            input("\nPress Enter to continue...")
    
    def handle_vigenere_decrypt():
        print_section("Vigenère Cipher - Decrypt")
        text = get_input("Enter text to decrypt")
        key = get_input("Enter key")
        if text and key:
            result = vigenere_decrypt(text, key)
            print_colored(f"\nDecrypted: {result}", Fore.GREEN)
            input("\nPress Enter to continue...")
    
    def handle_atbash():
        print_section("Atbash Cipher")
        text = get_input("Enter text")
        if text:
            result = atbash_cipher(text)
            print_colored(f"\nResult: {result}", Fore.GREEN)
            input("\nPress Enter to continue...")
    
    def handle_xor_encrypt():
        print_section("XOR Cipher - Encrypt")
        text = get_input("Enter text to encrypt")
        key = get_input("Enter key")
        if text and key:
            result = xor_cipher(text, key)
            print_colored(f"\nEncrypted (hex): {result}", Fore.GREEN)
            input("\nPress Enter to continue...")
    
    def handle_xor_decrypt():
        print_section("XOR Cipher - Decrypt")
        hex_str = get_input("Enter hex string to decrypt")
        key = get_input("Enter key")
        if hex_str and key:
            result = xor_decipher(hex_str, key)
            print_colored(f"\nDecrypted: {result}", Fore.GREEN)
            input("\nPress Enter to continue...")
    
    def handle_rail_fence_encrypt():
        print_section("Rail Fence Cipher - Encrypt")
        text = get_input("Enter text to encrypt")
        try:
            rails = int(get_input("Enter number of rails", "3"))
            result = rail_fence_encrypt(text, rails)
            print_colored(f"\nEncrypted: {result}", Fore.GREEN)
        except ValueError:
            print_colored("Invalid number of rails.", Fore.RED)
        input("\nPress Enter to continue...")
    
    def handle_rail_fence_decrypt():
        print_section("Rail Fence Cipher - Decrypt")
        text = get_input("Enter text to decrypt")
        try:
            rails = int(get_input("Enter number of rails", "3"))
            result = rail_fence_decrypt(text, rails)
            print_colored(f"\nDecrypted: {result}", Fore.GREEN)
        except ValueError:
            print_colored("Invalid number of rails.", Fore.RED)
        input("\nPress Enter to continue...")
    
    def handle_frequency_analysis():
        text = get_input("Enter text for frequency analysis")
        if text:
            frequency_analysis(text)
    
    options = [
        (1, "Caesar - Encrypt", handle_caesar_encrypt),
        (2, "Caesar - Decrypt", handle_caesar_decrypt),
        (3, "Caesar - Bruteforce", handle_caesar_bruteforce),
        (4, "Vigenère - Encrypt", handle_vigenere_encrypt),
        (5, "Vigenère - Decrypt", handle_vigenere_decrypt),
        (6, "Atbash", handle_atbash),
        (7, "XOR - Encrypt", handle_xor_encrypt),
        (8, "XOR - Decrypt", handle_xor_decrypt),
        (9, "Rail Fence - Encrypt", handle_rail_fence_encrypt),
        (10, "Rail Fence - Decrypt", handle_rail_fence_decrypt),
        (11, "Frequency Analysis", handle_frequency_analysis),
        (0, "Back to Main Menu", lambda: None),
    ]
    
    menu = Menu("Cipher Module", options)
    result = menu.run()
    # Return None to signal "go back to main menu" when submenu exits
    return None if result else False

