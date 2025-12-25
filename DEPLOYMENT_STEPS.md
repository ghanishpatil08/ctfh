# Complete Deployment Guide - CTF-H v1.1.0

## 📋 Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Step-by-Step Deployment](#step-by-step-deployment)
3. [PyPI Account Setup](#pypi-account-setup)
4. [Upload to TestPyPI](#upload-to-testpypi)
5. [Upload to Production PyPI](#upload-to-production-pypi)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## ✅ Pre-Deployment Checklist

Before starting, verify:

- [x] Version updated to `1.1.0` in `setup.py` and `ctfh/__init__.py`
- [x] All code changes are saved
- [x] No syntax errors (run `python -m ctfh.main` to test)
- [x] README.md is up to date
- [x] All new features are working

---

## 🚀 Step-by-Step Deployment

### STEP 1: Open Command Prompt

1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. Navigate to your project directory:
   ```cmd
   cd F:\ctfh
   ```

### STEP 2: Activate Virtual Environment (If Using One)

If you're using a virtual environment:
```cmd
.venv\Scripts\activate
```

**OR** if you're not using a virtual environment, you can proceed directly.

### STEP 3: Clean Old Build Files

Remove any previous build artifacts:

```cmd
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for /d %d in (*.egg-info) do rmdir /s /q "%d"
```

**Expected Output:**
- No errors (or "cannot find file" messages are OK if folders don't exist)

### STEP 4: Install/Upgrade Build Tools

Install the required tools for building and uploading:

```cmd
python -m pip install --upgrade build twine
```

**Expected Output:**
```
Successfully installed build-1.3.0 twine-6.2.0 ...
```

**If you see PATH warnings:** That's OK, we'll use `python -m` commands instead.

### STEP 5: Build the Package

Create the distribution files:

```cmd
python -m build
```

**Expected Output:**
```
* Creating isolated environment...
* Building sdist...
* Building wheel...
Successfully built ctfh-1.1.0.tar.gz and ctfh-1.1.0-py3-none-any.whl
```

**What this creates:**
- `dist/ctfh-1.1.0.tar.gz` - Source distribution
- `dist/ctfh-1.1.0-py3-none-any.whl` - Wheel distribution

### STEP 6: Verify the Build

Check that the build is valid:

```cmd
python -m twine check dist/*
```

**Expected Output:**
```
Checking dist\ctfh-1.1.0-py3-none-any.whl: PASSED
Checking dist\ctfh-1.1.0.tar.gz: PASSED
```

**If you see errors:** Fix them before proceeding.

---

## 🔐 PyPI Account Setup

### If You DON'T Have a PyPI Account:

1. **Go to PyPI Registration:**
   - Open browser: https://pypi.org/account/register/
   - Fill in:
     - Username (choose a unique username)
     - Email address
     - Password (strong password)
   - Click "Create account"

2. **Verify Email:**
   - Check your email inbox
   - Click the verification link

3. **Enable Two-Factor Authentication (Recommended):**
   - Go to: https://pypi.org/manage/account/
   - Click "Add 2FA" and follow instructions

### Create API Token:

1. **Go to API Tokens Page:**
   - Visit: https://pypi.org/manage/account/
   - Click on "API tokens" in the left sidebar
   - OR go directly to: https://pypi.org/manage/account/token/

2. **Create New Token:**
   - Click "Add API token"
   - **Token name:** `ctfh-deployment` (or any name you prefer)
   - **Scope:** Choose one:
     - **"Entire account"** - Can upload any project (easier, but less secure)
     - **"Project: ctfh"** - Only for ctfh project (more secure, recommended)
   - Click "Add token"

3. **Copy the Token:**
   - ⚠️ **IMPORTANT:** Copy the token immediately!
   - It will look like: `pypi-AgEIcHlwaS5vcmcCJGY...` (long string)
   - **You won't be able to see it again!**
   - Save it securely (password manager, secure note, etc.)

### For TestPyPI (Separate Account):

TestPyPI is a separate testing environment. You need a separate account:

1. **Register at TestPyPI:**
   - Go to: https://test.pypi.org/account/register/
   - Create account (can use same email as PyPI)
   - Verify email

2. **Create TestPyPI API Token:**
   - Go to: https://test.pypi.org/manage/account/token/
   - Create token (same process as above)
   - Copy the token (starts with `pypi-`)

---

## 🧪 Upload to TestPyPI (Recommended First)

**Why TestPyPI first?**
- Test the upload process without affecting production
- Verify everything works before real deployment
- Safe to experiment

### STEP 1: Upload Command

```cmd
python -m twine upload --repository testpypi dist/*
```

### STEP 2: Enter Credentials

When prompted:

```
Enter your username: __token__
Enter your password: [Paste your TestPyPI API token here]
```

**Important:**
- Username is literally: `__token__` (two underscores, word "token", two underscores)
- Password is your TestPyPI API token (the long string starting with `pypi-`)
- You won't see the password as you type (this is normal)

### STEP 3: Wait for Upload

**Expected Output:**
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading ctfh-1.1.0-py3-none-any.whl
100%|████████████████████| 45.2k/45.2k [00:05<00:00, 8.45kB/s]
Uploading ctfh-1.1.0.tar.gz
100%|████████████████████| 38.1k/38.1k [00:03<00:00, 11.2kB/s]

View at:
https://test.pypi.org/project/ctfh/1.1.0/
```

### STEP 4: Test Installation from TestPyPI

Verify it works:

```cmd
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ctfh
```

**Why `--extra-index-url`?** TestPyPI might not have all dependencies, so this allows pip to get them from regular PyPI.

### STEP 5: Test the Installed Package

```cmd
python -m ctfh.main
```

Or if the command is available:
```cmd
ctfh
```

**Verify:**
- [ ] Tool starts without errors
- [ ] All menus work
- [ ] New features (clipboard, save, progress, etc.) work
- [ ] Version shows 1.1.0

---

## 🎯 Upload to Production PyPI

**Only proceed after successful TestPyPI upload!**

### STEP 1: Upload Command

```cmd
python -m twine upload dist/*
```

**Note:** No `--repository` flag needed (defaults to production PyPI)

### STEP 2: Enter Credentials

When prompted:

```
Enter your username: __token__
Enter your password: [Paste your PyPI API token here]
```

**Important:**
- Use your **production PyPI** token (not TestPyPI token)
- Username is still `__token__`

### STEP 3: Wait for Upload

**Expected Output:**
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading ctfh-1.1.0-py3-none-any.whl
100%|████████████████████| 45.2k/45.2k [00:05<00:00, 8.45kB/s]
Uploading ctfh-1.1.0.tar.gz
100%|████████████████████| 38.1k/38.1k [00:03<00:00, 11.2kB/s]

View at:
https://pypi.org/project/ctfh/1.1.0/
```

### STEP 4: Verify on PyPI Website

1. Visit: https://pypi.org/project/ctfh/
2. Check:
   - [ ] Version 1.1.0 is listed
   - [ ] Description is correct
   - [ ] Files are available for download
   - [ ] Release date is today

---

## ✅ Verification

### Test Installation from PyPI

```cmd
pip uninstall ctfh -y
pip install ctfh
```

### Verify Version

```cmd
python -c "import ctfh; print('Version:', ctfh.__version__)"
```

**Expected Output:**
```
Version: 1.1.0
```

### Test the Tool

```cmd
python -m ctfh.main
```

**Verify all features:**
- [ ] Main menu displays
- [ ] All modules accessible
- [ ] New features work (clipboard, save, progress, etc.)
- [ ] Help system works (type `?` in menus)
- [ ] Quick Actions menu available

### Test with Full Features

```cmd
pip install "ctfh[full]"
```

This installs optional dependencies (Pillow, jsbeautifier, base58).

---

## 🔧 Troubleshooting

### Error: "File already exists"

**Problem:** Version 1.1.0 already exists on PyPI

**Solution:**
1. Increment version in `setup.py` and `ctfh/__init__.py`:
   - Change `1.1.0` to `1.1.1` (patch) or `1.2.0` (minor)
2. Rebuild:
   ```cmd
   python -m build
   ```
3. Upload again

### Error: "Authentication failed"

**Problem:** Wrong credentials

**Solutions:**
1. **Check username:** Must be exactly `__token__` (with underscores)
2. **Check token:** Make sure you copied the entire token
3. **Check token scope:** Token must have permission for the project
4. **Check token type:** Using TestPyPI token on PyPI (or vice versa)
5. **Regenerate token:** Create a new token if needed

### Error: "Invalid version"

**Problem:** Version format is wrong

**Solution:**
- Version must be in format: `X.Y.Z` (e.g., `1.1.0`)
- No letters, no special characters (except dots)
- Check both `setup.py` and `ctfh/__init__.py`

### Error: "Package metadata is invalid"

**Problem:** Issues with setup.py or README

**Solution:**
1. Check `twine check` output for specific errors
2. Verify README.md is valid Markdown
3. Check setup.py syntax

### Error: "Module not found" after installation

**Problem:** Package structure issue

**Solution:**
1. Verify `ctfh/__init__.py` exists
2. Check `setup.py` uses `find_packages()`
3. Rebuild and reinstall

### Error: "Command 'ctfh' not found" (Windows)

**Problem:** PATH issue

**Solution:**
1. Use: `python -m ctfh.main` instead
2. Or add Python Scripts to PATH:
   - Find Scripts folder: `python -c "import site; print(site.USER_BASE + '\\Scripts')"`
   - Add to Windows PATH environment variable

### Build Takes Too Long

**Problem:** Normal for first build

**Solution:**
- First build creates isolated environment (takes 1-2 minutes)
- Subsequent builds are faster
- This is normal behavior

### Upload Fails Midway

**Problem:** Network issue or timeout

**Solution:**
1. Check internet connection
2. Try again (upload is idempotent - safe to retry)
3. If file exists error: version already uploaded (this is OK)

---

## 📝 Post-Deployment Checklist

After successful deployment:

- [ ] Package is visible on PyPI: https://pypi.org/project/ctfh/
- [ ] Installation works: `pip install ctfh`
- [ ] Tool runs: `python -m ctfh.main`
- [ ] All features work correctly
- [ ] Version is correct: `1.1.0`
- [ ] Update GitHub (if using): Create release tag
- [ ] Announce update (if you have users/channels)

---

## 🎉 Success!

Your package is now live on PyPI! Users can install it with:

```cmd
pip install ctfh
```

Or with all features:
```cmd
pip install "ctfh[full]"
```

---

## 📚 Quick Reference Commands

```cmd
# Clean build
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

# Build
python -m build

# Check
python -m twine check dist/*

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ctfh

# Verify version
python -c "import ctfh; print(ctfh.__version__)"
```

---

## 🆘 Need Help?

If you encounter issues:

1. Check the error message carefully
2. Review the troubleshooting section above
3. Check PyPI status: https://status.pypi.org/
4. Verify your API token is valid
5. Try the TestPyPI upload first to isolate issues

---

**Last Updated:** For CTF-H v1.1.0
**Deployment Date:** [Fill in when you deploy]

