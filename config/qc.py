import re
from end_characters_cleaner import remove_consecutive_ends_n_and_hyphens_repeatedly
from multistate_character_cleaner import replacing_multistate_characters_with_n 

def remove_empty_or_none_sequences(seq_table):
    """
    Identifies rows with empty or None 'seq' values in a DataFrame and removes them.

    Parameters:
    - seq_table (pandas.DataFrame): Data containing 'seq' column.

    Returns:
    - tuple: (cleaned, empty)
        - cleaned (pandas.DataFrame): DataFrame with empty or None 'seq' rows removed.
        - empty (pandas.DataFrame): DataFrame containing the empty or None 'seq' rows.
    """
    # Find rows where 'seq' is empty or None.
    empty_rows = seq_table[(seq_table['seq'] == '') | (seq_table['seq'].isnull())]
    
    # Check if there are any empty sequences to drop
    if not empty_rows.empty:
        # Remove rows with empty or None 'seq' values from the original DataFrame
        seq_table = seq_table.drop(empty_rows.index)
    # Return both the cleaned DataFrame and the DataFrame containing empty sequences
    return seq_table, empty_rows

def find_and_remove_duplicates(seq_table):
    """
    Identifies and removes duplicate rows from a DataFrame.

    Parameters:
    - seq_table (DataFrame): The DataFrame to process.

    Returns:
    - tuple: (duplicates, unique)
        - duplicates (DataFrame): Duplicate rows, excluding their first occurrence.
        - unique (DataFrame): DataFrame with duplicates removed.
    """
    duplicate_rows = seq_table[seq_table.duplicated()]  # Find duplicate rows, excluding the first occurrence
    seq_table_cleaned = seq_table.drop_duplicates()     # Remove duplicates, keep first occurrence
    return seq_table_cleaned, duplicate_rows

def remove_n_only_sequences(seq_table):
    """
    Identifies and removes rows with sequences consisting of only 'n' characters.

    Parameters:
    - seq_table (pandas.DataFrame): Data containing 'seq' column.

    Returns:
    - tuple: (cleaned, n_only)
        - cleaned (pandas.DataFrame): DataFrame with rows containing 'n' only sequences removed.
        - n_only (pandas.DataFrame): DataFrame containing the rows with 'n' only sequences.
    """
    # Create a mask to identify rows with sequences consisting of 'n' characters
    mask = seq_table['seq'].apply(lambda x: x == 'n' * len(x))
    # Identify rows with 'n' only sequences
    n_only_sequences = seq_table[mask]
    # Drop rows that meet the condition
    seq_table_cleaned = seq_table[~mask]
    return seq_table_cleaned, n_only_sequences

def remove_low_acgt_ratio_sequences(seq_table):
    """
    Identifies and removes rows with low ACGT ratio sequences.

    Parameters:
    - seq_table (pandas.DataFrame): Data containing 'seq_cleaned' column.

    Returns:
    - tuple: (cleaned, low_acgt_ratio)
        - cleaned (pandas.DataFrame): DataFrame with low ACGT ratio sequences removed.
        - low_acgt_ratio (pandas.DataFrame): DataFrame containing the rows with low ACGT ratio sequences.
    """
    # Create a function to calculate the ratio of each a, c, g, t, and n character separately
    def base_ratio(sequence, base):
        base_count = sequence.count(base)
        total_count = len(sequence)
        return base_count / total_count

    # Calculate the ratios for each base (a, c, g, t) and add them as new columns
    bases = ['a', 'c', 'g', 't']
    for base in bases:
        seq_table[f'{base}_ratio'] = seq_table['seq_cleaned'].apply(lambda x: base_ratio(x, base))

    # Calculate the 'acgt_ratio' and add it as a new column
    seq_table['acgt_ratio'] = seq_table[['a_ratio', 'c_ratio', 'g_ratio', 't_ratio']].sum(axis=1)

    # Calculate the 'non_acgtn_ratio' and add it as a new column
    seq_table['non_acgt_ratio'] = 1 - seq_table['acgt_ratio']

    # Identify rows with low ACGT ratio sequences
    low_acgt_ratio_sequences = seq_table[(seq_table['non_acgt_ratio'] >= seq_table['acgt_ratio'])]

    # Remove rows with low ACGT ratio sequences
    seq_table_cleaned = seq_table.drop(low_acgt_ratio_sequences.index)
    return seq_table_cleaned, low_acgt_ratio_sequences

