"""Main entry point for CTF-H"""

import hashlib
import base64
from ctfh.menu import Menu
from ctfh.utils import print_section, print_colored, Fore, get_input, ask_copy_to_clipboard
from ctfh.modules import hashing, ciphers, encoding, steganography, binary, vulnerability, javascript, fuzzing


def quick_hash():
    """Quick hash operation"""
    print_section("Quick Hash")
    text = get_input("Enter text to hash")
    if not text:
        return
    
    algo = get_input("Algorithm (md5/sha256)", "md5").lower()
    
    if algo == "md5":
        result = hashlib.md5(text.encode()).hexdigest()
    elif algo == "sha256":
        result = hashlib.sha256(text.encode()).hexdigest()
    else:
        print_colored("Invalid algorithm. Use md5 or sha256", Fore.RED)
        input("\nPress Enter to continue...")
        return
    
    print_colored(f"{algo.upper()}: {result}", Fore.GREEN)
    ask_copy_to_clipboard(result)
    input("\nPress Enter to continue...")


def quick_encode():
    """Quick encode/decode operation"""
    print_section("Quick Encode/Decode")
    text = get_input("Enter text")
    if not text:
        return
    
    op = get_input("Operation (encode/decode)", "encode").lower()
    fmt = get_input("Format (base64/hex/url)", "base64").lower()
    
    try:
        if fmt == "base64":
            if op == "encode":
                result = base64.b64encode(text.encode()).decode()
            else:
                result = base64.b64decode(text.encode()).decode('utf-8', errors='ignore')
        elif fmt == "hex":
            if op == "encode":
                result = text.encode().hex()
            else:
                result = bytes.fromhex(text.replace(' ', '')).decode('utf-8', errors='ignore')
        elif fmt == "url":
            import urllib.parse
            if op == "encode":
                result = urllib.parse.quote(text, safe='')
            else:
                result = urllib.parse.unquote(text)
        else:
            print_colored("Invalid format.", Fore.RED)
            input("\nPress Enter to continue...")
            return
        
        print_colored(f"Result: {result}", Fore.GREEN)
        ask_copy_to_clipboard(result)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    
    input("\nPress Enter to continue...")


def quick_actions_menu() -> None:
    """Quick actions menu for common operations"""
    options = [
        (1, "Quick Hash (MD5/SHA256)", quick_hash),
        (2, "Quick Encode/Decode (Base64/Hex/URL)", quick_encode),
        (0, "Back to Main Menu", lambda: None),
    ]
    
    menu = Menu("Quick Actions", options)
    result = menu.run()
    return None if result else False


def main():
    """Main entry point"""
    modules = {
        'hashing': hashing.hashing_menu,
        'ciphers': ciphers.ciphers_menu,
        'encoding': encoding.encoding_menu,
        'steganography': steganography.steganography_menu,
        'binary': binary.binary_menu,
        'vulnerability': vulnerability.vulnerability_menu,
        'javascript': javascript.javascript_menu,
        'fuzzing': fuzzing.fuzzing_menu,
        'quick': quick_actions_menu,
    }
    
    from ctfh.menu import create_main_menu
    menu = create_main_menu(modules)
    menu.run()


if __name__ == '__main__':
    main()

