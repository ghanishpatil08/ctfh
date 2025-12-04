"""JavaScript tools module for CTF-H"""

import re
from typing import List, Tuple
from ctfh.utils import print_section, print_colored, Fore, get_file_path, get_input
from ctfh.menu import Menu

try:
    import jsbeautifier
    HAS_JSBEAUTIFIER = True
except ImportError:
    HAS_JSBEAUTIFIER = False

# JavaScript sink patterns (XSS, code injection risks)
JS_SINKS = [
    (r'eval\s*\(', 'eval() - Code injection'),
    (r'Function\s*\(', 'Function() constructor - Code injection'),
    (r'setTimeout\s*\(', 'setTimeout() - Code injection'),
    (r'setInterval\s*\(', 'setInterval() - Code injection'),
    (r'innerHTML\s*=', 'innerHTML - XSS'),
    (r'outerHTML\s*=', 'outerHTML - XSS'),
    (r'document\.write\s*\(', 'document.write() - XSS'),
    (r'document\.writeln\s*\(', 'document.writeln() - XSS'),
    (r'\.insertAdjacentHTML\s*\(', 'insertAdjacentHTML() - XSS'),
    (r'location\s*=', 'location assignment - Open redirect'),
    (r'location\.href\s*=', 'location.href - Open redirect'),
    (r'location\.replace\s*\(', 'location.replace() - Open redirect'),
    (r'dangerouslySetInnerHTML', 'React dangerouslySetInnerHTML - XSS'),
    (r'\.html\s*\(', 'jQuery .html() - XSS'),
    (r'\.append\s*\(', 'jQuery .append() - Potential XSS'),
]


def prettify_js(code: str) -> None:
    """Prettify JavaScript code"""
    print_section("JavaScript Prettifier")
    
    if not HAS_JSBEAUTIFIER:
        print_colored("jsbeautifier not installed. Install with: pip install jsbeautifier", Fore.RED)
        print_colored("\nAttempting basic formatting...", Fore.YELLOW)
        
        # Basic formatting fallback
        lines = code.split('\n')
        formatted = []
        indent = 0
        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted.append('')
                continue
            
            # Decrease indent on closing braces
            if stripped.startswith('}') or stripped.startswith(']'):
                indent = max(0, indent - 1)
            
            formatted.append('  ' * indent + stripped)
            
            # Increase indent on opening braces
            if stripped.endswith('{') or stripped.endswith('['):
                indent += 1
        
        print_colored("\nFormatted code:\n", Fore.GREEN)
        print_colored('\n'.join(formatted), Fore.CYAN)
    else:
        try:
            opts = jsbeautifier.default_options()
            opts.indent_size = 2
            formatted = jsbeautifier.beautify(code, opts)
            print_colored("\nFormatted code:\n", Fore.GREEN)
            print_colored(formatted, Fore.CYAN)
        except Exception as e:
            print_colored(f"Error prettifying: {e}", Fore.RED)
    
    input("\nPress Enter to continue...")


def detect_sinks(code: str) -> List[Tuple[int, str, str]]:
    """Detect suspicious JavaScript sinks"""
    findings = []
    lines = code.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        for pattern, description in JS_SINKS:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append((line_num, line.strip(), description))
    
    return findings


def analyze_js_file() -> None:
    """Analyze JavaScript file for sinks and prettify"""
    print_section("JavaScript Analysis")
    file_path = get_file_path("Enter JavaScript file path")
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
    except Exception as e:
        print_colored(f"Error reading file: {e}", Fore.RED)
        input("\nPress Enter to continue...")
        return
    
    # Detect sinks
    findings = detect_sinks(code)
    
    if findings:
        print_colored(f"\nFound {len(findings)} suspicious sinks:\n", Fore.RED)
        for line_num, line, description in findings:
            print_colored(f"Line {line_num}: {description}", Fore.RED)
            print_colored(f"  {line[:80]}", Fore.CYAN)
    else:
        print_colored("\nNo suspicious sinks detected.", Fore.GREEN)
    
    # Prettify option
    prettify = get_input("\nPrettify code? (y/n)", "n")
    if prettify.lower() == 'y':
        prettify_js(code)


def analyze_js_text() -> None:
    """Analyze JavaScript text for sinks"""
    print_section("JavaScript Sink Detection")
    code = get_input("Enter JavaScript code (or 'file:path' to load from file)")
    
    if code.startswith('file:'):
        file_path = code[5:].strip()
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
        except Exception as e:
            print_colored(f"Error reading file: {e}", Fore.RED)
            input("\nPress Enter to continue...")
            return
    
    findings = detect_sinks(code)
    
    if findings:
        print_colored(f"\nFound {len(findings)} suspicious sinks:\n", Fore.RED)
        for line_num, line, description in findings:
            print_colored(f"Line {line_num}: {description}", Fore.RED)
            print_colored(f"  {line[:80]}", Fore.CYAN)
    else:
        print_colored("\nNo suspicious sinks detected.", Fore.GREEN)
    
    input("\nPress Enter to continue...")


def prettify_js_file() -> None:
    """Prettify JavaScript file"""
    file_path = get_file_path("Enter JavaScript file path")
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
    except Exception as e:
        print_colored(f"Error reading file: {e}", Fore.RED)
        input("\nPress Enter to continue...")
        return
    
    prettify_js(code)


def prettify_js_text() -> None:
    """Prettify JavaScript text"""
    code = get_input("Enter JavaScript code (or 'file:path' to load from file)")
    
    if code.startswith('file:'):
        file_path = code[5:].strip()
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
        except Exception as e:
            print_colored(f"Error reading file: {e}", Fore.RED)
            input("\nPress Enter to continue...")
            return
    
    prettify_js(code)


def javascript_menu() -> None:
    """JavaScript tools module menu"""
    options = [
        (1, "Analyze JS File (Sinks + Prettify)", analyze_js_file),
        (2, "Detect Sinks (Text Input)", analyze_js_text),
        (3, "Prettify JS File", prettify_js_file),
        (4, "Prettify JS Text", prettify_js_text),
        (0, "Back to Main Menu", lambda: None),
    ]
    
    menu = Menu("JavaScript Tools Module", options)
    menu.run()

