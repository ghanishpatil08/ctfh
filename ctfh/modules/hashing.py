"""Hashing module for CTF-H"""

import hashlib
import os
from typing import Optional, List
from ctfh.utils import (
    print_section, print_colored, Fore, Style, get_input, get_file_path,
    ask_copy_to_clipboard, ask_save_to_file, show_progress,
    add_to_history, get_history, get_config, get_input_with_example
)
from ctfh.menu import Menu


def hash_md5(text: str) -> None:
    """Hash text with MD5"""
    print_section("MD5 Hash")
    result = hashlib.md5(text.encode()).hexdigest()
    print_colored(f"MD5: {result}", Fore.GREEN)
    
    # Add to history
    add_to_history("hash", {"algorithm": "MD5", "input": text, "output": result})
    
    # Copy and save options
    ask_copy_to_clipboard(result)
    ask_save_to_file(f"Input: {text}\nMD5: {result}", "md5_hash", "txt")
    
    input("\nPress Enter to continue...")


def hash_sha1(text: str) -> None:
    """Hash text with SHA1"""
    print_section("SHA1 Hash")
    result = hashlib.sha1(text.encode()).hexdigest()
    print_colored(f"SHA1: {result}", Fore.GREEN)
    
    add_to_history("hash", {"algorithm": "SHA1", "input": text, "output": result})
    ask_copy_to_clipboard(result)
    ask_save_to_file(f"Input: {text}\nSHA1: {result}", "sha1_hash", "txt")
    
    input("\nPress Enter to continue...")


def hash_sha256(text: str) -> None:
    """Hash text with SHA256"""
    print_section("SHA256 Hash")
    result = hashlib.sha256(text.encode()).hexdigest()
    print_colored(f"SHA256: {result}", Fore.GREEN)
    
    add_to_history("hash", {"algorithm": "SHA256", "input": text, "output": result})
    ask_copy_to_clipboard(result)
    ask_save_to_file(f"Input: {text}\nSHA256: {result}", "sha256_hash", "txt")
    
    input("\nPress Enter to continue...")


def hash_sha512(text: str) -> None:
    """Hash text with SHA512"""
    print_section("SHA512 Hash")
    result = hashlib.sha512(text.encode()).hexdigest()
    print_colored(f"SHA512: {result}", Fore.GREEN)
    
    add_to_history("hash", {"algorithm": "SHA512", "input": text, "output": result})
    ask_copy_to_clipboard(result)
    ask_save_to_file(f"Input: {text}\nSHA512: {result}", "sha512_hash", "txt")
    
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
        
        add_to_history("hash", {"algorithm": f"SHA3-{variant.split('_')[1].upper()}", "input": text, "output": result})
        ask_copy_to_clipboard(result)
        ask_save_to_file(f"Input: {text}\nSHA3-{variant.split('_')[1].upper()}: {result}", f"sha3_{variant.split('_')[1]}_hash", "txt")
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def hash_blake2(text: str) -> None:
    """Hash text with Blake2b"""
    print_section("Blake2b Hash")
    try:
        result = hashlib.blake2b(text.encode()).hexdigest()
        print_colored(f"Blake2b: {result}", Fore.GREEN)
        
        add_to_history("hash", {"algorithm": "Blake2b", "input": text, "output": result})
        ask_copy_to_clipboard(result)
        ask_save_to_file(f"Input: {text}\nBlake2b: {result}", "blake2b_hash", "txt")
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


