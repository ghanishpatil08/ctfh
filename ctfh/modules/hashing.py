"""Hashing module for CTF-H"""

import hashlib
from typing import Optional
from ctfh.utils import print_section, print_colored, Fore, get_input
from ctfh.menu import Menu


def hash_md5(text: str) -> None:
    """Hash text with MD5"""
    print_section("MD5 Hash")
    result = hashlib.md5(text.encode()).hexdigest()
    print_colored(f"MD5: {result}", Fore.GREEN)
    input("\nPress Enter to continue...")


def hash_sha1(text: str) -> None:
    """Hash text with SHA1"""
    print_section("SHA1 Hash")
    result = hashlib.sha1(text.encode()).hexdigest()
    print_colored(f"SHA1: {result}", Fore.GREEN)
    input("\nPress Enter to continue...")


def hash_sha256(text: str) -> None:
    """Hash text with SHA256"""
    print_section("SHA256 Hash")
    result = hashlib.sha256(text.encode()).hexdigest()
    print_colored(f"SHA256: {result}", Fore.GREEN)
    input("\nPress Enter to continue...")


def hash_sha512(text: str) -> None:
    """Hash text with SHA512"""
    print_section("SHA512 Hash")
    result = hashlib.sha512(text.encode()).hexdigest()
    print_colored(f"SHA512: {result}", Fore.GREEN)
    input("\nPress Enter to continue...")


def hash_sha3(text: str, variant: str = "sha3_256") -> None:
    """Hash text with SHA3 variants"""
    print_section(f"SHA3-{variant.split('_')[1].upper()} Hash")
    try:
        if variant == "sha3_224":
            result = hashlib.sha3_224(text.encode()).hexdigest()
        elif variant == "sha3_256":
            result = hashlib.sha3_256(text.encode()).hexdigest()
        elif variant == "sha3_384":
            result = hashlib.sha3_384(text.encode()).hexdigest()
        elif variant == "sha3_512":
            result = hashlib.sha3_512(text.encode()).hexdigest()
        else:
            print_colored("Invalid SHA3 variant", Fore.RED)
            input("\nPress Enter to continue...")
            return
        print_colored(f"SHA3-{variant.split('_')[1].upper()}: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def hash_blake2(text: str) -> None:
    """Hash text with Blake2b"""
    print_section("Blake2b Hash")
    try:
        result = hashlib.blake2b(text.encode()).hexdigest()
        print_colored(f"Blake2b: {result}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def get_text_input() -> Optional[str]:
    """Get text input from user"""
    text = get_input("Enter text to hash")
    if not text:
        print_colored("No text provided.", Fore.RED)
        return None
    return text


def hashing_menu() -> None:
    """Hashing module menu"""
    def handle_md5():
        text = get_text_input()
        if text:
            hash_md5(text)
    
    def handle_sha1():
        text = get_text_input()
        if text:
            hash_sha1(text)
    
    def handle_sha256():
        text = get_text_input()
        if text:
            hash_sha256(text)
    
    def handle_sha512():
        text = get_text_input()
        if text:
            hash_sha512(text)
    
    def handle_sha3_224():
        text = get_text_input()
        if text:
            hash_sha3(text, "sha3_224")
    
    def handle_sha3_256():
        text = get_text_input()
        if text:
            hash_sha3(text, "sha3_256")
    
    def handle_sha3_384():
        text = get_text_input()
        if text:
            hash_sha3(text, "sha3_384")
    
    def handle_sha3_512():
        text = get_text_input()
        if text:
            hash_sha3(text, "sha3_512")
    
    def handle_blake2():
        text = get_text_input()
        if text:
            hash_blake2(text)
    
    options = [
        (1, "MD5", handle_md5),
        (2, "SHA1", handle_sha1),
        (3, "SHA256", handle_sha256),
        (4, "SHA512", handle_sha512),
        (5, "SHA3-224", handle_sha3_224),
        (6, "SHA3-256", handle_sha3_256),
        (7, "SHA3-384", handle_sha3_384),
        (8, "SHA3-512", handle_sha3_512),
        (9, "Blake2b", handle_blake2),
        (0, "Back to Main Menu", lambda: None),
    ]
    
    menu = Menu("Hashing Module", options)
    menu.run()

