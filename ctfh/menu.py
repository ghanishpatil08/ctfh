"""Interactive menu system for CTF-H"""

from typing import Callable, Dict, List
from ctfh.utils import print_banner, print_colored, Fore, Style, clear_screen


class Menu:
    """Interactive menu handler"""
    
    def __init__(self, title: str, options: List[tuple]):
        """
        Initialize menu
        Args:
            title: Menu title
            options: List of (option_number, option_name, handler_function) tuples
        """
        self.title = title
        self.options = options
        self.handlers: Dict[int, Callable] = {
            opt[0]: opt[2] for opt in options if len(opt) >= 3
        }
        self.option_names: Dict[int, str] = {
            opt[0]: opt[1] for opt in options
        }
    
    def display(self) -> None:
        """Display the menu"""
        clear_screen()
        print_banner()
        print_colored(f"\n{self.title}\n", Fore.YELLOW, Style.BRIGHT)
        print_colored("-" * 60, Fore.CYAN)
        
        for num, name, *_ in self.options:
            print_colored(f"  {num}. {name}", Fore.GREEN)
        
        print_colored("-" * 60, Fore.CYAN)
        print()
    
    def run(self) -> bool:
        """
        Run the menu and handle user selection
        Returns: True if should continue, False if should exit
        """
        while True:
            self.display()
            try:
                print_colored("Select an option: ", Fore.CYAN, end="")
                choice = input().strip()
                
                if not choice:
                    continue
                
                choice_num = int(choice)
                
                if choice_num in self.handlers:
                    result = self.handlers[choice_num]()
                    if result is False:
                        return False  # Exit signal
                    elif result is None:
                        return True  # Go back signal (exit current menu)
                    # Continue to next iteration (menu will redisplay)
                else:
                    print_colored(f"Invalid option: {choice_num}", Fore.RED)
                    input("Press Enter to continue...")
                    
            except ValueError:
                print_colored("Please enter a valid number.", Fore.RED)
                input("Press Enter to continue...")
            except KeyboardInterrupt:
                print_colored("\n\nExiting...", Fore.YELLOW)
                return False
            except Exception as e:
                print_colored(f"Error: {e}", Fore.RED)
                input("Press Enter to continue...")


def create_main_menu(modules: Dict[str, Callable]) -> Menu:
    """Create the main menu"""
    options = [
        (1, "Hashing", lambda: modules.get('hashing', lambda: None)()),
        (2, "Ciphers", lambda: modules.get('ciphers', lambda: None)()),
        (3, "Encoding / Decoding", lambda: modules.get('encoding', lambda: None)()),
        (4, "Steganography", lambda: modules.get('steganography', lambda: None)()),
        (5, "Binary Analysis", lambda: modules.get('binary', lambda: None)()),
        (6, "Vulnerability Scanner", lambda: modules.get('vulnerability', lambda: None)()),
        (7, "JavaScript Tools", lambda: modules.get('javascript', lambda: None)()),
        (8, "HTTP Fuzzing", lambda: modules.get('fuzzing', lambda: None)()),
        (9, "Exit", lambda: False),
    ]
    return Menu("Main Menu", options)

