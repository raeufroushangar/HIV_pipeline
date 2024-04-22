import psycopg2
import csv
import pandas as pd

def list_tables(database, user, password, host, port):
    """
    Lists all tables in a PostgreSQL database.

    Parameters:
    - database (str): The name of the PostgreSQL database.
    - user (str): The username for accessing the database.
    - password (str): The password for accessing the database.
    - host (str): The host address of the database server.
    - port (str): The port number of the database server.

    Returns:
    - tables (list or str): A list of table names in the database, or an error message as a string.
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
                # Query to get the list of table names
                query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public';
                """
                # Execute the query
                cursor.execute(query)

                # Fetch all the table names
                table_names = cursor.fetchall()

                if not table_names:
                    return "No tables found in the database."
                else:
                    # Return the list of table names
                    return [table[0] for table in table_names]

    except psycopg2.Error as e:
        # Return an error message if an exception occurs
        return f"An error occurred: {str(e)}"


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


def extract_table_to_csv(database, user, password, host, port, table_name, csv_file_path):
    """
    Extracts a specified table from a PostgreSQL database and writes the result to a CSV file.

    Parameters:
    - database (str): The name of the PostgreSQL database.
    - user (str): The username for accessing the database.
    - password (str): The password for accessing the database.
    - host (str): The host address of the database server.
    - port (str): The port number of the database server.
    - table_name (str): The name of the table to extract.
    - csv_file_path (str): The path to the CSV file where the table will be written.

    Returns:
    - str: A success message or an error message.
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
                    
                    # Write the records to a CSV file
                    with open(csv_file_path, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(column_names)
                        writer.writerows(records)
                    
                    return f"The table '{table_name}' has been successfully written to {csv_file_path}."
                else:
                    # Return an error message if the table does not exist
                    return f"The table '{table_name}' does not exist in the database."
    except psycopg2.Error as e:
        # Return an error message if an exception occurs
        return f"An error occurred: {str(e)}"


def get_table_column_data_types(database, user, password, host, port, table_name):
    """
    Retrieves the data types of columns in a specified table within a PostgreSQL database.

    Parameters:
    - database (str): The name of the PostgreSQL database.
    - user (str): The username for accessing the database.
    - password (str): The password for accessing the database.
    - host (str): The host address of the database server.
    - port (str): The port number of the database server.
    - table_name (str): The name of the table whose column data types are to be retrieved.

    Returns:
    - dict: A dictionary where keys are column names and values are their data types.
    - str: An error message if the table does not exist or if an exception occurs.
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
            # Create a cursor object
            with connection.cursor() as cursor:
                # Check if the table exists in the PostgreSQL database
                cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);", (table_name,))
                exists = cursor.fetchone()[0]

                if not exists:
                    return f"The table '{table_name}' does not exist in the database."

                # Execute query to fetch column data types
                query = f"SELECT column_name, data_type, character_maximum_length " \
                        f"FROM information_schema.columns " \
                        f"WHERE table_name = '{table_name}'"
                cursor.execute(query)

                # Fetch all rows
                rows = cursor.fetchall()

                # Create a dictionary to store column names and data types
                column_data_types = {}

                # Process each row
                for row in rows:
                    column_name, data_type, char_length = row
                    if data_type == "character varying" and char_length is not None:
                        data_type = f"{data_type}({char_length})"
                    column_data_types[column_name] = data_type

                return column_data_types

    except psycopg2.Error as e:
        return f"Error retrieving column data types for table '{table_name}': {e}"


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
    

def drop_table(database, user, password, host, port, table_name):
    """
    Drops a specified table from a PostgreSQL database.

    Parameters:
    - database (str): The name of the PostgreSQL database.
    - user (str): The username for accessing the database.
    - password (str): The password for accessing the database.
    - host (str): The host address of the database server.
    - port (str): The port number of the database server.
    - table_name (str): The name of the table to drop.

    Returns:
    - str: A message indicating whether the table was dropped successfully or an error message.
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
                    # Drop the table if it exists
                    cursor.execute(f"DROP TABLE {table_name};")
                    connection.commit()
                    return f"The table '{table_name}' was dropped successfully."
                else:
                    # Return an error message if the table does not exist
                    return f"The table '{table_name}' does not exist in the database."
    except psycopg2.Error as e:
        # Return an error message if an exception occurs
        return f"An error occurred: {str(e)}"

    
def write_table_to_sql(table_column_dict, table_name, file_path):
    """
    Write a CREATE TABLE SQL command to a .sql file.

    Parameters:
    - table_column_dict (dict): A dictionary where keys are column names and values are their data types.
    - table_name (str): The name of the table to be created.
    - file_path (str): The path to the .sql file where the SQL command will be written.
    """
    with open(file_path, 'a') as file:
        file.write(f"\n-- Create table {table_name}\n")
        file.write(f"CREATE TABLE IF NOT EXISTS {table_name} (\n")
        for column_name, data_type in table_column_dict.items():
            file.write(f"    {column_name} {data_type},\n")
        file.write(");\n")