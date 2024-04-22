import os

def find_apps_in_external_apps_dir():
    # Find the current working directory of the script
    current_directory = os.getcwd()

    # Search for the 'hiv_desktop_app' directory starting from the current directory
    while 'hiv_desktop_app' not in os.listdir(current_directory):
        current_directory = os.path.dirname(current_directory)

    # Once the 'hiv_desktop_app' directory is found, construct the path to Muscle 
    app_path = os.path.join(current_directory, 'hiv_desktop_app/bin/external_apps')

    # Check if the Muscle executable exists at the specified path
    if os.path.exists(app_path):
        return app_path
    else:
        return None