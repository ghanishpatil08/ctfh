@echo off
REM CTF-H Deployment Script for Windows

echo ========================================
echo CTF-H Deployment Script
echo ========================================
echo.

REM Step 1: Clean old builds
echo [1/5] Cleaning old build files...
if exist build (
    rmdir /s /q build
    echo   - Removed build/
)
if exist dist (
    rmdir /s /q dist
    echo   - Removed dist/
)
for /d %%d in (*.egg-info) do (
    rmdir /s /q "%%d"
    echo   - Removed %%d
)
echo Done! (No old files to clean if this is first build)
echo.

REM Step 2: Install/upgrade build tools
echo [2/5] Installing build tools...
python -m pip install --upgrade build twine
echo Done!
echo.

REM Step 3: Build package
echo [3/5] Building package...
python -m build
if errorlevel 1 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)
echo Done!
echo.

REM Step 4: Check build
echo [4/5] Checking build...
python -m twine check dist/*
if errorlevel 1 (
    echo ERROR: Build check failed!
    pause
    exit /b 1
)
echo Done!
echo.

REM Step 5: Upload options
echo [5/5] Ready to upload!
echo.
echo Choose upload option:
echo 1. Upload to TestPyPI (recommended first)
echo 2. Upload to PyPI (production)
echo 3. Skip upload (build only)
echo.
set /p choice="Enter choice (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo Uploading to TestPyPI...
    python -m twine upload --repository testpypi dist/*
) else if "%choice%"=="2" (
    echo.
    echo Uploading to PyPI...
    python -m twine upload dist/*
) else (
    echo.
    echo Skipping upload. Files are in dist/ folder.
)

echo.
echo ========================================
echo Deployment complete!
echo ========================================
pause

