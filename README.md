# 🔥 CTF-H  
### **Interactive CTF, Cryptography & Cybersecurity Toolkit**

CTF-H is a fully interactive, menu-driven CLI tool designed for:

- CTF competitions  
- Cybersecurity learning  
- Cryptography practice  
- Reversing & forensics  
- Web security testing  
- Steganography challenges  
- Encoding/decoding tasks  

Launch it with:

```bash
ctfh
```

CTF-H opens a **full-screen ASCII menu** with nested options such as:

```
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

Main Menu
------------------------------------------------------------
  1. Hashing
  2. Ciphers
  3. Encoding / Decoding
  4. Steganography
  5. Binary Analysis
  6. Vulnerability Scanner
  7. JavaScript Tools
  8. HTTP Fuzzing
  9. Exit
------------------------------------------------------------
```

Users navigate by selecting numbers, and each section expands into its own submenu.

---

## 🧰 Features (Menu-Based)

### **1. Hashing Module**
Interactive hashing options:
- MD5  
- SHA1  
- SHA256  
- SHA512  
- SHA3 variants (224, 256, 384, 512)
- Blake2b  

### **2. Cipher Module**
Includes:
- Caesar (encrypt, decrypt, bruteforce)  
- Vigenère  
- Atbash  
- XOR cipher  
- Rail Fence  
- Frequency analysis  

### **3. Encoding / Decoding**
Supports:
- Base64 / Base32 / Base58 / Base85  
- Hex  
- Binary / ASCII  
- URL encode/decode  
- ROT13 / ROT-N  
- XOR encode/decode  

### **4. Steganography Tools (CTF-safe)**
- PNG LSB embed / extract  
- BMP extract  
- EXIF metadata dump  

### **5. Binary Analysis**
- file metadata  
- strings extraction  
- objdump preview (if installed)  
- simple entropy check  

### **6. Vulnerability Scanner**
Pattern detection for:
- `eval()`
- `innerHTML`
- `document.write`
- `shell=True`
- `pickle.loads`
- `os.system`
- And more...

### **7. JS Tools**
- JS prettifying  
- Suspicious sink detection  

### **8. HTTP Fuzzer**
Safe fuzzing with:
- Required confirmation before use
- Controlled payload sets  
- Custom payload support

---

## 🚀 Installation

### Development Install

```bash
git clone https://github.com/your/ctfh.git
cd ctfh
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### System-Wide Install

```bash
pip install .
```

### Full Features Install

For all features including steganography and JavaScript tools:

```bash
pip install -e ".[full]"
# or
pip install -r requirements-full.txt
```

Starts with:

```bash
ctfh
```

---

## 📋 Requirements

**Minimum:**
- Python 3.10+
- colorama
- requests

**Full Features:**
- Pillow (for steganography)
- jsbeautifier (for JavaScript prettifying)
- base58 (for Base58 encoding)

---

## ⚠️ Disclaimer

This tool is for **educational purposes and authorized testing only**. Always ensure you have explicit permission before using the HTTP fuzzing module or vulnerability scanner on any system you do not own.

---

## 📝 License

MIT License