def remove_consecutive_internal_ns(seq, n=30):
    """
    Remove consecutive 'n' characters that occur internally in a DNA sequence.

    Parameters:
    - seq (str): The DNA sequence string.
    - n (int): The minimum number of consecutive 'n' characters to remove (default is 30).

    Returns:
    - str: The modified DNA sequence with consecutive internal 'n' characters removed.
    """
    # Create a regular expression pattern to match consecutive 'n' characters
    pattern = f'n{{{n},}}'
    # Use re.sub to replace the matched pattern with an empty string
    seq_cleaned = re.sub(pattern, '', seq)
    return seq_cleaned

def remove_short_sequences(seq_table, col_name, seq_len):
    """
    Removes sequences shorter than or equal to a specified length.

    Parameters:
    - seq_table (pandas.DataFrame): Data containing the column with sequence lengths.
    - col_name (str): The name of the column containing the sequence lengths.
    - seq_len (int): The maximum allowed sequence length (inclusive).

    Returns:
    - pandas.DataFrame: DataFrame with sequences shorter than or equal to seq_len removed.
    """
    # Create a mask to identify sequences shorter than or equal to seq_len
    mask = seq_table[col_name] <= seq_len
    # Identify rows with sequences shorter than or equal to seq_len
    short_sequences = seq_table[mask]
    # Drop rows that meet the condition
    seq_table_cleaned = seq_table[~mask]
    return seq_table_cleaned, short_sequences

def process_sequences(seq_table):
    """
    Process a DataFrame with sequences, removing empty, 'n' only sequences,
    and identifying and removing duplicate sequences. Also removes sequences shorter than a specified length.

    Parameters:
    - seq_table (pandas.DataFrame): Data containing 'seq' column.

    Returns:
    - dict: A dictionary with statements as keys and resulting DataFrames or details as values.
    """

    # Lowercase all sequences
    seq_table['seq'] = seq_table['seq'].str.lower()
    
    results = {}
    original_count = len(seq_table)

    # Remove empty or None sequences
    seq_table, empty_rows = remove_empty_or_none_sequences(seq_table)
    empty_count = len(empty_rows)
    results["empty_statement"] = f"Empty or None sequences removed: {empty_count} rows, remaining {len(seq_table)} rows."
    results["empty_df"] = empty_rows

    # Find and remove duplicates
    seq_table, duplicate_rows = find_and_remove_duplicates(seq_table)
    duplicates_count = len(duplicate_rows)
    results["duplicate_statement"] = f"Duplicate sequences removed: {duplicates_count} rows, remaining {len(seq_table)} rows."
    results["duplicate_df"] = duplicate_rows
    
    # Remove 'n' only sequences
    seq_table, n_only_sequences = remove_n_only_sequences(seq_table)
    n_only_count = len(n_only_sequences)
    results["n_only_statement"] = f"'N' only sequences removed: {n_only_count} rows, remaining {len(seq_table)} rows."
    results["n_only_df"] = n_only_sequences
    
    # Remove consecutive 'n' and/or '-' from either end repeatedly
    seq_table['seq_cleaned'] = seq_table['seq'].apply(remove_consecutive_ends_n_and_hyphens_repeatedly)

    # Remove sequences with low ACGT ratio
    seq_table, low_acgt_ratio_sequences = remove_low_acgt_ratio_sequences(seq_table)
    low_acgt_count = len(low_acgt_ratio_sequences)
    results["low_acgt_ratio_statement"] = f"Low ACGT ratio sequences removed: {low_acgt_count} rows, remaining {len(seq_table)} rows."
    results["low_acgt_ratio_df"] = low_acgt_ratio_sequences

    # Call seq_poly_cleaner to replace all non-acgt and abnormal IUPAC characters to 'n' 
    seq_table['seq_cleaned'] = seq_table['seq_cleaned'].apply(replacing_multistate_characters_with_n)

    # Remove consecutive 'n' and/or '-' from either end repeatedly
    seq_table['seq_cleaned'] = seq_table['seq_cleaned'].apply(remove_consecutive_ends_n_and_hyphens_repeatedly)
    
    # Remove consecutive internal n's >= 30 nucleotides
    seq_table['seq_cleaned'] = seq_table['seq_cleaned'].apply(remove_consecutive_internal_ns)

    # Add a new column with the length of each string
    seq_table['seq_cleaned_len'] = seq_table['seq_cleaned'].apply(len)
    
    # Remove sequences with length < 583 nucleotides 
    seq_table, short_sequences = remove_short_sequences(seq_table, 'seq_cleaned_len', 583)
    short_count = len(short_sequences)
    results["short_statement"] = f"Short sequences (< 583 nt) removed: {short_count} rows, remaining {len(seq_table)} rows."
    results["short_df"] = short_sequences

    final_count = len(seq_table)
    rows_removed = original_count - final_count

    summary_statement = (
        f"\nInitial dataset contained {original_count} rows.",
        f"\nEmpty or None sequences: {empty_count}."
        f"\nDuplicate sequences: {duplicates_count}."
        f"\n'N' only sequences: {n_only_count}."
        f"\nLow ACGT ratio sequences: {low_acgt_count}."
        f"\nShort sequences (< 583 nt): {short_count}.",
        f"\n{rows_removed} rows removed in total.",
        f"\nFinal dataset contains {final_count} rows."
    )
 
    results["summary"] = '\n'.join(summary_statement)
    return results, seq_table


