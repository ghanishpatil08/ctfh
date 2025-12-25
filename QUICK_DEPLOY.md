# Quick Deployment Reference - Copy & Paste Commands

## 🚀 Complete Command Sequence (Copy & Paste)

### 1. Navigate to Project
```cmd
cd F:\ctfh
```

### 2. Clean Old Builds
```cmd
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for /d %d in (*.egg-info) do rmdir /s /q "%d"
```

### 3. Install Build Tools
```cmd
python -m pip install --upgrade build twine
```

### 4. Build Package
```cmd
python -m build
```

### 5. Check Build
```cmd
python -m twine check dist/*
```

### 6. Upload to TestPyPI (Test First)
```cmd
python -m twine upload --repository testpypi dist/*
```
**When prompted:**
- Username: `__token__`
- Password: [Your TestPyPI API token]

### 7. Test Installation from TestPyPI
```cmd
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ctfh
python -m ctfh.main
```

### 8. Upload to Production PyPI
```cmd
python -m twine upload dist/*
```
**When prompted:**
- Username: `__token__`
- Password: [Your PyPI API token]

### 9. Verify Installation
```cmd
pip install --upgrade ctfh
python -c "import ctfh; print('Version:', ctfh.__version__)"
python -m ctfh.main
```

---

## 📋 What Each Step Does

| Step | Command | Purpose |
|------|---------|---------|
| 1 | `cd F:\ctfh` | Navigate to project |
| 2 | Clean commands | Remove old build files |
| 3 | `pip install build twine` | Install build tools |
| 4 | `python -m build` | Create distribution files |
| 5 | `twine check` | Validate build |
| 6 | `twine upload --repository testpypi` | Upload to test environment |
| 7 | `pip install` | Test installation works |
| 8 | `twine upload` | Upload to production |
| 9 | Verify | Confirm everything works |

---

## 🔑 Credentials Needed

### TestPyPI Token
- Get from: https://test.pypi.org/manage/account/token/
- Starts with: `pypi-`
- Username: `__token__`

### PyPI Token
- Get from: https://pypi.org/manage/account/token/
- Starts with: `pypi-`
- Username: `__token__`

---

## ⚠️ Common Mistakes to Avoid

1. ❌ Using account password instead of API token
2. ❌ Using wrong token (TestPyPI vs PyPI)
3. ❌ Wrong username (must be `__token__` exactly)
4. ❌ Forgetting to increment version if already exists
5. ❌ Uploading without testing on TestPyPI first

---

## ✅ Success Indicators

- ✅ Build completes: "Successfully built..."
- ✅ Check passes: "PASSED"
- ✅ Upload completes: "100%" progress
- ✅ Package visible on PyPI website
- ✅ Installation works: `pip install ctfh` succeeds
- ✅ Tool runs: `python -m ctfh.main` works

---

**For detailed explanations, see [DEPLOYMENT_STEPS.md](DEPLOYMENT_STEPS.md)**

