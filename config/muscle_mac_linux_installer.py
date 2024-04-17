import os
import platform
import subprocess

def find_path():
    # Find the current working directory of the script
    current_directory = os.getcwd()

    # Search for the 'hiv_desktop_app' directory starting from the current directory
    while 'hiv_desktop_app' not in os.listdir(current_directory):
        current_directory = os.path.dirname(current_directory)

    # Once the 'hiv_desktop_app' directory is found, construct the path to Muscle 
    muscle_path = os.path.join(current_directory, 'hiv_desktop_app/external_apps')

    # Check if the Muscle executable exists at the specified path
    if os.path.exists(muscle_path):
        return muscle_path
    else:
        return None

def get_os_name_and_arch():
    os_name = platform.system().lower()
    arch, _ = platform.architecture()
    arch_string = ''.join(filter(str.isdigit, arch))
    return os_name, arch_string

def add_to_bash_profile_or_bashrc(path_command):
    # Check if .bash_profile or .bashrc exists
    home_directory = os.path.expanduser("~")
    bash_profile_path = os.path.join(home_directory, ".bash_profile")
    bashrc_path = os.path.join(home_directory, ".bashrc")

    # Check if the path_command is already in the file
    if os.path.exists(bash_profile_path):
        with open(bash_profile_path, "r") as f:
            if path_command not in f.read():
                # .bash_profile exists, append path_command
                with open(bash_profile_path, "a") as f:
                    f.write(f"\n{path_command}\n")
    elif os.path.exists(bashrc_path):
        with open(bashrc_path, "r") as f:
            if path_command not in f.read():
                # .bashrc exists, append path_command
                with open(bashrc_path, "a") as f:
                    f.write(f"\n{path_command}\n")
    else:
        # Neither .bash_profile nor .bashrc exists, create .bash_profile and add path_command
        with open(bash_profile_path, "w") as f:
            f.write(f"{path_command}\n")


def create_activation_script(filename):
    activation_script = f"""#!/bin/bash
source ~/{filename}
"""
    with open(f"activate_{filename}.sh", "w") as f:
        f.write(activation_script)
    
    # Add execute permissions to the activation script
    os.chmod(f"activate_{filename}.sh", 0o755)


def get_entry_path(entry, item_path):
    # Set the name of the uncompressed version
    entry_uncompressed = entry.replace('.tar.gz', '')
    entry_path = os.path.join(item_path, entry_uncompressed)
    
    if os.path.exists(entry_path):
        return entry_path
    else:
        return None

def install_and_activate_muscle():
    directory_path = find_path()
    os_name, arch = get_os_name_and_arch()
    
    if "muscle" in os.listdir(directory_path):
        item_path = os.path.join(directory_path, "muscle")
        os.chdir(item_path)
        for entry in os.listdir():
            if os_name in entry and arch in entry:
                # Check if the uncompressed version already exists
                entry_path = get_entry_path(entry, item_path)
                if entry_path is None:
                    if os_name in ["darwin", "linux"]:
                        # Uncompress using 'tar xvf' on macOS or Linux, redirect stdout and stderr to DEVNULL
                        subprocess.run(["tar", "xvf", entry], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        
                        # Set the name of the uncompressed version and update entry_path
                        entry_uncompressed = entry.replace('.tar.gz', '')
                        entry_path = os.path.join(item_path, entry_uncompressed)
                        path_command = f"export PATH=$PATH:{entry_path}"

                        # Grant execute permissions to the binary
                        os.chmod(entry_path, 0o755)

                        # Add path_command to .bash_profile or .bashrc
                        add_to_bash_profile_or_bashrc(path_command)

                        # Determine the appropriate filename
                        filename = "bashrc" if os.path.exists(os.path.expanduser("~/.bashrc")) else "bash_profile"

                        # Create the activation script and call it
                        create_activation_script(filename)

                        # Call the activation script to activate .bash_profile
                        activation_script = f"./activate_{filename}.sh"
                        subprocess.run([activation_script])
                        
                        return entry_path
                else:
                    return entry_path
