# CTF-H Deployment & Testing Guide

## Quick Start Testing

### 1. Install Dependencies

```bash
# Basic installation (minimum required)
pip install -e .

# Full installation (all features)
pip install -e ".[full]"
```

### 2. Test Installation

```bash
# Verify the command is available
ctfh

# Or run directly
python -m ctfh.main
```

### 3. Manual Testing Checklist

#### Main Menu
- [ ] Menu displays with ASCII banner
- [ ] All 9 options are visible (8 modules + Exit)
- [ ] Navigation works (can select options)

#### Hashing Module
- [ ] Test MD5: Input "test" → Should produce hash
- [ ] Test SHA256: Input "test" → Should produce hash
- [ ] Test SHA3-256: Input "test" → Should produce hash
- [ ] Test Blake2b: Input "test" → Should produce hash
- [ ] Back to main menu works

#### Ciphers Module
- [ ] Caesar Encrypt: Text "hello", shift 13 → Should encrypt
- [ ] Caesar Decrypt: Encrypted text, shift 13 → Should decrypt
- [ ] Caesar Bruteforce: Encrypted text → Shows all 26 shifts
- [ ] Vigenère: Text "hello", key "key" → Should encrypt/decrypt
- [ ] Atbash: Text "hello" → Should transform
- [ ] Frequency Analysis: Text "hello world" → Shows frequencies

#### Encoding/Decoding Module
- [ ] Base64 Encode: "test" → Should encode
- [ ] Base64 Decode: Encoded text → Should decode back
- [ ] Hex Encode: "test" → Should produce hex
- [ ] URL Encode: "test string" → Should encode
- [ ] ROT13: "test" → Should transform
- [ ] Binary Encode: "test" → Should produce binary

#### Steganography Module (requires Pillow)
- [ ] EXIF Metadata: Use any image file → Shows metadata
- [ ] PNG LSB Extract: Use PNG file → Attempts extraction
- [ ] Note: Some features require Pillow (`pip install Pillow`)

#### Binary Analysis Module
- [ ] File Info: Use any file → Shows metadata
- [ ] Extract Strings: Use any binary file → Shows strings
- [ ] Entropy Check: Use any file → Shows entropy

#### Vulnerability Scanner
- [ ] Scan Single File: Use a test file → Shows findings
- [ ] Scan Directory: Use a test directory → Shows findings
- [ ] Scan Text: Input code with `eval(` → Detects vulnerability

#### JavaScript Tools (requires jsbeautifier)
- [ ] Prettify JS: Input JavaScript code → Formats code
- [ ] Detect Sinks: Input JS with `eval(` → Detects sinks
- [ ] Note: Requires jsbeautifier (`pip install jsbeautifier`)

#### HTTP Fuzzing
- [ ] Confirmation prompt appears
- [ ] Type "CONFIRM" → Proceeds with fuzzing
- [ ] Type anything else → Cancels
- [ ] Note: Only test on authorized systems!

### 4. Test Error Handling

- [ ] Run without optional dependencies (should show helpful messages)
- [ ] Test with invalid file paths (should show error)
- [ ] Test with invalid inputs (should handle gracefully)
- [ ] Test Ctrl+C (should exit cleanly)

## Deployment Steps

### For Local/Development Use

```bash
# 1. Install in development mode
pip install -e .

# 2. Verify installation
ctfh --help  # Should show no errors

# 3. Test run
ctfh
```

### For Production/System-Wide Installation

```bash
# 1. Install system-wide
pip install .

# 2. Or with all features
pip install ".[full]"

# 3. Verify
ctfh
```

### For Distribution (PyPI)

```bash
# 1. Build distribution
python -m build

# 2. Check build
twine check dist/*

# 3. Upload to PyPI (if ready)
twine upload dist/*
```

## Verification Commands

```bash
# Check if package is installed
pip show ctfh

# Check if command is available
which ctfh  # Linux/Mac
where ctfh  # Windows

# Test import
python -c "import ctfh; from ctfh.main import main; print('OK')"

# Run the tool
ctfh
```

## Common Issues

### Issue: "ctfh: command not found"
**Solution:** Make sure you installed with `pip install -e .` and your Python scripts directory is in PATH.

### Issue: "ModuleNotFoundError: No module named 'ctfh'"
**Solution:** Install the package: `pip install -e .`

### Issue: Optional features don't work
**Solution:** Install full dependencies: `pip install -e ".[full]"` or individually:
- `pip install Pillow` (for steganography)
- `pip install jsbeautifier` (for JS prettify)
- `pip install base58` (for Base58 encoding)

### Issue: Colors don't work
**Solution:** Install colorama: `pip install colorama`

## Testing Without Optional Dependencies

The tool is designed to work without optional dependencies. Test this:

```bash
# Uninstall optional packages
pip uninstall Pillow jsbeautifier base58

# Run ctfh - should still work, but show messages for missing features
ctfh
```

## Ready for Deployment ✅

Your tool is ready for deployment when:
- ✅ All imports work (`python -c "from ctfh.main import main"` succeeds)
- ✅ Command is available (`ctfh` runs)
- ✅ Main menu displays correctly
- ✅ All modules are accessible
- ✅ Error handling works gracefully
- ✅ Optional dependencies are handled properly

