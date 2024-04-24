import os

def install_postgres(pgsql_path):
    """
    Installs PostgreSQL from the specified path if it is not already installed.

    Parameters:
    - pgsql_path (str): The path to the PostgreSQL binary directory.

    Returns:
    - message (str): A message indicating the success or failure of the installation.
    """
    try:
        # Initialize the database cluster
        os.system(f"{pgsql_path}/bin/initdb -D {pgsql_path}/data")

        # Start the PostgreSQL server
        os.system(f"{pgsql_path}/bin/pg_ctl -D {pgsql_path}/data -l {pgsql_path}/logfile start")

        return "PostgreSQL installed and server started successfully."
    except Exception as e:
        # Return an error message if an exception occurs
        return f"Error: {str(e)}"