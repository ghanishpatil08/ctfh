"""Utility functions for CTF-H"""

import sys
from typing import Optional

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    # Fallback colors (no-op if colorama not available)
    class Fore:
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        MAGENTA = ""
        CYAN = ""
        RESET = ""
    class Style:
        BRIGHT = ""
        RESET = ""


def print_colored(text: str, color: str = Fore.CYAN, style: str = "", end: str = "\n") -> None:
    """Print colored text"""
    if HAS_COLORAMA:
        print(f"{style}{color}{text}{Style.RESET}", end=end)
    else:
        print(text, end=end)


def print_banner() -> None:
    """Print ASCII art banner"""
    banner = """
╔═══════════════════════════════════════════════════════╗
║  ██████╗████████╗███████╗██╗  ██╗                    ║
║  ██╔════╝╚══██╔══╝██╔════╝██║ ██╔╝                    ║
║  ██║      ██║   ███████╗█████╔╝                     ║
║  ██║      ██║   ╚════██║██╔═██╗                     ║
║  ╚██████╗ ██║   ███████║██║  ██╗                    ║
║   ╚═════╝ ╚═╝   ╚══════╝╚═╝  ╚═╝                    ║
║                                                       ║
║     Interactive CTF & Cybersecurity Toolkit          ║
╚═══════════════════════════════════════════════════════╝
"""
    print_colored(banner, Fore.CYAN, Style.BRIGHT)


def clear_screen() -> None:
    """Clear the terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def get_input(prompt: str, default: Optional[str] = None) -> str:
    """Get user input with optional default"""
    if default:
        full_prompt = f"{prompt} [{default}]: "
    else:
        full_prompt = f"{prompt}: "
    
    result = input(full_prompt).strip()
    return result if result else (default or "")


def get_file_path(prompt: str = "Enter file path") -> str:
    """Get file path from user with validation"""
    import os
    while True:
        path = get_input(prompt)
        if os.path.exists(path):
            return path
        print_colored(f"Error: File '{path}' not found. Please try again.", Fore.RED)


def print_section(title: str) -> None:
    """Print a section header"""
    print()
    print_colored("=" * 60, Fore.CYAN)
    print_colored(f"  {title}", Fore.CYAN, Style.BRIGHT)
    print_colored("=" * 60, Fore.CYAN)
    print()

