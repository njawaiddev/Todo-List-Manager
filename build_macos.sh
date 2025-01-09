#!/bin/bash

# Clean previous builds
rm -rf build dist

# Build the app using PyInstaller
pyinstaller todo_app.spec --clean

# Check if the app was built successfully
if [ ! -d "dist/Todo List Manager.app" ]; then
    echo "Error: App build failed!"
    exit 1
fi

# Create a temporary directory for DMG contents
mkdir -p dist/dmg
cp -r "dist/Todo List Manager.app" dist/dmg/

# Create a temporary icon if it doesn't exist
if [ ! -f "app_icon.icns" ]; then
    echo "Note: No app icon found. Using default icon."
fi

# Create the DMG file
create-dmg \
  --volname "Todo List Manager" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "Todo List Manager.app" 175 120 \
  --hide-extension "Todo List Manager.app" \
  --app-drop-link 425 120 \
  "dist/Todo List Manager.dmg" \
  "dist/dmg/" || echo "Warning: DMG creation had some non-fatal errors"

# Clean up
rm -rf dist/dmg 