def hash_crack(hash_value: str, hash_type: str = "md5") -> None:
    """Crack hash using wordlist file"""
    print_section(f"Hash Cracking - {hash_type.upper()}")
    
    hash_value = hash_value.strip().lower()
    
    # Check config for default wordlist
    config = get_config()
    default_wordlist = config.get("default_wordlist", "")
    
    wordlist_path = get_input("Enter wordlist file path", default_wordlist)
    
    if not wordlist_path or not os.path.exists(wordlist_path):
        print_colored("Wordlist file is required for cracking.", Fore.RED)
        input("\nPress Enter to continue...")
        return
    
    if os.path.isdir(wordlist_path):
        print_colored("Error: Path is a directory, not a file.", Fore.RED)
        input("\nPress Enter to continue...")
        return
    
    # Count total lines for progress
    try:
        total_lines = sum(1 for _ in open(wordlist_path, 'r', encoding='utf-8', errors='ignore'))
    except Exception:
        total_lines = 0
    
    print_colored(f"\nCracking hash using wordlist: {wordlist_path}", Fore.YELLOW)
    print_colored(f"Total passwords to check: {total_lines:,}", Fore.CYAN)
    print_colored("This may take a while...\n", Fore.CYAN)
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                password = line.strip()
                if not password:
                    continue
                
                # Hash the password
                if hash_type == "md5":
                    computed = hashlib.md5(password.encode()).hexdigest()
                elif hash_type == "sha1":
                    computed = hashlib.sha1(password.encode()).hexdigest()
                elif hash_type == "sha256":
                    computed = hashlib.sha256(password.encode()).hexdigest()
                elif hash_type == "sha512":
                    computed = hashlib.sha512(password.encode()).hexdigest()
                else:
                    print_colored(f"Unsupported hash type: {hash_type}", Fore.RED)
                    input("\nPress Enter to continue...")
                    return
                
                if computed.lower() == hash_value:
                    print()  # New line after progress
                    print_colored(f"\n✓ CRACKED!", Fore.GREEN, Style.BRIGHT)
                    print_colored(f"Password: {password}", Fore.GREEN)
                    print_colored(f"Hash: {hash_value}", Fore.CYAN)
                    print_colored(f"Line: {line_num:,}", Fore.CYAN)
                    
                    # Add to history
                    add_to_history("crack", {
                        "algorithm": hash_type.upper(),
                        "hash": hash_value,
                        "password": password,
                        "wordlist": wordlist_path
                    })
                    
                    # Copy and save
                    ask_copy_to_clipboard(password)
                    ask_save_to_file(
                        f"Hash: {hash_value}\nAlgorithm: {hash_type.upper()}\nPassword: {password}\nWordlist: {wordlist_path}\nLine: {line_num}",
                        "cracked_hash", "txt"
                    )
                    
                    input("\nPress Enter to continue...")
                    return
                
                # Show progress
                if config.get("show_progress", True) and line_num % 1000 == 0:
                    show_progress(line_num, total_lines, "Cracking")
        
        print()  # New line after progress
        print_colored(f"\n✗ Hash not cracked ({line_num:,} passwords checked)", Fore.RED)
        print_colored("Try a different wordlist or use dehashing for online lookup", Fore.YELLOW)
        
        # Save failed attempt
        ask_save_to_file(
            f"Hash: {hash_value}\nAlgorithm: {hash_type.upper()}\nStatus: Not cracked\nPasswords checked: {line_num:,}\nWordlist: {wordlist_path}",
            "crack_failed", "txt"
        )
    except Exception as e:
        print_colored(f"Error reading wordlist: {e}", Fore.RED)
    
    input("\nPress Enter to continue...")


def hash_dehash(hash_value: str, hash_type: str = "md5") -> None:
    """Dehash using common passwords and online lookup methods"""
    print_section(f"Hash Dehashing - {hash_type.upper()}")
    
    hash_value = hash_value.strip().lower()
    
    print_colored("Trying common passwords and patterns...\n", Fore.YELLOW)
    
    # Common passwords database
    common_passwords = [
        "password", "123456", "12345678", "1234", "qwerty", "abc123",
        "password1", "admin", "letmein", "welcome", "monkey", "1234567",
        "dragon", "master", "hello", "freedom", "whatever", "qazwsx",
        "trustno1", "jordan23", "harley", "robert", "matthew", "jordan",
        "michelle", "charlie", "andrew", "michael", "shadow", "jennifer",
        "superman", "hunter", "buster", "soccer", "batman", "thomas",
        "tigger", "robert", "access", "thomas", "tigger", "robert",
        "love", "buster", "jessica", "daniel", "summer", "hockey",
        "ranger", "daniel", "hannah", "maggie", "joshua", "bailey",
        "amber", "oliver", "jasmine", "kelly", "justin", "guitar",
        "secret", "password123", "root", "toor", "pass", "test",
        "guest", "user", "administrator", "login", "welcome123"
    ]
    
    # Try common passwords
    print_colored("Checking common passwords...", Fore.CYAN)
    for password in common_passwords:
        if hash_type == "md5":
            computed = hashlib.md5(password.encode()).hexdigest()
        elif hash_type == "sha1":
            computed = hashlib.sha1(password.encode()).hexdigest()
        elif hash_type == "sha256":
            computed = hashlib.sha256(password.encode()).hexdigest()
        elif hash_type == "sha512":
            computed = hashlib.sha512(password.encode()).hexdigest()
        else:
            print_colored(f"Unsupported hash type: {hash_type}", Fore.RED)
            input("\nPress Enter to continue...")
            return
        
        if computed.lower() == hash_value:
            print_colored(f"\n✓ DEHASHED!", Fore.GREEN)
            print_colored(f"Password: {password}", Fore.GREEN)
            print_colored(f"Hash: {hash_value}", Fore.CYAN)
            input("\nPress Enter to continue...")
            return
    
    print_colored(f"\n✗ Not found in common passwords", Fore.RED)
    
    # Suggest online lookup
    print_colored("\nOnline lookup suggestions:", Fore.YELLOW)
    print_colored(f"  - MD5: https://md5decrypt.net/en/", Fore.CYAN)
    print_colored(f"  - SHA1: https://sha1.gromweb.com/", Fore.CYAN)
    print_colored(f"  - SHA256: https://md5decrypt.net/Sha256/", Fore.CYAN)
    print_colored(f"  - Or use hash cracking with a wordlist file", Fore.CYAN)
    
    input("\nPress Enter to continue...")


