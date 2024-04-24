import os
import pandas as pd
import json


def read_data_file(file_path):
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        # Check if the file path is a file
        if not os.path.isfile(file_path):
            return "File not found."
        
        # Check the file extension to determine the format
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, keep_default_na=False)
        elif file_path.endswith('.txt') or file_path.endswith('.tab') or file_path.endswith('.tsv'):
            df = pd.read_csv(file_path, delimiter='\t', keep_default_na=False)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, keep_default_na=False)
        else:
            return "Invalid file format. Only CSV, tab-delimited TXT/TSV/TAB, and Excel files are supported."
        
        # Replace empty cells with None
        df.replace('', None, inplace=True)
        
        # Check if the DataFrame has at least two columns
        if len(df.columns) < 2:
            return "Parsing error. Please check the file content."
        
        if df.empty:
            return "File is empty."
        return df
    
    except pd.errors.ParserError:
        return "Parsing error. Please check the file format and content."
    except Exception as e:
        return f"{str(e)}"
    
    
def read_db_tables_from_json(json_file_path):
    """
    Read table information from a JSON file and return a list of dictionaries.
    
    Each dictionary should have keys 'table_name' and 'columns', where 'columns' is a dictionary of column names and types.
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            return data
    except Exception as e:
        return f"Error reading JSON file: {str(e)}"
