# CTF-H Deployment Guide

## Quick Deployment Steps

### Step 1: Update Version (Already Done ✅)
- Version updated to `1.1.0` in `setup.py` and `ctfh/__init__.py`

### Step 2: Clean Previous Builds
```bash
# Remove old build artifacts
rm -rf build/ dist/ *.egg-info
# Windows:
# rmdir /s /q build dist *.egg-info
```

### Step 3: Install Build Tools
```bash
pip install --upgrade build twine
```

### Step 4: Build the Package
```bash
python -m build
```

This creates:
- `dist/ctfh-1.1.0.tar.gz` (source distribution)
- `dist/ctfh-1.1.0-py3-none-any.whl` (wheel distribution)

### Step 5: Check the Build
```bash
twine check dist/*
```

Should show: `Checking dist/ctfh-1.1.0.tar.gz: PASSED`

### Step 6: Test on TestPyPI (Recommended First)
```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ ctfh
```

### Step 7: Deploy to PyPI (Production)
```bash
# Upload to real PyPI
twine upload dist/*
```

You'll be prompted for:
- **Username**: `__token__`
- **Password**: Your PyPI API token (starts with `pypi-`)

## What's New in Version 1.1.0

### ✨ Major Improvements
- ✅ **Clipboard Support**: Copy results to clipboard (Windows/Linux/macOS)
- ✅ **Save to File**: Save all results to text files
- ✅ **Progress Indicators**: Progress bars for long operations
- ✅ **Table Formatting**: Beautiful tables for scan results
- ✅ **Input Validation**: Examples in prompts, better error handling
- ✅ **Batch Processing**: Hash multiple strings at once
- ✅ **Configuration File**: User preferences saved in `~/.ctfh/config.json`
- ✅ **Operation History**: Track last 50 operations
- ✅ **Interactive Help**: Type `?` or `h` for help in any menu
- ✅ **Export Formats**: JSON, CSV, HTML export for scan results
- ✅ **Quick Actions Menu**: Fast access to common operations
- ✅ **Better Navigation**: Improved menu system with help support

### 🐛 Bug Fixes
- Fixed menu navigation (option 0 now properly returns to main menu)
- Improved error handling for file operations
- Better path validation

## Pre-Deployment Checklist

Before deploying, verify:

- [ ] Version number updated in `setup.py` and `ctfh/__init__.py`
- [ ] All tests pass (if you have tests)
- [ ] README.md is up to date
- [ ] No hardcoded paths or local dependencies
- [ ] All imports work correctly
- [ ] Build succeeds without errors
- [ ] `twine check` passes

## Testing After Deployment

```bash
# Install from PyPI
pip install --upgrade ctfh

# Or with full features
pip install --upgrade "ctfh[full]"

# Test the tool
ctfh

# Verify version
python -c "import ctfh; print(ctfh.__version__)"
```

## Rollback (If Needed)

If something goes wrong:

```bash
# Uninstall current version
pip uninstall ctfh

# Install previous version
pip install ctfh==1.0.0
```

## Version Numbering

- **Major** (2.0.0): Breaking changes
- **Minor** (1.1.0): New features, backward compatible
- **Patch** (1.0.1): Bug fixes only

## PyPI Account Setup

If you don't have a PyPI account:

1. Go to https://pypi.org/account/register/
2. Create an account
3. Enable 2FA (recommended)
4. Create an API token:
   - Go to Account Settings → API tokens
   - Create token with scope: "Entire account" or "Project: ctfh"
   - Copy the token (starts with `pypi-`)

## Troubleshooting

### Error: "File already exists"
**Solution**: Delete old files in `dist/` folder or use `--skip-existing` flag:
```bash
twine upload --skip-existing dist/*
```

### Error: "Invalid version"
**Solution**: Check version format in `setup.py` (must be like `1.1.0`)

### Error: "Authentication failed"
**Solution**: 
- Use `__token__` as username
- Use your PyPI API token as password (not your account password)
- Make sure token has correct scope

### Error: "Package already exists"
**Solution**: Version must be incremented. Update to `1.1.1` or `1.2.0`

## Post-Deployment

After successful deployment:

1. ✅ Verify on PyPI: https://pypi.org/project/ctfh/
2. ✅ Test installation: `pip install ctfh`
3. ✅ Update GitHub releases (if using GitHub)
4. ✅ Announce the update (if you have users)

## Next Steps

After deployment, users can install with:
```bash
pip install --upgrade ctfh
```

Or with all features:
```bash
pip install --upgrade "ctfh[full]"
```

