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
    muscle_path = os.path.join(current_directory, 'hiv_desktop_app/bin/external_apps')

    # Check if the Muscle executable exists at the specified path
    if os.path.exists(muscle_path):
        return muscle_path
    else:
        return None

def check_os():
    os_name = platform.system().lower()  # Get the operating system name and convert to lowercase
    if os_name == "darwin":
        os_name = "mac"  # Change "darwin" to "mac"
    return os_name

def add_to_profile(path_command, profile_path, comment="# Set mafft to the path"):
    # Check if the profile file exists
    if os.path.exists(profile_path):
        with open(profile_path, "r") as f:
            file_content = f.read()
            if path_command not in file_content:
                # Profile exists, append path_command with comment
                with open(profile_path, "a") as f:
                    f.write(f"\n{comment}\n{path_command}\n")
    else:
        # Profile doesn't exist, create and add path_command with comment
        with open(profile_path, "w") as f:
            f.write(f"{comment}\n{path_command}\n")

    
def create_activation_script(filename, activation_script):
    with open(f"activate_{filename}.sh", "w") as f:
        f.write(activation_script)
    
    # Add execute permissions to the activation script
    os.chmod(f"activate_{filename}.sh", 0o755)



def install_and_activate_mafft():
    directory_path = find_path()
    os_name = check_os()

    # Check if "mafft" is in the directory specified by directory_path
    if "mafft" in os.listdir(directory_path):
        # Add "mafft" to directory_path and set to mafft_path variable
        mafft_dir_path = os.path.join(directory_path, "mafft")

        # Change the current working directory to mafft_path
        os.chdir(mafft_dir_path)

    if os_name == "mac":
        mafft_mac_dir_path = os.path.join(mafft_dir_path, 'mafft-mac/')
        path_command = f"export PATH=$PATH:{mafft_mac_dir_path}"


        # Determine the appropriate filename
        profile_filename = ".bashrc" if os.path.exists(os.path.expanduser("~/.bashrc")) else ".bash_profile"
        activation_script = f"#!/bin/bash\nsource ~/{profile_filename}\n"

        # Add path_command to .bash_profile or .bashrc
        add_to_profile(path_command, os.path.expanduser(f"~/{profile_filename}"))


        profile_filename = profile_filename.replace(".", "")  # Remove dot

        # Create the activation script and call it
        create_activation_script(profile_filename, activation_script)

        # Source the activation script to activate .bash_profile
        subprocess.run(["bash", f"activate_{profile_filename}.sh"])
        return mafft_mac_dir_path+'mafft.bat'

# # Call the function to install and activate MAFFT
# install_and_activate_mafft()