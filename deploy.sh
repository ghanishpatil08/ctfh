#!/bin/bash
# CTF-H Deployment Script for Linux/macOS

echo "========================================"
echo "CTF-H Deployment Script"
echo "========================================"
echo

# Step 1: Clean old builds
echo "[1/5] Cleaning old build files..."
rm -rf build/ dist/ *.egg-info
echo "Done!"
echo

# Step 2: Install/upgrade build tools
echo "[2/5] Installing build tools..."
python3 -m pip install --upgrade build twine
echo "Done!"
echo

# Step 3: Build package
echo "[3/5] Building package..."
python3 -m build
if [ $? -ne 0 ]; then
    echo "ERROR: Build failed!"
    exit 1
fi
echo "Done!"
echo

# Step 4: Check build
echo "[4/5] Checking build..."
python3 -m twine check dist/*
if [ $? -ne 0 ]; then
    echo "ERROR: Build check failed!"
    exit 1
fi
echo "Done!"
echo

# Step 5: Upload options
echo "[5/5] Ready to upload!"
echo
echo "Choose upload option:"
echo "1. Upload to TestPyPI (recommended first)"
echo "2. Upload to PyPI (production)"
echo "3. Skip upload (build only)"
echo
read -p "Enter choice (1/2/3): " choice

if [ "$choice" == "1" ]; then
    echo
    echo "Uploading to TestPyPI..."
    python3 -m twine upload --repository testpypi dist/*
elif [ "$choice" == "2" ]; then
    echo
    echo "Uploading to PyPI..."
    python3 -m twine upload dist/*
else
    echo
    echo "Skipping upload. Files are in dist/ folder."
fi

echo
echo "========================================"
echo "Deployment complete!"
echo "========================================"