def categorize_hiv_typing(hiv_typing_df):
    """
    Categorize sequences into HIV-2, HIV-1, and unknown (not typed) based on their 'hiv_type_lanl' classification,
    'hiv_type_similarity_percentage', and remove sequences shorter than 583 nucleotides.
    
    Parameters:
    - hiv_typing_df (pandas.DataFrame): DataFrame containing 'hiv_type_lanl', 'hiv_type_similarity_percentage', and sequence length.
    
    Returns:
    - dict: A dictionary with statements and DataFrames for each HIV type category, including removed short sequences, and a summary.
    """
    results = {}

    original_count = len(hiv_typing_df)
    
    # Continue with HIV typing categorization
    hiv2_typing_df = hiv_typing_df[hiv_typing_df['hiv_type_lanl'] == 'HIV-2']
    not_hiv_typing_df = hiv_typing_df[hiv_typing_df['hiv_type_similarity_percentage'] < 75]
    
    # Conditions for HIV-1
    condition_hiv1 = (hiv_typing_df['hiv_type_lanl'] != 'HIV-2') & (hiv_typing_df['hiv_type_similarity_percentage'] >= 75)
    hiv1_typing_df = hiv_typing_df[condition_hiv1]
    
    # Assigning categorized DataFrames to results
    results["hiv2_statement"] = f"HIV-2 classified sequences: {len(hiv2_typing_df)} rows."
    results["hiv2_df"] = hiv2_typing_df
    
    results["not_hiv_statement"] = f"Sequences not typed or below 75% similarity: {len(not_hiv_typing_df)} rows."
    results["not_hiv_df"] = not_hiv_typing_df
    
    results["hiv1_statement"] = f"HIV-1 classified sequences: {len(hiv1_typing_df)} rows."
    results["hiv1_df"] = hiv1_typing_df

    # Remove sequences shorter than 583 nucleotides
    hiv_typing_df, short_sequences = remove_short_sequences(hiv_typing_df, 'extracted_pol_query_seq_cleaned_len', 583)

    results["short_statement"] = f"Short sequences (< 583 nt) removed: {len(short_sequences)} rows, remaining {len(hiv_typing_df)} rows."
    results["short_df"] = short_sequences
    # Summary

    summary_statement = (
        f"Initial dataset contained {original_count} sequences.",
        f"Short sequences (< 583 nt) removed: {len(short_sequences)}.",
        f"\nHIV-2 classified sequences: {len(hiv2_typing_df)}.",
        f"Sequences not typed or below 75% similarity: {len(not_hiv_typing_df)}.",
        f"HIV-1 classified sequences: {len(hiv1_typing_df)}.",
        f"\nData has been categorized into HIV-1, HIV-2, and Unknown (or low similarity) types."
    )
    results["summary"] = '\n'.join(summary_statement)
    return results