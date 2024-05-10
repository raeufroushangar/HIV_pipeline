#!/bin/bash

# Step 1: Set the https_proxy environment variable
export https_proxy=http://proxyout.lanl.gov:8080

# Step 2: Create a Virtual Environment
python3 -m venv env

# Step 3: Activate the Virtual Environment
source env/bin/activate

# Step 4: Install Dependencies
pip3 install -r requirements.txt

# Step 5: Configure Jupyter Notebook
./configure_jupyter.sh

# Step 6: Source the configuration script to apply changes to the current shell
if [ -f "$HOME/.bash_profile" ]; then
    source "$HOME/.bash_profile"
elif [ -f "$HOME/.bashrc" ]; then
    source "$HOME/.bashrc"
else
    echo "No shell configuration file found."
fi

# Step 7: Open the Jupyter Notebook
jupyter-notebook seq.ipynb
