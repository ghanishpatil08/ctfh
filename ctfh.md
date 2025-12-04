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

ctfh

csharp
Copy code

CTFH opens a **full-screen ASCII menu** with nested options such as:

==========================================
██████╗████████╗███████╗██╗ ██╗
██╔════╝╚══██╔══╝██╔════╝██║ ██╔╝
██║ ███╗ ██║ ███████╗█████╔╝
██║ ██║ ██║ ╚════██║██╔═██╗
╚██████╔╝ ██║ ███████║██║ ██╗
╚═════╝ ╚═╝ ╚══════╝╚═╝ ╚═╝
Welcome to CTF-H
Hashing

Ciphers

Encoding / Decoding

Steganography

Binary Analysis

Vulnerability Scanner

JavaScript Tools

HTTP Fuzzing

Exit

markdown
Copy code

Users navigate by selecting numbers, and each section expands into its own submenu.

---

# 🧰 Features (Menu-Based)

### **1. Hashing Module**
Interactive hashing options:
- MD5  
- SHA1  
- SHA256  
- SHA512  
- SHA3 variants  
- Blake2  

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
- `eval(`
- `innerHTML`
- `document.write`
- `shell=True`
- `pickle.loads`
- `os.system`

### **7. JS Tools**
- JS prettifying  
- Suspicious sink detection  

### **8. HTTP Fuzzer**
Safe fuzzing with:
- Required `--confirm` flag  
- Controlled payload sets  

---

# 🚀 Installation

### Development Install

```bash
git clone https://github.com/your/ctfh.git
cd ctfh
python3 -m venv .venv
. .venvenv/bin/activate
pip install -e .
System-Wide Install
bash
Copy code
sudo pip install .
Starts with:

bash
Copy code
ctfh
