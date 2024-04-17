import psycopg2

def create_postgres_database(database, user, password, host, port):
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


def drop_postgres_database(database, user, password, host, port):
    """
    Drops a PostgreSQL database if it exists.

    Parameters:
    - database (str): The name of the PostgreSQL database to be dropped.
    - user (str): The username for accessing the PostgreSQL server.
    - password (str): The password for accessing the PostgreSQL server.
    - host (str): The host address of the PostgreSQL server.
    - port (str): The port number of the PostgreSQL server.

    Returns:
    - message (str): A message indicating the success or failure of the database drop operation.
    """
    try:
        # Connect to the default 'postgres' database with autocommit enabled
        connection = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        connection.autocommit = True

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Check if the database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (database,))
        if cursor.fetchone() is not None:
            # Issue the SQL command to drop the target database
            sql_drop_db = f"DROP DATABASE {database};"
            cursor.execute(sql_drop_db)

            return f"Database '{database}' has been dropped successfully."
        else:
            return f"Database '{database}' does not exist. It might have already been dropped."

    except Exception as e:
        return f"Error: {e}"
    finally:
        # Close the connection
        if connection:
            connection.close()
