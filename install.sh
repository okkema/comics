#!/bin/sh

# unrar is the recommended backend for rarfile Python package
# https://rarfile.readthedocs.io/
echo "Installing dependencies"
apt-get update && apt-get install -y unrar-free

# Create virtual environment and install packages
echo "Creating virtual environment"
python3.11 -m venv .venv
echo "Installing packages"
.venv/bin/pip install -r requirements.txt 
