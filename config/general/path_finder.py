import os

def find_path_of_file_or_dir(target_dir):
    """
    Find the path to the specified target directory within the 'HIV_pipline_main' directory.

    Parameters:
    - target_dir (str): The name of the target directory ('external_apps' or 'database').

    Returns:
    - app_path (str): The path to the target directory if found, otherwise None.
    """
    try:
        # Find the current working directory of the script
        current_dir = os.getcwd()

        # Once the 'hiv_desktop_app' directory is found, construct the path to the target directory
        app_path = os.path.join(current_dir[:current_dir.rfind('HIV_pipeline_main')], f'HIV_pipeline_main/{target_dir}')

        return app_path
    except Exception as e:
        return f"Error: {str(e)}"
