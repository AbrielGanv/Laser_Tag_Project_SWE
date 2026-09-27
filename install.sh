#!/bin/bash

set -e

echo "Installing Photon Laser Tag dependencies..."

sudo apt update

sudo apt install -y \
    python3 \
    python3-tk \
    python3-psycopg2 \
    python3-pil \
    python3-pil.imagetk

echo "Installation complete."
echo "Run the program with:"
echo "python3 app.py"