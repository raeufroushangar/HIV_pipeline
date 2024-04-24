from db_server_starter import start_or_connect_postgres

import psycopg2
import pandas as pd

def create_db(database, user, password, host, port):
    """
    Creates a new PostgreSQL database and grants admin privileges to the specified user.

    Parameters:
    - database (str): The name of the new PostgreSQL database to create.
    - user (str): The username for accessing the database.
    - password (str): The password for accessing the database.
    - host (str): The host address of the database server.
    - port (str): The port number of the database server.

    Returns:
    - message (str): A message indicating the success or failure of the database creation and privilege granting.
    """
    try:
        # Connect to the default PostgreSQL database
        connection = psycopg2.connect(
            database="postgres",
            user=user,
            password=password,
            host=host,
            port=port
        )
        connection.autocommit = True

        # Create a cursor to interact with the database
        with connection.cursor() as cursor:
            # Check if the database already exists
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (database,))
            if cursor.fetchone() is not None:
                return f"Database '{database}' already exists."
            
            # Create the new database
            cursor.execute(f"CREATE DATABASE {database};")

            # Grant privileges to the user on the new database
            cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {database} TO {user};")
            cursor.execute(f"ALTER USER {user} WITH SUPERUSER;")

            return f"Database '{database}' created successfully. Admin privileges granted to user '{user}'."
    except Exception as e:
        # Return an error message if an exception occurs
        return f"Error: {str(e)}"
    finally:
        # Close the connection
        if connection:
            connection.close()
            

def create_table(database, user, password, host, port, column_dict, table_name):
    """
    Creates a new table in a PostgreSQL database with the specified columns.

    Parameters:
    - database (str): The name of the PostgreSQL database.
    - user (str): The username for accessing the database.
    - password (str): The password for accessing the database.
    - host (str): The host address of the database server.
    - port (str): The port number of the database server.
    - table_name (str): The name of the table to be created.
    - column_dict (dict): A dictionary where keys are column names and values are their data types.

    Returns:
    - str: A success message if the table is created, a skip message if the table already exists, or an error message if an exception occurs.
    """
    try:
        # Connect to the PostgreSQL database
        with psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        ) as connection:
            # Create a cursor
            with connection.cursor() as cursor:
                # Generate the column definitions string
                column_defs = [f"{column_name} {data_type}" for column_name, data_type in column_dict.items()]
                column_defs_str = ", ".join(column_defs)

                # Check if the table exists
                check_table_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');"
                cursor.execute(check_table_query)
                table_exists = cursor.fetchone()[0]

                if table_exists:
                    return f"Table '{table_name}' already exists. Skipping table creation."
                else:
                    # Define the SQL command to create the table
                    create_table_query = f"CREATE TABLE {table_name} ({column_defs_str});"

                    # Execute the SQL command
                    cursor.execute(create_table_query)

                    # Commit the changes to the database
                    connection.commit()

                    return f"Table '{table_name}' created successfully!"

    except psycopg2.Error as error:
        return f"Error while creating table: {error}"
    
    
def db_wrapper(pgsql_path, database, user, password, host, port, read_db_tables_from_json, db_tables_json_path):
    """
    Wrapper function to install, start or connect to PostgreSQL, and create a new database if it doesn't already exist.
    """
    try:
        # Find the path to the PostgreSQL binary directory
        if pgsql_path is None:
            return "Error: PostgreSQL binary directory not found."

        # Start or connect to PostgreSQL server
        start_result = start_or_connect_postgres(pgsql_path)
        print(start_result)
        if start_result.startswith("Error"):
            return start_result

        # Check if the database already exists
        connection = psycopg2.connect(
            database="postgres",
            user=user,
            password=password,
            host=host,
            port=port
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (database,))
        if cursor.fetchone() is not None:
            return f"PostgreSQL server started. Database '{database}' already exists."

        # Create PostgreSQL database
        create_result = create_db(database, user, password, host, port)
        if create_result.startswith("Error"):
            return create_result

        db_tables_info = read_db_tables_from_json(db_tables_json_path)
        for table_name, table_data in db_tables_info["tables"].items():
            column_dict = table_data["column_dict"]
            create_table(database, user, password, host, port, column_dict, table_name)

        return f"PostgreSQL installed, server started, and database '{database}' created successfully."
    except Exception as e:
        return f"Error: {str(e)}"

    
def extract_table(database, user, password, host, port, table_name):
    """
    Extracts a specified table from a PostgreSQL database and returns the result as a Pandas DataFrame.

    Parameters:
    - database (str): The name of the PostgreSQL database.
    - user (str): The username for accessing the database.
    - password (str): The password for accessing the database.
    - host (str): The host address of the database server.
    - port (str): The port number of the database server.
    - table_name (str): The name of the table to extract.

    Returns:
    - df (DataFrame or str): The extracted table as a Pandas DataFrame, or an error message as a string.
    """
    try:
        # Connect to the PostgreSQL database
        with psycopg2.connect(
                database=database,
                user=user,
                password=password,
                host=host,
                port=port
        ) as connection:
            # Create a cursor to interact with the database
            with connection.cursor() as cursor:
                # Check if the table exists in the PostgreSQL database
                cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);", (table_name,))
                exists = cursor.fetchone()[0]

                if exists:
                    # Fetch all the records from the specified table
                    cursor.execute(f"SELECT * FROM {table_name};")
                    records = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]
                    df = pd.DataFrame(records, columns=column_names)
                    return df
                else:
                    # Return an error message if the table does not exist
                    return f"The table '{table_name}' does not exist in the database."
    except psycopg2.Error as e:
        # Return an error message if an exception occurs
        return f"An error occurred: {str(e)}"