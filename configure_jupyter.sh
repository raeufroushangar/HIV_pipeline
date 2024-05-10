#!/bin/bash

# Function to search for the directory containing jupyter-notebook
find_jupyter_notebook_dir() {
    local directories=("/usr/local/bin" "/usr/bin" "/usr/sbin" "/bin")
    for dir in "${directories[@]}"; do
        if [ -x "$dir/jupyter-notebook" ]; then
            echo "$dir"
            return
        fi
    done
}

# Function to find the first shell configuration file (.bash_profile or .bashrc)
find_shell_config_file() {
    local files=("$HOME/.bash_profile" "$HOME/.bashrc")
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            echo "$file"
            return
        fi
    done
}

# Find the directory containing the jupyter-notebook executable
JUPYTER_NOTEBOOK_DIR=$(find_jupyter_notebook_dir)

# Find the shell configuration file
SHELL_CONFIG_FILE=$(find_shell_config_file)

# Check if Jupyter Notebook directory is found
if [ -n "$JUPYTER_NOTEBOOK_DIR" ]; then
    echo "Found Jupyter Notebook at: $JUPYTER_NOTEBOOK_DIR"

    # Add Jupyter Notebook directory to PATH in the first shell configuration file found
    if [ -n "$SHELL_CONFIG_FILE" ]; then
        if ! grep -q "$JUPYTER_NOTEBOOK_DIR" "$SHELL_CONFIG_FILE"; then
            echo "export PATH=\"$JUPYTER_NOTEBOOK_DIR:\$PATH\"" >> "$SHELL_CONFIG_FILE"
            source "$SHELL_CONFIG_FILE"
            echo "Jupyter Notebook directory added to PATH in $SHELL_CONFIG_FILE."
        else
            echo "Jupyter Notebook directory already exists in PATH in $SHELL_CONFIG_FILE."
        fi
    else
        # Create .bash_profile if it doesn't exist
        SHELL_CONFIG_FILE="$HOME/.bash_profile"
        touch "$SHELL_CONFIG_FILE"
        echo "export PATH=\"$JUPYTER_NOTEBOOK_DIR:\$PATH\"" >> "$SHELL_CONFIG_FILE"
        source "$SHELL_CONFIG_FILE"
        echo "Jupyter Notebook directory added to PATH in $SHELL_CONFIG_FILE."
    fi
else
    echo "Jupyter Notebook not found. Please make sure it's installed and in your PATH."
fi
