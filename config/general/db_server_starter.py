import os
from db_server_installer import install_postgres

def start_or_connect_postgres(pgsql_path):
    """
    Starts or connects to the PostgreSQL server.

    Parameters:
    - pgsql_path (str): The path to the PostgreSQL binary directory.

    Returns:
    - message (str): A message indicating the success or failure of starting or connecting to the PostgreSQL server.
    """
    try:
        # Check if "pgsql" is in the directory specified by pgsql_path
        if "pgsql" in os.listdir(pgsql_path):
            # Add "pgsql" to pgsql_path
            pgsql_path = os.path.join(pgsql_path, "pgsql")

        # Check if the PostgreSQL binary directory exists
        if not os.path.exists(pgsql_path):
            return f"Error: PostgreSQL binary directory not found at {pgsql_path}"

        # Check if PostgreSQL is already installed
        if not os.path.exists(os.path.join(pgsql_path, "data")):
            # If PostgreSQL is not installed, install it
            install_result = install_postgres(pgsql_path)
            if install_result.startswith("Error"):
                return install_result

        # Start the PostgreSQL server
        os.system(f"{pgsql_path}/bin/pg_ctl -D {pgsql_path}/data -l {pgsql_path}/logfile start > /dev/null 2>&1")

        return "PostgreSQL server started successfully."
    except Exception as e:
        # Return an error message if an exception occurs
        return f"Error: {str(e)}"
