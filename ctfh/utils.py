"""Utility functions for CTF-H"""

import sys
from typing import Optional, List

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORAMA = True
    STYLE_RESET = Style.RESET_ALL
except ImportError:
    HAS_COLORAMA = False
    STYLE_RESET = ""
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
        RESET_ALL = ""


def print_colored(text: str, color: str = Fore.CYAN, style: str = "", end: str = "\n") -> None:
    """Print colored text"""
    if HAS_COLORAMA:
        print(f"{style}{color}{text}{STYLE_RESET}", end=end)
    else:
        print(text, end=end)


GLYPH_WIDTH = 10
GLYPH_HEIGHT = 6
# Final wordmark for the banner
BANNER_WORD = "CTF-H"
BANNER_TAGLINE = "Interactive CTF & Cybersecurity Toolkit"
BANNER_CREDIT = "by CSBC"

PIXEL_FONT = {
    " ": [" " * GLYPH_WIDTH] * GLYPH_HEIGHT,
    "C": [
        " ██████╗ ",
        "██╔════╝ ",
        "██║      ",
        "██║      ",
        "╚██████╗ ",
        " ╚═════╝ ",
    ],
    "T": [
        "████████╗",
        "╚══██╔══╝",
        "   ██║   ",
        "   ██║   ",
        "   ██║   ",
        "   ╚═╝   ",
    ],
    "F": [
        "████████╗",
        "██╔══════",
        "█████╗   ",
        "██╔══╝   ",
        "██║      ",
        "╚═╝      ",
    ],
    "-": [
        "          ",
        " ██████  ",
        "          ",
        "          ",
        "          ",
        "          ",
    ],
    "H": [
        "██╗  ██╗",
        "██║  ██║",
        "███████║",
        "██╔══██║",
        "██║  ██║",
        "╚═╝  ╚═╝",
    ],
}


def _render_pixel_word(text: str) -> List[str]:
    """Render text using the pixel font"""
    lines: List[str] = []
    for row in range(GLYPH_HEIGHT):
        segments = []
        for ch in text.upper():
            glyph = PIXEL_FONT.get(ch, PIXEL_FONT[" "])
            segments.append(glyph[row].ljust(GLYPH_WIDTH))
        lines.append("  ".join(segments).rstrip())
    return lines


def print_banner() -> None:
    """Print ASCII art banner"""
    pixel_lines = _render_pixel_word(BANNER_WORD)

    # Compute inner width based on the widest content + padding
    content_items = pixel_lines + [BANNER_TAGLINE, BANNER_CREDIT]
    content_width = max(len(item) for item in content_items)
    inner_width = max(content_width + 4, 60)  # at least 60 chars, with side padding

    def fmt_line(content: str = "", align: str = "center", pad_right: bool = False) -> str:
        """
        Format a line inside the banner.
        pad_right=True adds an extra space before the right border (for 'by CSBC').
        """
        effective_width = inner_width - (1 if pad_right else 0)

        if align == "right":
            text = content.rjust(effective_width)
        elif align == "left":
            text = content.ljust(effective_width)
        else:
            text = content.center(effective_width)

        if pad_right:
            return f"║{text} ║"
        return f"║{text}║"

    lines = [
        "╔" + "═" * inner_width + "╗",
        fmt_line(),  # top empty padding
    ]

    for row in pixel_lines:
        lines.append(fmt_line(row))

    lines.extend([
        fmt_line(),  # spacing between logo and tagline
        fmt_line(BANNER_TAGLINE),
        fmt_line(BANNER_CREDIT, align="right", pad_right=True),
        "╚" + "═" * inner_width + "╝",
    ])

    banner = "\n".join(lines)
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

