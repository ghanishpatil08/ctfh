## CTF-H Setup & Usage Guide

This document explains, step‑by‑step, how to **install**, **run**, and **update** the CTF‑H toolkit on Windows, Linux (including Kali), and macOS.

---

## 1. Prerequisites

- **Python 3.10+** installed and available as `python` or `python3`
- Internet access (for installing from PyPI or cloning the repo)
- Terminal / command prompt access

Recommended extras (for full feature set):

- `Pillow` – steganography (PNG/BMP/EXIF)
- `jsbeautifier` – JavaScript prettifier
- `base58` – Base58 encoding/decoding

These are installed automatically if you use the `ctfh[full]` extra.

---

## 2. Installing from PyPI (recommended for users)

Once the project is published to PyPI, installation is the same on **Windows, Kali, and macOS**.

### 2.1. Basic install (core features)

```bash
pip install ctfh
```

Run the toolkit:

- **Windows:**
  ```bash
  python -m ctfh.main
  ```
- **Linux / macOS (or if `ctfh` is on PATH):**
  ```bash
  ctfh
  ```

### 2.2. Full install (all features)

```bash
pip install "ctfh[full]"
```

This installs:

- Core CTF‑H package
- Pillow (steganography)
- jsbeautifier (JS tools)
- base58 (encoding)

Run:

- **Windows:**
  ```bash
  python -m ctfh.main
  ```
- **Linux / macOS (or if `ctfh` is on PATH):**
  ```bash
  ctfh
  ```

If `pip` on your system is tied to Python 2, use `pip3` instead.

---

## 3. Installing from source (development)

Use this if you’re developing CTF‑H locally or running from a cloned repository.

### 3.1. Clone the repository

```bash
git clone https://github.com/your/ctfh.git
cd ctfh
```

### 3.2. Create and activate a virtual environment

**Windows (PowerShell or cmd):**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3.3. Install in editable mode

Full feature install (recommended for dev):

```bash
pip install -e ".[full]"
```

Core only:

```bash
pip install -e .
```

### 3.4. Run CTF‑H

- **Windows (recommended):**
  ```bash
  python -m ctfh.main
  ```
- **Linux / macOS (or if `ctfh` is on PATH):**
  ```bash
  ctfh
  ```

If the `ctfh` command isn’t found, make sure your virtual environment is activated and your `Scripts`/`bin` directory is on `PATH`. On Windows, using `python -m ctfh.main` avoids PATH issues entirely.

---

## 4. Basic usage

After running `ctfh`, you’ll see:

- A **pixel banner** displaying the CTF‑H wordmark
- A **Main Menu** with numbered options

Example main menu:

- `1. Hashing`
- `2. Ciphers`
- `3. Encoding / Decoding`
- `4. Steganography`
- `5. Binary Analysis`
- `6. Vulnerability Scanner`
- `7. JavaScript Tools`
- `8. HTTP Fuzzing`
- `9. Exit`

### 4.1. Navigating menus

- Type the **number** of the option you want and press **Enter**.
- Each module shows its own submenu and prompts you for text, files, or parameters as needed.
- Selecting `0` or the **Back** option returns you to the **Main Menu**.
- Selecting `9` from the main menu exits the tool.

### 4.2. Example workflows

#### Hashing a string

1. Run `ctfh`  
2. Choose `1` (**Hashing**)  
3. Choose a hash function, e.g. `3` (**SHA256**)  
4. Enter text to hash (e.g. `flag{example}`)  
5. The hex digest is displayed; press Enter to return.

#### Trying a Caesar bruteforce

1. Run `ctfh`  
2. Choose `2` (**Ciphers**)  
3. Choose `3` (**Caesar – Bruteforce**)  
4. Paste ciphertext  
5. All 26 shifts are shown for manual inspection.

#### Using the HTTP fuzzer

1. Run `ctfh`  
2. Choose `8` (**HTTP Fuzzing**)  
3. Select **Quick Fuzz** or **Custom Fuzz**  
4. The tool will **ask you to type `CONFIRM`** before sending any requests  
5. Provide the target URL and parameter name  
6. Results (status codes, response lengths) are shown and summarized.

> The fuzzer and scanners are for **authorized environments only**. Do not target systems you do not own or explicitly control.

---

## 5. Upgrading and uninstalling

### 5.1. Upgrade to the latest version

From any shell:

```bash
pip install -U "ctfh[full]"
```

Or core only:

```bash
pip install -U ctfh
```

### 5.2. Uninstall

```bash
pip uninstall ctfh
```

If you installed extras separately (e.g. Pillow, jsbeautifier), you can remove them too:

```bash
pip uninstall Pillow jsbeautifier base58
```

---

## 6. Building & publishing (for the maintainer)

These steps are for you when you want to release new versions.

1. **Update the version** in:
   - `setup.py` → `version="1.0.x"`  
   - `ctfh/__init__.py` → `__version__ = "1.0.x"`  

2. **Build the package** (in the project root, venv active):

   ```bash
   python -m build
   ```

3. **Upload to TestPyPI** (optional safety step):

   ```bash
   twine upload --repository testpypi dist/*
   ```

4. **Upload to PyPI**:

   ```bash
   twine upload dist/*
   ```

5. Users upgrade with:

   ```bash
   pip install -U "ctfh[full]"
   ```

For more details, see the official packaging docs at `https://packaging.python.org/`.


