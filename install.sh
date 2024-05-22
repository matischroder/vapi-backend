#!/bin/bash

# Check if any arguments are passed
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 package1 [package2 ...]"
    exit 1
fi

# Ensure pip-tools is installed
pip install pip-tools

# Install each package passed as an argument
for pkg in "$@"
do
    echo "Installing $pkg..."
    pip install "$pkg"
    # Add the package to requirements.in if not already present
    if ! grep -q "^$pkg" requirements.in; then
        echo "$pkg" >> requirements.in
    fi
done

# Generate requirements.txt from requirements.in
echo "Compiling requirements.txt from requirements.in..."
pip-compile requirements.in
echo "Done."
