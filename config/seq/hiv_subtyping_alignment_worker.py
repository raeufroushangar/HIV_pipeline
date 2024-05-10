import pandas as pd   
import numpy as np
from mafft_caller import perform_mafft_alignment
from similarity_calculator import calculate_similarity_between_aligned_seqs
from end_characters_cleaner import remove_consecutive_ends_n_and_hyphens_repeatedly
from hypermutation_calculator import analyze_mutations


def identify_unidentified_hiv_subtypes(alignment_result_df):
    """
    Identifies unidentified HIV subtypes based on a similarity threshold.

    Parameters:
    - alignment_result_df : DataFrame
        DataFrame containing alignment results.

    Returns:
    - DataFrame
        DataFrame with identified unidentified HIV subtypes.
    """
    SIMILARITY_THRESHOLD = 75

    # Step 1: Sort the DataFrame by 'hiv1_subtype_similarity_percentage' in descending order
    result_df = alignment_result_df.sort_values(by='hiv1_subtype_similarity_percentage', ascending=False)
    result_df = result_df.reset_index(drop=True)

    # Check if the similarity percentage of the top row is greater than or equal to the threshold
    if result_df.head(1)['hiv1_subtype_similarity_percentage'].tolist()[0] >= SIMILARITY_THRESHOLD:
        # If so, mark the top row as 'UI' and set it as the reference row
        top_row = result_df.head(1)
        top_row_similarity = top_row['hiv1_subtype_similarity_percentage'].tolist()[0]
        top_row_subtype = top_row['hiv1_subtype_lanl'].tolist()[0]

        # Step 2: Iterate through each row and apply the conditions
        for index, row in result_df.iloc[1:].iterrows():
            iterated_row_similarity = row['hiv1_subtype_similarity_percentage']
            iterated_row_subtype = row['hiv1_subtype_lanl']

            # Check if the iterated row has similarity greater than or equal to the threshold
            if iterated_row_similarity >= SIMILARITY_THRESHOLD:
                # Check if the absolute difference between top_row_similarity and iterated_row_similarity is within 1
                
                if top_row_subtype != iterated_row_subtype:
                    if abs(top_row_similarity - iterated_row_similarity) <= 1:
                        # If conditions are met, mark the row as 'UI'
                        result_df.at[index, 'hiv1_subtype_lanl_anomaly'] = 'UI'
    else:
        # If the top row doesn't meet the similarity threshold, mark it as 'UN'
        result_df.at[0, 'hiv1_subtype_lanl_anomaly'] = 'UN'
        top_row = result_df.head(1)

    # Check if any rows have 'UI' in 'hiv1_subtype_lanl_anomaly' column
    if result_df['hiv1_subtype_lanl_anomaly'].isin(['UI']).any():
        # If so, mark the reference row as 'UI'
        result_df.loc[0, 'hiv1_subtype_lanl_anomaly'] = 'UI'

    # Extract rows with 'UI'
    ui_rows = result_df[result_df['hiv1_subtype_lanl_anomaly'].isin(['UI'])]

    # Return either the rows with 'UI' or the reference row based on the presence of 'UI' rows
    if not ui_rows.empty:
        return ui_rows
    else:
        return top_row


def aggregate_duplicate_rows(subtyped_df):
    """
    Aggregates duplicate rows in a DataFrame based on specific columns.

    Parameters:
    - subtyped_df : DataFrame
        DataFrame containing duplicate rows.

    Returns:
    - DataFrame
        DataFrame with aggregated duplicate rows.
    """
    # Check for duplicates
    duplicates = subtyped_df.duplicated(subset=['pat_id', 'seq_sample_date'], keep=False)

    # Columns to perform list aggregation on
    list_aggregation_columns = ['hiv1_ref_seq_name', 
                                'hiv1_aligned_ref_seq',
                                'hiv1_aligned_query_seq',
                                'hiv1_subtype_alignment_score', 
                                'hiv1_subtype_similarity_percentage',
                                'hiv1_subtype_lanl', 
                                'hiv1_hypermut_p_value',
                                'hiv1_aligned_query_seq_cleaned',
                                'hiv1_aligned_query_seq_cleaned_len']
    
    # Group by 'pat_id' and 'seq_sample_date' for duplicates
    grouped = subtyped_df[duplicates].groupby(['pat_id', 'seq_sample_date'], as_index=False).agg({
        **{col: lambda x: x.tolist() for col in list_aggregation_columns},
        **{col: 'first' for col in subtyped_df.columns if col not in list_aggregation_columns}
    })

    # Include non-duplicate rows in the result and keep the first value for additional columns
    non_duplicates = subtyped_df[~duplicates].groupby(['pat_id', 'seq_sample_date'], as_index=False).first()

    # Concatenate the two results
    result_df = pd.concat([non_duplicates, grouped], ignore_index=True).sort_values(by='pat_id').reset_index(drop=True)
    return result_df


