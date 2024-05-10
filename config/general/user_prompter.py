from file_reading_operations import read_data_file
from path_finder import find_path_of_file_or_dir 
import pandas as pd


def create_dic_from_tbl_descr(dataframe):
    """
    Creates a dictionary from table descriptions.

    Args:
        dataframe (pandas.DataFrame): DataFrame containing 'tbl_name' and 'description' columns.

    Returns:
        dict: A dictionary where table names are keys and their descriptions are values.
    """
    dictionary = {}
    for index, row in dataframe.iterrows():
        dictionary[row['tbl_name']] = row['description']
    return dictionary


def create_dic_from_col_descr(col_descr_df, tbl_name_str):
    """
    Creates a dictionary containing column descriptions, data types, and upload status for a specified table.

    Args:
        col_descr_df (pandas.DataFrame): DataFrame with column descriptions, data types, and upload status.
        tbl_name_str (str): Name of the table for which column descriptions are needed.

    Returns:
        dict: Dictionary where column names are keys, and values are lists with description, datatype, and upload status.
    """
    # Filter columns for the specified table and upload status
    filtered_df = col_descr_df[(col_descr_df['tbl_name'] == tbl_name_str) & ((col_descr_df['upload_status'] == 'must upload') | (col_descr_df['upload_status'] == 'optional'))]

    result_dict = {}  
    for index, row in filtered_df.iterrows():  
        result_dict[row['col_name']] = [row['description'], row['datatype'], row['upload_status']]
    return result_dict  


def get_user_input_or_exit(prompt, header=''):
    """
    Prompts the user for input and handles 'exit' or 'esc' to confirm exit.

    Args:
        prompt (str): The prompt to display to the user, which may include a header.
        header (str): Optional header to include in the prompt.

    Returns:
        str or None or bool: User input if not 'exit' or 'esc', None if user confirms exit, False if user cancels exit.
    """
    user_input = input(prompt.format(header=header)).strip().lower()
    if user_input in ['esc', 'exit']:
        confirm_exit = input("\nAre you sure you want to exit? (yes/no):").lower()
        if confirm_exit == "yes":
            print("Exiting...")
            return None
        else:
            return False
    return user_input


def display_accepted_data_types(tbl_descr_dict):
    """
    Displays accepted data types for each table.

    Args:
        tbl_descr_dict (dict): Dictionary containing table names as keys and their descriptions as values.
    """
    print("\nAccepted data files:")
    for tbl_name, tbl_description in tbl_descr_dict.items():
        print(f"{tbl_name}: {tbl_description}")


def get_data_file_type_input(tbl_descr_df, col_descr_df):
    """
    Prompts the user to input/select a data file type and validates it against accepted types.

    Args:
        tbl_descr_df (pandas.DataFrame): DataFrame containing table descriptions.
        col_descr_df (pandas.DataFrame): DataFrame containing column descriptions, data types, and upload status.

    Returns:
        dict or None: A dictionary containing column descriptions, data types, and upload status for the selected data file type, or None if the user exits.
    """
    tbl_descr_dict = create_dic_from_tbl_descr(tbl_descr_df)
    while True:
        display_accepted_data_types(tbl_descr_dict)
        user_file_type_input = get_user_input_or_exit("Please input/select a data file, or type 'esc' to exit:")
        if user_file_type_input is None:  # User chose to exit
            return None
        if user_file_type_input:  # If user_input is not False (i.e., user didn't confirm exit)
            result_dict = create_dic_from_col_descr(col_descr_df, user_file_type_input)
            if result_dict:
                return result_dict
            else:
                print(f"\nThe entry '{user_file_type_input}' is not an acceptable data file type. Please try again.")

def get_user_input(header, dic_copy):
    """
    Prompts the user to input/select a match for a header and validates it against accepted matches.

    Args:
        header (str): The header for which the user is providing a match.
        dic_copy (dict): A copy of a dictionary containing accepted matches.

    Returns:
        str or None: The user-selected match for the header, or None if the user exits.
    """
    while True:
        user_input = get_user_input_or_exit(
            f"\nPlease input/select a match for '{header}', or type 'esc' to exit:")
        if user_input is None:  # User chose to exit
            return None
        if user_input in dic_copy:
            confirm = input(f"Is '{user_input}' the correct match for '{header}'? (yes/no):").strip().lower()
            if confirm == 'yes':
                del dic_copy[user_input]  # Remove the matched key:value pair from the dictionary
                return user_input
            else:
                print("Please try again.")
        else:
            print(f"\n'{user_input}' is not an accepted header. Please try again.")


