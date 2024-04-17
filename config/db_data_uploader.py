import psycopg2
import pandas as pd

def upload_df_to_table(database, user, password, host, port, table_name, df):
    """
    Uploads rows from a Pandas DataFrame to a PostgreSQL table.

    This function uploads rows from the provided DataFrame to the specified PostgreSQL table.
    It checks if each row already exists in the table based on all column values.
    If a row does not exist, it is uploaded to the table. Rows that already exist are not uploaded.

    Args:
        database (str): Name of the PostgreSQL database.
        user (str): Username for the database.
        password (str): Password for the database.
        host (str): Hostname of the database server.
        port (int): Port number of the database server.
        table_name (str): Name of the table to upload rows to.
        df (pd.DataFrame): DataFrame containing the rows to upload.

    Returns:
        tuple: A tuple containing two DataFrames:
            - DataFrame of rows that were uploaded (to_upload_df).
            - DataFrame of rows that were not uploaded (not_to_upload_df).

    Raises:
        psycopg2.Error: If an error occurs while executing database operations.
    """
    def escape_single_quotes(value):
        """Escape single quotes in a string by doubling them."""
        if isinstance(value, str):
            return value.replace("'", "''")
        return value

    try:
        with psycopg2.connect(dbname=database, user=user, password=password, host=host, port=port) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
                table_columns = [row[0] for row in cur.fetchall()]

                # Remove 'id' and 'mod_date' columns
                if 'id' in table_columns:
                    table_columns.remove('id')
                if 'mod_date' in table_columns:
                    table_columns.remove('mod_date')

                # Add missing columns to the DataFrame with null values
                for col in table_columns:
                    if col not in df.columns:
                        df[col] = None

                # Extract columns that are in common between table_columns and the DataFrame
                common_columns = [col for col in table_columns if col in df.columns]
                df = df[common_columns]

                # Check rows for upload
                to_upload = []
                not_to_upload = []

                # Check if each row should be uploaded or not
                for index, row in df.iterrows():
                    # Construct the WHERE clause for the query
                    where_clauses = []
                    for col in df.columns:
                        value = row[col]
                        if value is None:
                            where_clauses.append(f"{col} IS NULL")
                        else:
                            where_clauses.append(f"{col}='{escape_single_quotes(value)}'")
                    where_clause = " AND ".join(where_clauses)
                    query = f"SELECT COUNT(*) FROM {table_name} WHERE {where_clause}"
                    cur.execute(query)
                    count = cur.fetchone()[0]
                    if count > 0:
                        not_to_upload.append(row)
                    else:
                        to_upload.append(row)

                to_upload_df = pd.DataFrame(to_upload, columns=df.columns)
                not_to_upload_df = pd.DataFrame(not_to_upload, columns=df.columns)

                # Upload the to_upload_df DataFrame to the table
                if not to_upload_df.empty:
                    values = ", ".join(["%s"] * len(to_upload_df.columns))
                    query = f"INSERT INTO {table_name} ({', '.join(to_upload_df.columns)}) VALUES ({values})"
                    cur.executemany(query, to_upload_df.values)
                    conn.commit()

                return to_upload_df, not_to_upload_df
    except psycopg2.Error as e:
        # Return an error message if an exception occurs
        return f"An error occurred: {str(e)}"
