import os

def find_apps_in_external_apps_dir(target_dir):
    """
    Find the path to the specified target directory within the 'hiv_desktop_app' directory.

    Parameters:
    - target_dir (str): The name of the target directory ('external_apps' or 'database').

    Returns:
    - app_path (str): The path to the target directory if found, otherwise None.
    """
    try:
        # Find the current working directory of the script
        current_directory = os.getcwd()

        # Search for the 'hiv_desktop_app' directory starting from the current directory
        while 'hiv_desktop_app' not in os.listdir(current_directory):
            current_directory = os.path.dirname(current_directory)

        # Once the 'hiv_desktop_app' directory is found, construct the path to the target directory
        app_path = os.path.join(current_directory, f'hiv_desktop_app/bin/{target_dir}')

        # Check if the target directory exists at the specified path
        if os.path.exists(app_path):
            return app_path
        else:
            return None
    except Exception as e:
        return f"Error: {str(e)}"
