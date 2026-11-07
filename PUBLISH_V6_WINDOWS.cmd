@echo off
setlocal
cd /d "%~dp0"
if not exist ".git" (
  echo ERROR: Run this script INSIDE your original depths-3d Git repository.
  echo The downloaded ZIP does not contain .git. Extract its contents into your existing repo first.
  pause
  exit /b 1
)
where git >nul 2>&1
if errorlevel 1 (
  echo ERROR: git was not found. Install Git for Windows and try again.
  pause
  exit /b 1
)
git tag -l v6.0.0 | findstr /x v6.0.0 >nul
if not errorlevel 1 (
  echo ERROR: Tag v6.0.0 already exists. Inspect it before proceeding.
  pause
  exit /b 1
)
node --check src\game.js
if errorlevel 1 (
  echo ERROR: JavaScript syntax verification failed. No commit created.
  pause
  exit /b 1
)
echo This will commit and push to origin main and create tag v6.0.0.
choice /m "Continue"
if errorlevel 2 exit /b 0
git add -A
git commit -m "Release Depths 3D v6.0.0 - The Bestiary Expansion"
if errorlevel 1 (
  echo ERROR: Git commit failed or no changes. Check git status.
  pause
  exit /b 1
)
git push origin main
if errorlevel 1 (
  echo ERROR: Push failed. Check origin/branch/permissions before tagging.
  pause
  exit /b 1
)
git tag -a v6.0.0 -m "Depths 3D v6.0.0 - The Bestiary Expansion"
git push origin v6.0.0
if errorlevel 1 (
  echo ERROR: Tag push failed. Check GitHub permissions.
  pause
  exit /b 1
)
echo Code and tag pushed. Publish a GitHub Release from tag v6.0.0.
pause
