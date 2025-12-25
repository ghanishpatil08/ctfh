"""Binary analysis module for CTF-H"""

import os
import subprocess
import math
from typing import Optional
from ctfh.utils import print_section, print_colored, Fore, get_file_path, get_input
from ctfh.menu import Menu


def calculate_entropy(data: bytes) -> float:
    """Calculate Shannon entropy of data"""
    if not data:
        return 0
    
    entropy = 0
    for x in range(256):
        p_x = float(data.count(bytes([x]))) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    return entropy


def file_info(file_path: str) -> None:
    """Display file metadata"""
    print_section("File Information")
    try:
        stat = os.stat(file_path)
        size = stat.st_size
        
        print_colored(f"File: {file_path}", Fore.GREEN)
        print_colored(f"Size: {size} bytes ({size/1024:.2f} KB)", Fore.CYAN)
        print_colored(f"Modified: {os.path.getmtime(file_path)}", Fore.CYAN)
        
        # Try to determine file type
        import mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            print_colored(f"MIME type: {mime_type}", Fore.CYAN)
        
        # Check if executable
        if os.access(file_path, os.X_OK):
            print_colored("Executable: Yes", Fore.YELLOW)
        
        # Calculate entropy
        with open(file_path, 'rb') as f:
            data = f.read()
            entropy = calculate_entropy(data)
            print_colored(f"Entropy: {entropy:.4f} (max 8.0)", Fore.CYAN)
            if entropy > 7.5:
                print_colored("  High entropy - possibly encrypted/compressed", Fore.YELLOW)
        
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def extract_strings(file_path: str, min_length: int = 4) -> None:
    """Extract printable strings from binary"""
    print_section("Strings Extraction")
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        strings = []
        current_string = ""
        
        for byte in data:
            if 32 <= byte <= 126:  # Printable ASCII
                current_string += chr(byte)
            else:
                if len(current_string) >= min_length:
                    strings.append(current_string)
                current_string = ""
        
        if len(current_string) >= min_length:
            strings.append(current_string)
        
        print_colored(f"Found {len(strings)} strings (min length: {min_length}):\n", Fore.GREEN)
        
        # Show first 100 strings
        for i, s in enumerate(strings[:100], 1):
            print_colored(f"{i:4d}: {s}", Fore.CYAN)
        
        if len(strings) > 100:
            print_colored(f"\n... ({len(strings) - 100} more strings)", Fore.YELLOW)
        
        # Option to save to file
        save = get_input("\nSave all strings to file? (y/n)", "n")
        if save.lower() == 'y':
            output = get_input("Enter output file path", "strings_output.txt")
            if output:
                with open(output, 'w') as f:
                    f.write('\n'.join(strings))
                print_colored(f"Strings saved to {output}", Fore.GREEN)
        
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def objdump_preview(file_path: str) -> None:
    """Preview objdump output if available"""
    print_section("Objdump Preview")
    try:
        # Check if objdump is available
        result = subprocess.run(['objdump', '--version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        
        if result.returncode != 0:
            print_colored("objdump not found. Install binutils package.", Fore.YELLOW)
            input("\nPress Enter to continue...")
            return
        
        # Run objdump
        result = subprocess.run(['objdump', '-d', file_path],
                              capture_output=True,
                              text=True,
                              timeout=10)
        
        if result.returncode == 0:
            output = result.stdout
            print_colored("Objdump output (first 100 lines):\n", Fore.GREEN)
            lines = output.split('\n')[:100]
            for line in lines:
                print_colored(line, Fore.CYAN)
            if len(output.split('\n')) > 100:
                print_colored("\n... (truncated)", Fore.YELLOW)
        else:
            print_colored(f"Error: {result.stderr}", Fore.RED)
        
    except FileNotFoundError:
        print_colored("objdump not found. Install binutils package.", Fore.YELLOW)
    except subprocess.TimeoutExpired:
        print_colored("objdump timed out.", Fore.RED)
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def entropy_check(file_path: str) -> None:
    """Check file entropy"""
    print_section("Entropy Check")
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        entropy = calculate_entropy(data)
        
        print_colored(f"File: {file_path}", Fore.GREEN)
        print_colored(f"Size: {len(data)} bytes", Fore.CYAN)
        print_colored(f"Entropy: {entropy:.4f} / 8.0", Fore.CYAN)
        
        # Interpretation
        if entropy < 4.0:
            print_colored("Interpretation: Low entropy - likely text or structured data", Fore.GREEN)
        elif entropy < 6.0:
            print_colored("Interpretation: Medium entropy - normal binary data", Fore.YELLOW)
        elif entropy < 7.5:
            print_colored("Interpretation: High entropy - possibly compressed", Fore.YELLOW)
        else:
            print_colored("Interpretation: Very high entropy - possibly encrypted or random", Fore.RED)
        
        # Calculate entropy per block (for detecting sections)
        block_size = 1024
        if len(data) > block_size:
            print_colored(f"\nEntropy by {block_size}-byte blocks:", Fore.YELLOW)
            for i in range(0, min(len(data), 5 * block_size), block_size):
                block = data[i:i+block_size]
                block_entropy = calculate_entropy(block)
                print_colored(f"  Block {i//block_size}: {block_entropy:.4f}", Fore.CYAN)
        
    except Exception as e:
        print_colored(f"Error: {e}", Fore.RED)
    input("\nPress Enter to continue...")


def binary_menu() -> None:
    """Binary analysis module menu"""
    def handle_file_info():
        path = get_file_path("Enter file path")
        if path:
            file_info(path)
    
    def handle_strings():
        path = get_file_path("Enter file path")
        if path:
            try:
                min_len = int(get_input("Minimum string length", "4"))
                extract_strings(path, min_len)
            except ValueError:
                print_colored("Invalid length.", Fore.RED)
                input("\nPress Enter to continue...")
    
    def handle_objdump():
        path = get_file_path("Enter binary file path")
        if path:
            objdump_preview(path)
    
    def handle_entropy():
        path = get_file_path("Enter file path")
        if path:
            entropy_check(path)
    
    options = [
        (1, "File Information", handle_file_info),
        (2, "Extract Strings", handle_strings),
        (3, "Objdump Preview", handle_objdump),
        (4, "Entropy Check", handle_entropy),
        (0, "Back to Main Menu", lambda: None),
    ]
    
    menu = Menu("Binary Analysis Module", options)
    result = menu.run()
    # Return None to signal "go back to main menu" when submenu exits
    return None if result else False

