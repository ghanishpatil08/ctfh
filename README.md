## 🔥 CTF-H  
### **Interactive CTF, Cryptography & Cybersecurity Toolkit**

CTF-H is a fully interactive, menu‑driven CLI toolkit for:

- CTF competitions  
- Cybersecurity learning & training  
- Cryptography practice  
- Reversing & forensics  
- Web security testing  
- Steganography & encoding challenges  

Launch it with:

- **Windows:**
  ```bash
  python -m ctfh.main
  ```
- **Linux / macOS (or if `ctfh` is on PATH):**
  ```bash
  ctfh
  ```

You’ll see a full‑screen pixel banner and a numbered main menu. Navigate by typing the **number** of a module and pressing **Enter**; each module shows its own submenu and returns to the main menu when you choose the “Back”/`0` option.

---

## 🧰 Features

- **Hashing**: MD5, SHA1, SHA256, SHA512, SHA3 (224/256/384/512), Blake2b  
- **Ciphers**: Caesar (encrypt/decrypt/bruteforce), Vigenère, Atbash, XOR, Rail Fence, frequency analysis  
- **Encoding / Decoding**: Base64/32/58/85, Hex, Binary/ASCII, URL encode/decode, ROT13 / ROT‑N, XOR encode/decode  
- **Steganography** (CTF‑safe): PNG LSB embed/extract, BMP text extraction, EXIF metadata dump  
- **Binary Analysis**: file metadata, strings extraction, objdump preview (if installed), entropy estimation  
- **Vulnerability Scanner**: regex‑based detection for dangerous sinks (`eval`, `innerHTML`, `document.write`, `shell=True`, `pickle.loads`, `os.system`, …)  
- **JavaScript Tools**: JS prettifier, sink detection (eval, `Function`, DOM sinks, jQuery sinks, etc.)  
- **HTTP Fuzzer**: parameter fuzzing with built‑in payload sets, **explicit confirmation** required before sending any requests  

Each module is interactive and guides you through required inputs (text, files, URLs, etc.) and shows results directly in the terminal.

---

## 🚀 Installation

### From PyPI (recommended for users)

Once you’ve published `ctfh` to PyPI, users can install it on **Windows, Linux (including Kali), and macOS** with:

```bash
pip install "ctfh[full]"
```

This installs CTF‑H plus all optional dependencies (Pillow, jsbeautifier, base58). Then run:

- **Windows:**
  ```bash
  python -m ctfh.main
  ```
- **Linux / macOS (or if `ctfh` is on PATH):**
  ```bash
  ctfh
  ```

To install only the core features (no stego/JS extras):

```bash
pip install ctfh
ctfh
```

### From source (development install)

```bash
git clone https://github.com/ghanishpatil08/ctfh
cd ctfh

# Create a virtual environment
python -m venv .venv

# Activate it
# Windows
.venv\Scripts\activate
# Linux / macOS
# source .venv/bin/activate

# Install in editable mode
pip install -e ".[full]"

# Run
python -m ctfh.main
```

### Local system‑wide install from source

```bash
pip install .
```

---

## 📋 Requirements

**Minimum (core):**

- Python 3.10+  
- `colorama`  
- `requests`  

**Full feature set adds:**

- `Pillow` – image handling & EXIF for steganography  
- `jsbeautifier` – JavaScript prettifier  
- `base58` – Base58 encoding/decoding  

All of these are installed automatically when using:

```bash
pip install "ctfh[full]"
```

---

## 🛠 Troubleshooting

### `ctfh` is not recognized as an internal or external command

This usually means the Python *Scripts* directory (where console scripts are installed) is not on your `PATH`.

**Quick workaround (always works):**

```bash
python -m ctfh.main
```

If `python` points to a different version, try:

```bash
py -m ctfh.main
```

**Permanent fix on Windows:**

1. Find the Scripts directory mentioned in `pip` warnings, e.g.
   - `C:\Users\<you>\AppData\Roaming\Python\Python313\Scripts`
2. Open **Start → “Environment Variables” → Edit the system environment variables**  
3. Click **Environment Variables…**
4. Under **User variables**, select **Path → Edit → New**
5. Paste the Scripts path and save
6. Close old terminals, open a new one, and run:

```bash
ctfh
```

### `No module named build` (when running `python -m build`)

Install the packaging tools into your development environment:

```bash
pip install build twine
python -m build
```

### Optional feature errors (Pillow / jsbeautifier / base58 missing)

If a module warns that an optional dependency is missing, either:

- Install the **full** extras:

```bash
pip install "ctfh[full]"
```

- Or install the specific package:

```bash
pip install Pillow jsbeautifier base58
```

### HTTP fuzzing / scanner connectivity issues

- Verify you have an active network connection and the target URL is correct
- The fuzzer **will not** run unless you explicitly type `CONFIRM` when prompted
- Only use these features against systems you own or have written permission to test

For any other error, run with `python -m ctfh.main` and capture the full traceback when reporting issues.

---

## ⚠️ Disclaimer

CTF‑H is for **educational use and authorized security testing only**.  

- Do **not** run the HTTP fuzzer or vulnerability scanner against systems you do not own or explicitly control.  
- Always obtain written permission before testing third‑party infrastructure.  
- You are responsible for complying with all applicable laws and rules where you operate.

---

## 📝 License (MIT)

Copyright (c) 2025 **CSBC**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