def perform_hiv_subtyping(quary_row_df, ref_seq_df, quary_seq_col_nam, mafft_executable):
    """
    This function aligns a query sequence against multiple reference sequences, calculates 
    alignment scores, and similarity percentages. It also performs HIV subtyping based on the 
    reference sequences' known subtypes and cleans the aligned query sequence. The function returns 
    a DataFrame with the alignment results, including extracted sequences, alignment scores, 
    similarity percentages, identified subtypes, and hypermutation analysis results.

    Parameters:
    - quary_row_df : DataFrame
        DataFrame containing the query sequence to be aligned.
    - ref_seq_df : DataFrame
        DataFrame containing the reference sequences with known subtypes.
    - quary_seq_col_nam : str
        Column name in quary_row_df containing the query sequence.

    Returns:
    - DataFrame
        DataFrame with alignment results including extracted sequences, alignment scores, similarity percentages,
        identified subtypes, and hypermutation analysis results.
    """
    query_seq = quary_row_df[quary_seq_col_nam].tolist()[0]
    # Create an empty list to store DataFrames
    result_list = []

    for index, ref_row in ref_seq_df.iterrows():
        ref_seq_name = ref_row['seq_name']
        ref_seq = ref_row['ref_seq']
        hiv1_subtype_lanl = ref_row['hiv1_subtype_lanl']

        aligned_ref_seq, aligned_query_seq = perform_mafft_alignment(ref_seq, query_seq, mafft_executable)
        alignment_score, similarity_percentage = calculate_similarity_between_aligned_seqs(aligned_ref_seq, aligned_query_seq)

        hiv1_aligned_query_seq_cleaned = remove_consecutive_ends_n_and_hyphens_repeatedly(aligned_query_seq)
        hiv1_aligned_query_seq_cleaned = hiv1_aligned_query_seq_cleaned.replace('-', '')
        hiv1_aligned_query_seq_cleaned_len = len(hiv1_aligned_query_seq_cleaned)
        alignment_df = pd.DataFrame({
            'hiv1_ref_seq_name': [ref_seq_name],
            'hiv1_aligned_ref_seq': [aligned_ref_seq],
            'hiv1_aligned_query_seq': [aligned_query_seq],
            'hiv1_subtype_alignment_score': [alignment_score],
            'hiv1_subtype_similarity_percentage': [similarity_percentage],
            'hiv1_subtype_lanl': [hiv1_subtype_lanl],
            'hiv1_subtype_lanl_anomaly': [''],
            'hiv1_hypermut_p_value':[np.nan],
            'hiv1_aligned_query_seq_cleaned': [hiv1_aligned_query_seq_cleaned],
            "hiv1_aligned_query_seq_cleaned_len": [hiv1_aligned_query_seq_cleaned_len]})

        quary_row_alignment_df = pd.concat([quary_row_df.reset_index(drop=True), alignment_df], axis=1)
        result_list.append(quary_row_alignment_df)

    result_df = pd.concat(result_list, ignore_index=True)
    
    # Assign 'UI' and 'UK, and return either if Assigned. Otherwsie, return highest hiv1_subtype_similarity_percentage row
    identify_unidentified_result_df = identify_unidentified_hiv_subtypes(result_df)

    # Calculate hypermutation
    identify_unidentified_result_df['hiv1_hypermut_p_value'] = identify_unidentified_result_df.apply(lambda row: analyze_mutations(row['hiv1_aligned_query_seq'], row['hiv1_aligned_ref_seq']), axis=1)

    # Aggraget rows with same 'pat_id' and 'seq_sample_date'  
    processed_result_df = aggregate_duplicate_rows(identify_unidentified_result_df)
    
    return processed_result_df