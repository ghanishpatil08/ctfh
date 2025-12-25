"""Utility functions for CTF-H"""

import sys
import os
import json
import csv
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

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


# ==================== Clipboard Functions ====================

def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard"""
    try:
        if os.name == 'nt':  # Windows
            import subprocess
            subprocess.run(['clip'], input=text.encode('utf-8'), check=True)
            return True
        else:  # Linux/macOS
            try:
                import subprocess
                subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode('utf-8'), check=True)
                return True
            except FileNotFoundError:
                try:
                    import subprocess
                    subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=True)
                    return True
                except FileNotFoundError:
                    return False
    except Exception:
        return False


def ask_copy_to_clipboard(text: str, prompt: str = "Copy to clipboard? (y/n)") -> bool:
    """Ask user if they want to copy text to clipboard"""
    response = get_input(prompt, "n").lower()
    if response == 'y':
        if copy_to_clipboard(text):
            print_colored("✓ Copied to clipboard!", Fore.GREEN)
            return True
        else:
            print_colored("✗ Failed to copy to clipboard (clipboard tool not available)", Fore.YELLOW)
            return False
    return False


# ==================== Save to File Functions ====================

def save_to_file(content: str, default_filename: str, file_type: str = "txt") -> Optional[str]:
    """Save content to file with user prompt"""
    filename = get_input(f"Enter filename to save ({file_type})", default_filename)
    if not filename:
        return None
    
    # Add extension if not present
    if not filename.endswith(f'.{file_type}'):
        filename += f'.{file_type}'
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print_colored(f"✓ Saved to: {filename}", Fore.GREEN)
        return filename
    except Exception as e:
        print_colored(f"✗ Error saving file: {e}", Fore.RED)
        return None


def ask_save_to_file(content: str, default_filename: str, file_type: str = "txt", prompt: str = "Save to file? (y/n)") -> Optional[str]:
    """Ask user if they want to save content to file"""
    response = get_input(prompt, "n").lower()
    if response == 'y':
        return save_to_file(content, default_filename, file_type)
    return None


# ==================== Progress Indicator ====================

def show_progress(current: int, total: int, prefix: str = "Progress", bar_length: int = 40) -> None:
    """Show progress bar"""
    if total == 0:
        return
    
    percent = float(current) / total
    filled = int(bar_length * percent)
    bar = '█' * filled + '░' * (bar_length - filled)
    
    print_colored(f"\r{prefix}: [{bar}] {percent*100:.1f}% ({current}/{total})", Fore.CYAN, end="")
    if current >= total:
        print()  # New line when complete


# ==================== Table Formatting ====================

def print_table(headers: List[str], rows: List[List[str]], max_col_width: int = 50) -> None:
    """Print a formatted table"""
    if not headers or not rows:
        return
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], min(len(str(cell)), max_col_width))
    
    # Create separator
    sep = "─" * (sum(col_widths) + len(headers) * 3 + 1)
    
    # Print header
    header_row = "│ " + " │ ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " │"
    print_colored("┌" + sep + "┐", Fore.CYAN)
    print_colored(header_row, Fore.YELLOW, Style.BRIGHT)
    print_colored("├" + sep + "┤", Fore.CYAN)
    
    # Print rows
    for row in rows:
        row_str = "│ " + " │ ".join(str(cell)[:max_col_width].ljust(col_widths[i]) for i, cell in enumerate(row)) + " │"
        print_colored(row_str, Fore.CYAN)
    
    print_colored("└" + sep + "┘", Fore.CYAN)


# ==================== Configuration Management ====================

CONFIG_DIR = Path.home() / ".ctfh"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"

def get_config() -> Dict[str, Any]:
    """Load user configuration"""
    default_config = {
        "default_wordlist": "",
        "default_extensions": [".py", ".js", ".html", ".php"],
        "auto_copy": False,
        "auto_save": False,
        "theme": "default",
        "show_progress": True,
    }
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except Exception:
            pass
    
    # Ensure config directory exists
    CONFIG_DIR.mkdir(exist_ok=True)
    
    return default_config


def save_config(config: Dict[str, Any]) -> None:
    """Save user configuration"""
    try:
        CONFIG_DIR.mkdir(exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception:
        pass


# ==================== History Management ====================

def add_to_history(operation_type: str, data: Dict[str, Any]) -> None:
    """Add operation to history"""
    try:
        CONFIG_DIR.mkdir(exist_ok=True)
        
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        history.append({
            "timestamp": datetime.now().isoformat(),
            "type": operation_type,
            "data": data
        })
        
        # Keep only last 50 entries
        history = history[-50:]
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass


def get_history(operation_type: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Get operation history"""
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
                if operation_type:
                    history = [h for h in history if h.get("type") == operation_type]
                return history[-limit:]
    except Exception:
        pass
    return []


# ==================== Export Functions ====================

def export_to_json(data: Any, filename: str) -> bool:
    """Export data to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def export_to_csv(headers: List[str], rows: List[List[str]], filename: str) -> bool:
    """Export data to CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        return True
    except Exception:
        return False


def export_to_html(title: str, content: str, filename: str) -> bool:
    """Export content to HTML file"""
    try:
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: monospace; margin: 20px; background: #1e1e1e; color: #d4d4d4; }}
        pre {{ background: #252526; padding: 15px; border-radius: 5px; }}
        h1 {{ color: #4ec9b0; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <pre>{content}</pre>
    <p><small>Generated by CTF-H on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
</body>
</html>"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    except Exception:
        return False


# ==================== Input Validation ====================

def get_input_with_example(prompt: str, example: str, default: Optional[str] = None) -> str:
    """Get input with example shown"""
    if example:
        print_colored(f"Example: {example}", Fore.YELLOW, Style.BRIGHT)
    return get_input(prompt, default)


def validate_file_path(path: str, must_exist: bool = True, must_be_file: bool = True) -> tuple[bool, Optional[str]]:
    """Validate file path and return (is_valid, error_message)"""
    if not path:
        return False, "Path is empty"
    
    if must_exist and not os.path.exists(path):
        return False, f"Path does not exist: {path}"
    
    if must_be_file and os.path.isdir(path):
        return False, f"Path is a directory, not a file: {path}"
    
    if must_be_file and not os.path.isfile(path):
        return False, f"Path is not a valid file: {path}"
    
    return True, None