def compare_headers_to_dict(df_original):
    """
    Compares headers of a DataFrame to a dictionary containing accepted headers and prompts for corrections if necessary.

    Args:
        df_original (pandas.DataFrame): Original DataFrame with headers to be compared.

    Returns:
        pandas.DataFrame or None: A DataFrame with corrected headers if necessary, or None if no corrections were made or if user exits.
    """
    tbl_descr_path = find_path_of_file_or_dir('assets/tbl_description.xlsx')
    tbl_descr = read_data_file(tbl_descr_path)
    
    col_descr_path = find_path_of_file_or_dir('assets/col_description.xlsx')
    col_descr = read_data_file(col_descr_path)
    
    data_file_dict = get_data_file_type_input(tbl_descr, col_descr)
    
    if data_file_dict:
        print("\nAccepted headers:")
        for key, value in data_file_dict.items():
            print(f"{key}: {value}")        
            
        headers = list(df_original.columns)
        mismatched_headers = []
        for header in headers:
            if header not in data_file_dict:
                mismatched_headers.append(header)
        if mismatched_headers:
            data_file_dict_copy = data_file_dict.copy()  # Make a copy of the dictionary
            df_copy = df_original.copy()  # Make a copy of the dataframe
            for header in mismatched_headers:
                matched_header = get_user_input(header, data_file_dict_copy)
                if matched_header is None:
                    return  # Exit the function if user chooses to exit
                df_copy.rename(columns={header: matched_header}, inplace=True)  # Rename the header in the copy
        # Create a new dictionary containing only keys with 'must upload' as the third element in the value list
        must_upload_dict = {key: value for key, value in data_file_dict_copy.items() if value[2] == 'must upload'}
        if must_upload_dict:
            print("\nThe following columns must be in the datafile for the data to be processed:")
            print(must_upload_dict)

            return compare_headers_to_dict(df_original)  # Recursively call with the copied dataframe
        else:
            return df_copy, data_file_dict
    else:
        print("No data file dictionary found.")
        return None


def filter_dataframe_by_datatype(df, column_datatype_dict):
    """
    Filter the dataframe by datatype.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        column_datatype_dict (dict): A dictionary where keys are column names and values are tuples
            containing a description of the column, its datatype, and a requirement indicator.

    Returns:
        tuple: A tuple containing two DataFrames. The first DataFrame contains the rows with invalid data types,
            and the second DataFrame contains the cleaned original DataFrame.

    """
    # Initialize a DataFrame to store rows with invalid data types
    filtered_rows = pd.DataFrame(columns=df.columns)
    
    # Iterate through each column in the dictionary
    for column, (description, datatype, requirement) in column_datatype_dict.items():
        if column in df.columns:
            if column == 'pat_id':
                # Filter out rows with invalid pat_id values
                invalid_rows = df[~(df[column].apply(lambda x: str(x).isdigit()) | df[column].isnull())]
                filtered_rows = pd.concat([filtered_rows, invalid_rows])
                df = df.drop(invalid_rows.index)
            elif datatype == 'INTEGER':
                # Convert the column to integer datatype if not null
                non_null_rows = df[df[column].notnull()]
                try:
                    non_null_rows[column] = pd.to_numeric(non_null_rows[column], errors='coerce', downcast='integer')
                    invalid_rows = non_null_rows[pd.isnull(non_null_rows[column])]
                    filtered_rows = pd.concat([filtered_rows, invalid_rows])
                    df = df.drop(invalid_rows.index)
                except ValueError:
                    # Handle rows with invalid integer values
                    invalid_rows = non_null_rows[pd.to_numeric(non_null_rows[column], errors='coerce').isnull()]
                    filtered_rows = pd.concat([filtered_rows, invalid_rows])
                    df = df.drop(invalid_rows.index)
            elif datatype == 'DATE':
                # Convert the column to datetime datatype if not null
                non_null_rows = df[df[column].notnull()]
                try:
                    non_null_rows[column] = pd.to_datetime(non_null_rows[column], errors='coerce')
                    invalid_rows = non_null_rows[pd.isnull(non_null_rows[column])]
                    filtered_rows = pd.concat([filtered_rows, invalid_rows])
                    df = df.drop(invalid_rows.index)
                except ValueError:
                    # Handle rows with invalid date values
                    invalid_rows = non_null_rows[pd.to_datetime(non_null_rows[column], errors='coerce').isnull()]
                    filtered_rows = pd.concat([filtered_rows, invalid_rows])
                    df = df.drop(invalid_rows.index)
            elif datatype == 'STRING':
                # Filter out rows with non-string values
                invalid_rows = df[df[column].notnull() & ~df[column].apply(lambda x: isinstance(x, str))]
                filtered_rows = pd.concat([filtered_rows, invalid_rows])
                df = df.drop(invalid_rows.index)
            else:
                # Skip unsupported data types
                continue
    
    # Return the filtered rows and the cleaned DataFrame
    return df, filtered_rows


def data_upload_and_header_matching():
    """
    Prompts the user to provide a data file path, reads the file, and compares its headers to a dictionary of accepted headers.

    Returns:
        pandas.DataFrame or None: A DataFrame with corrected headers if necessary, or None if no corrections were made or if user exits.
    """
    while True:
        user_input = get_user_input_or_exit("Please provide data file path, or type 'esc' to exit:")
        if user_input is None:  # User chose to exit
            return None
        try:
            seq_df = read_data_file(user_input)
            if seq_df is not None and not seq_df.empty:
                seq_df, data_file_dict = compare_headers_to_dict(seq_df)
                # Integrate the filter_dataframe_by_datatype function here
                updated_seq_df, filtered_rows = filter_dataframe_by_datatype(seq_df, data_file_dict)
                return updated_seq_df, filtered_rows
        except Exception as e:
            print(e)  # Print the error message if an exception occurs during file reading