def hash_compare(hash1: str, hash2: str) -> None:
    """Compare two hashes"""
    print_section("Hash Comparison")
    
    hash1 = hash1.strip().lower()
    hash2 = hash2.strip().lower()
    
    from ctfh.utils import print_table
    
    if hash1 == hash2:
        print_colored("✓ Hashes MATCH!", Fore.GREEN, Style.BRIGHT)
        print_table(
            ["Hash 1", "Hash 2", "Status"],
            [[hash1, hash2, "MATCH"]]
        )
    else:
        print_colored("✗ Hashes DO NOT match", Fore.RED)
        print_table(
            ["Hash 1", "Hash 2", "Status"],
            [[hash1, hash2, "NO MATCH"]]
        )
    
    add_to_history("compare", {"hash1": hash1, "hash2": hash2, "match": hash1 == hash2})
    
    input("\nPress Enter to continue...")


def hash_batch(texts: List[str], algorithm: str = "md5") -> None:
    """Hash multiple strings at once"""
    print_section(f"Batch Hashing - {algorithm.upper()}")
    
    results = []
    for text in texts:
        if algorithm == "md5":
            result = hashlib.md5(text.encode()).hexdigest()
        elif algorithm == "sha1":
            result = hashlib.sha1(text.encode()).hexdigest()
        elif algorithm == "sha256":
            result = hashlib.sha256(text.encode()).hexdigest()
        elif algorithm == "sha512":
            result = hashlib.sha512(text.encode()).hexdigest()
        else:
            print_colored(f"Unsupported algorithm: {algorithm}", Fore.RED)
            return
        results.append((text, result))
    
    from ctfh.utils import print_table
    print_table(
        ["Input", f"{algorithm.upper()} Hash"],
        [[text, hash_val] for text, hash_val in results]
    )
    
    # Save results
    output = "\n".join([f"{text}\t{hash_val}" for text, hash_val in results])
    ask_save_to_file(output, f"batch_{algorithm}_hashes", "txt")
    
    input("\nPress Enter to continue...")


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
    
    def handle_hash_crack_md5():
        hash_val = get_input("Enter MD5 hash to crack")
        if hash_val:
            hash_crack(hash_val, "md5")
    
    def handle_hash_crack_sha1():
        hash_val = get_input("Enter SHA1 hash to crack")
        if hash_val:
            hash_crack(hash_val, "sha1")
    
    def handle_hash_crack_sha256():
        hash_val = get_input("Enter SHA256 hash to crack")
        if hash_val:
            hash_crack(hash_val, "sha256")
    
    def handle_hash_crack_sha512():
        hash_val = get_input("Enter SHA512 hash to crack")
        if hash_val:
            hash_crack(hash_val, "sha512")
    
    def handle_hash_dehash_md5():
        hash_val = get_input("Enter MD5 hash to dehash")
        if hash_val:
            hash_dehash(hash_val, "md5")
    
    def handle_hash_dehash_sha1():
        hash_val = get_input("Enter SHA1 hash to dehash")
        if hash_val:
            hash_dehash(hash_val, "sha1")
    
    def handle_hash_dehash_sha256():
        hash_val = get_input("Enter SHA256 hash to dehash")
        if hash_val:
            hash_dehash(hash_val, "sha256")
    
    def handle_hash_dehash_sha512():
        hash_val = get_input("Enter SHA512 hash to dehash")
        if hash_val:
            hash_dehash(hash_val, "sha512")
    
    def handle_hash_compare():
        hash1 = get_input("Enter first hash")
        hash2 = get_input("Enter second hash")
        if hash1 and hash2:
            hash_compare(hash1, hash2)
    
    def handle_batch_hash():
        print_section("Batch Hashing")
        print_colored("Enter multiple strings to hash (one per line, empty line to finish):", Fore.YELLOW)
        texts = []
        while True:
            text = input("> ").strip()
            if not text:
                break
            texts.append(text)
        
        if not texts:
            print_colored("No input provided.", Fore.RED)
            input("\nPress Enter to continue...")
            return
        
        algo = get_input("Select algorithm (md5/sha1/sha256/sha512)", "md5").lower()
        if algo not in ["md5", "sha1", "sha256", "sha512"]:
            print_colored("Invalid algorithm.", Fore.RED)
            input("\nPress Enter to continue...")
            return
        
        hash_batch(texts, algo)
    
    def handle_show_history():
        print_section("Recent Hash Operations")
        history = get_history("hash", 10)
        if history:
            from ctfh.utils import print_table
            rows = []
            for h in reversed(history):
                data = h.get("data", {})
                rows.append([
                    data.get("algorithm", "N/A"),
                    data.get("input", "N/A")[:30] + "..." if len(data.get("input", "")) > 30 else data.get("input", "N/A"),
                    data.get("output", "N/A")[:20] + "..." if len(data.get("output", "")) > 20 else data.get("output", "N/A")
                ])
            print_table(["Algorithm", "Input", "Hash"], rows)
        else:
            print_colored("No history available.", Fore.YELLOW)
        input("\nPress Enter to continue...")
    
    def handle_help():
        help_text = """
Hashing Module Help
===================

Hash Functions (Options 1-9):
  - Generate one-way hashes from text input
  - Results can be copied to clipboard or saved to file
  - Supported: MD5, SHA1, SHA256, SHA512, SHA3 variants, Blake2b

Hash Cracking (Options 10-13):
  - Crack hashes using wordlist files
  - Requires a wordlist file (e.g., rockyou.txt)
  - Shows progress bar during cracking
  - Saves results automatically

Hash Dehashing (Options 14-17):
  - Quick lookup using common passwords database
  - No wordlist required
  - Suggests online lookup sites if not found

Other Features:
  - Compare Two Hashes: Check if two hashes match
  - Batch Hashing: Hash multiple strings at once
  - History: View recent hash operations

Tips:
  - Use wordlist cracking for best results
  - Common passwords work for weak passwords only
  - All results can be saved to files
  - Press ? in any menu for help
        """
        print_colored(help_text, Fore.CYAN)
        input("\nPress Enter to continue...")
    
    options = [
        (1, "MD5 Hash", handle_md5),
        (2, "SHA1 Hash", handle_sha1),
        (3, "SHA256 Hash", handle_sha256),
        (4, "SHA512 Hash", handle_sha512),
        (5, "SHA3-224 Hash", handle_sha3_224),
        (6, "SHA3-256 Hash", handle_sha3_256),
        (7, "SHA3-384 Hash", handle_sha3_384),
        (8, "SHA3-512 Hash", handle_sha3_512),
        (9, "Blake2b Hash", handle_blake2),
        (10, "MD5 Crack (Wordlist)", handle_hash_crack_md5),
        (11, "SHA1 Crack (Wordlist)", handle_hash_crack_sha1),
        (12, "SHA256 Crack (Wordlist)", handle_hash_crack_sha256),
        (13, "SHA512 Crack (Wordlist)", handle_hash_crack_sha512),
        (14, "MD5 Dehash (Common Passwords)", handle_hash_dehash_md5),
        (15, "SHA1 Dehash (Common Passwords)", handle_hash_dehash_sha1),
        (16, "SHA256 Dehash (Common Passwords)", handle_hash_dehash_sha256),
        (17, "SHA512 Dehash (Common Passwords)", handle_hash_dehash_sha512),
        (18, "Compare Two Hashes", handle_hash_compare),
        (19, "Batch Hashing", handle_batch_hash),
        (20, "View History", handle_show_history),
        (99, "Help (?)", handle_help),
        (0, "Back to Main Menu", lambda: None),
    ]
    
    menu = Menu("Hashing Module", options)
    result = menu.run()
    # Return None to signal "go back to main menu" when submenu exits
    return None if result else False

