"""Main entry point for CTF-H"""

from ctfh.menu import create_main_menu
from ctfh.modules import hashing, ciphers, encoding, steganography, binary, vulnerability, javascript, fuzzing


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
    }
    
    menu = create_main_menu(modules)
    menu.run()


if __name__ == '__main__':
    main()

