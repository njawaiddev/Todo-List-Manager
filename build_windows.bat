@echo off
echo Cleaning previous builds...
rmdir /s /q build dist

echo Building Windows executable...
pyinstaller todo_app.spec --windowed --onefile --clean

echo Build complete! Check the dist folder for the executable. 