import os

def install_postgres(pgsql_path):
    """
    Installs PostgreSQL from the specified path.

    Parameters:
    - pgsql_path (str): The path to the PostgreSQL binary directory.

    Returns:
    - message (str): A message indicating the success or failure of the installation.
    """
    try:
        # Check if "pgsql" is in the directory specified by pgsql_path
        if "pgsql" in os.listdir(pgsql_path):
            # Add "pgsql" to pgsql_path
            pgsql_path = os.path.join(pgsql_path, "pgsql")

        # Check if the PostgreSQL binary directory exists
        if not os.path.exists(pgsql_path):
            return f"Error: PostgreSQL binary directory not found at {pgsql_path}"

        # Initialize the database cluster
        os.system(f"{pgsql_path}/bin/initdb -D {pgsql_path}/data")

        # Start the PostgreSQL server
        os.system(f"{pgsql_path}/bin/pg_ctl -D {pgsql_path}/data -l {pgsql_path}/logfile start")

        return "PostgreSQL installed and server started successfully."
    except Exception as e:
        # Return an error message if an exception occurs
        return f"Error: {str(e)}"
