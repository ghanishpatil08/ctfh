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

## 🚀 Installation (virtual environment required)

For all operating systems, it is **strongly recommended and effectively required** to run CTF‑H inside a dedicated Python virtual environment.

The pattern is always:

```bash
python3 -m venv venv
source venv/bin/activate
```

> On Windows `python3` is usually `python`, and `source venv/bin/activate` is equivalent to `venv\Scripts\activate` in PowerShell/cmd.

Once your environment is active, follow the OS‑specific steps below.

---

### Windows

1. **Create and activate virtual environment (required)**

```bash
python -m venv venv
venv\Scripts\activate
```

2. **Install from PyPI (full feature set)**

```bash
pip install "ctfh[full]"
```

3. **Run**

```bash
python -m ctfh.main
```

4. **From source (development)**

```bash
git clone https://github.com/ghanishpatil08/ctfh
cd ctfh

python -m venv venv
venv\Scripts\activate

pip install -e ".[full]"
python -m ctfh.main
```

---

### Linux / Kali

1. **Create and activate virtual environment (required)**

```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install from PyPI (full feature set)**

```bash
pip install "ctfh[full]"
```

3. **Run**

```bash
ctfh
```

4. **From source (development)**

```bash
git clone https://github.com/ghanishpatil08/ctfh
cd ctfh

python3 -m venv venv
source venv/bin/activate

pip install -e ".[full]"
ctfh
```

---

### Termux (Android)

CTF-H works on **Termux** (Android terminal emulator). Since Termux is Linux-based, it follows the same installation pattern as Linux.

**Prerequisites:**

1. Install Termux from [F-Droid](https://f-droid.org/packages/com.termux/) or [GitHub Releases](https://github.com/termux/termux-app/releases)
2. Update packages and install Python 3.10+ plus system libraries needed for Pillow:

```bash
pkg update && pkg upgrade
pkg install python python-pip git
pkg install libjpeg-turbo libpng libwebp tiff freetype
```

**Installation:**

1. **Create and activate virtual environment (required)**

```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install from PyPI**

**Option A: Full feature set (includes steganography)**

```bash
pip install "ctfh[full]"
```

If Pillow fails to build, install system dependencies first:

```bash
pkg install libjpeg-turbo libpng libwebp tiff freetype
pip install --upgrade pip
pip install "ctfh[full]"
```

**Option B: Core features only (no steganography/JS tools)**

If you encounter Pillow build issues, you can install the core version:

```bash
pip install ctfh
```

This installs CTF-H without optional dependencies (Pillow, jsbeautifier, base58). You'll still have access to:
- Hashing, Ciphers, Encoding/Decoding
- Binary Analysis, Vulnerability Scanner
- HTTP Fuzzing

3. **Run**

```bash
ctfh
```

4. **From source (development)**

```bash
git clone https://github.com/ghanishpatil08/ctfh
cd ctfh

python3 -m venv venv
source venv/bin/activate

pip install -e ".[full]"
ctfh
```

**Note:** Some features may have limitations on Termux:
- Binary analysis tools (like `objdump`) require additional packages: `pkg install binutils`
- Image processing (steganography) requires Pillow and system libraries: `pkg install libjpeg-turbo libpng libwebp tiff freetype`
- Network features (HTTP fuzzing) work normally

---

### macOS

1. **Create and activate virtual environment (required)**

```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install from PyPI (full feature set)**

```bash
pip install "ctfh[full]"
```

3. **Run**

```bash
ctfh
```

4. **From source (development)**

```bash
git clone https://github.com/ghanishpatil08/ctfh
cd ctfh

python3 -m venv venv
source venv/bin/activate

pip install -e ".[full]"
ctfh
```

---

### Local system‑wide install from source (advanced)

If you know what you’re doing and still want to install system‑wide:

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

### Pillow build fails on Termux (Android)

If you see `RequiredDependencyException: The headers or library files could not be found for jpeg` when installing `ctfh[full]`:

1. **Install system libraries first (required for Pillow):**

```bash
pkg install libjpeg-turbo libpng libwebp tiff freetype
```

2. **Upgrade pip and retry:**

```bash
pip install --upgrade pip
pip install "ctfh[full]"
```

3. **Alternative: Install core version only**

If Pillow still fails after installing system libraries, use the core version (no steganography):

```bash
pip install ctfh
```

This gives you all features except steganography and some JS tools. You can always add Pillow later once system libraries are properly installed.

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
