"""HTTP fuzzing module for CTF-H"""

import requests
import time
from typing import List, Optional
from ctfh.utils import print_section, print_colored, Fore, get_input
from ctfh.menu import Menu


# Common fuzzing payloads (CTF-safe)
FUZZ_PAYLOADS = [
    # SQL Injection
    "' OR '1'='1",
    "' OR 1=1--",
    "admin'--",
    "' UNION SELECT NULL--",
    
    # XSS
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(1)",
    
    # Command Injection
    "; ls",
    "| whoami",
    "&& id",
    
    # Path Traversal
    "../../../etc/passwd",
    "..\\..\\..\\windows\\system32\\config\\sam",
    
    # Template Injection
    "{{7*7}}",
    "${7*7}",
    "#{7*7}",
    
    # Special characters
    "'",
    '"',
    "<",
    ">",
    "&",
    "=",
    "?",
    "#",
]


def confirm_fuzzing() -> bool:
    """Require explicit confirmation for fuzzing"""
    print_colored("\n" + "="*60, Fore.RED)
    print_colored("WARNING: HTTP Fuzzing", Fore.RED)
    print_colored("="*60, Fore.RED)
    print_colored("This tool is for authorized testing only.", Fore.YELLOW)
    print_colored("Only use on systems you own or have explicit permission to test.", Fore.YELLOW)
    print_colored("="*60, Fore.RED)
    
    confirm = get_input("\nType 'CONFIRM' to proceed", "")
    return confirm.upper() == 'CONFIRM'


def fuzz_url(url: str, parameter: str, method: str = "GET", custom_payloads: Optional[List[str]] = None) -> None:
    """Fuzz a URL parameter"""
    print_section("HTTP Fuzzing")
    
    if not confirm_fuzzing():
        print_colored("Fuzzing cancelled.", Fore.YELLOW)
        input("\nPress Enter to continue...")
        return
    
    payloads = custom_payloads if custom_payloads else FUZZ_PAYLOADS
    
    print_colored(f"\nTarget URL: {url}", Fore.YELLOW)
    print_colored(f"Parameter: {parameter}", Fore.YELLOW)
    print_colored(f"Method: {method}", Fore.YELLOW)
    print_colored(f"Payloads: {len(payloads)}\n", Fore.YELLOW)
    
    delay = float(get_input("Delay between requests (seconds)", "0.5"))
    
    results = []
    
    for i, payload in enumerate(payloads, 1):
        try:
            if method.upper() == "GET":
                params = {parameter: payload}
                response = requests.get(url, params=params, timeout=5, allow_redirects=False)
            else:  # POST
                data = {parameter: payload}
                response = requests.post(url, data=data, timeout=5, allow_redirects=False)
            
            status = response.status_code
            length = len(response.content)
            
            # Highlight interesting responses
            if status >= 400 and status < 500:
                color = Fore.YELLOW
            elif status >= 500:
                color = Fore.RED
            elif length > 0:
                color = Fore.GREEN
            else:
                color = Fore.CYAN
            
            result_str = f"[{i:3d}/{len(payloads)}] Status: {status:3d} | Length: {length:6d} | Payload: {payload[:40]}"
            print_colored(result_str, color)
            
            results.append({
                'payload': payload,
                'status': status,
                'length': length,
                'response': response.text[:200] if response.text else ''
            })
            
            time.sleep(delay)
            
        except requests.exceptions.RequestException as e:
            print_colored(f"[{i:3d}/{len(payloads)}] Error: {e}", Fore.RED)
        except KeyboardInterrupt:
            print_colored("\n\nFuzzing interrupted by user.", Fore.YELLOW)
            break
    
    # Summary
    print_colored(f"\n{'='*60}", Fore.CYAN)
    print_colored("Fuzzing Summary:", Fore.GREEN)
    print_colored(f"  Total requests: {len(results)}", Fore.CYAN)
    
    status_counts = {}
    for r in results:
        status = r['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print_colored("\nStatus code distribution:", Fore.YELLOW)
    for status, count in sorted(status_counts.items()):
        print_colored(f"  {status}: {count}", Fore.CYAN)
    
    # Show interesting results
    interesting = [r for r in results if r['status'] >= 400 or r['length'] > 10000]
    if interesting:
        print_colored(f"\nInteresting responses ({len(interesting)}):", Fore.YELLOW)
        for r in interesting[:5]:  # Show first 5
            print_colored(f"  Status {r['status']}, Length {r['length']}: {r['payload']}", Fore.CYAN)
    
    input("\nPress Enter to continue...")


def fuzz_custom() -> None:
    """Custom fuzzing with user-defined parameters"""
    print_section("HTTP Fuzzing - Custom")
    
    if not confirm_fuzzing():
        print_colored("Fuzzing cancelled.", Fore.YELLOW)
        input("\nPress Enter to continue...")
        return
    
    url = get_input("Enter target URL")
    parameter = get_input("Enter parameter name to fuzz")
    method = get_input("HTTP method (GET/POST)", "GET")
    
    if not url or not parameter:
        print_colored("URL and parameter are required.", Fore.RED)
        input("\nPress Enter to continue...")
        return
    
    # Custom payloads
    custom = get_input("Enter custom payloads (comma-separated, or 'default' for built-in)", "default")
    if custom.lower() == 'default':
        payloads = None
    else:
        payloads = [p.strip() for p in custom.split(',')]
    
    fuzz_url(url, parameter, method, payloads)


def fuzz_quick() -> None:
    """Quick fuzzing with default settings"""
    print_section("HTTP Fuzzing - Quick")
    
    if not confirm_fuzzing():
        print_colored("Fuzzing cancelled.", Fore.YELLOW)
        input("\nPress Enter to continue...")
        return
    
    url = get_input("Enter target URL")
    parameter = get_input("Enter parameter name to fuzz")
    
    if not url or not parameter:
        print_colored("URL and parameter are required.", Fore.RED)
        input("\nPress Enter to continue...")
        return
    
    fuzz_url(url, parameter)


def fuzzing_menu() -> None:
    """HTTP fuzzing module menu"""
    options = [
        (1, "Quick Fuzz (Default Payloads)", fuzz_quick),
        (2, "Custom Fuzz (Custom Payloads)", fuzz_custom),
        (0, "Back to Main Menu", lambda: None),
    ]
    
    menu = Menu("HTTP Fuzzing Module", options)
    result = menu.run()
    # Return None to signal "go back to main menu" when submenu exits
    return None if result else False

