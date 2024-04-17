import pandas as pd   
from mafft_caller import perform_mafft_alignment
from pol_region_coordinates_finder import extracting_seq_within_pol_region
from similarity_calculator import calculate_similarity_between_aligned_seqs
from end_characters_cleaner import remove_consecutive_ends_n_and_hyphens_repeatedly

def perform_hiv_typing(quary_row_df, ref_seq_df, quary_seq_col_nam, mafft_executable):
    """
    This function aligns a query sequence against two reference sequences (HXB2 and SIVMM239), 
    calculates similarity percentages, determines the HIV type based on a similarity threshold, 
    and cleans the query sequence by removing consecutive 'n' and '-'  characters from both ends. 
    It returns a DataFrame with the alignment results, including extracted sequences, alignment 
    scores, similarity percentages, and HIV type classification.

    Parameters:
    - quary_row_df : DataFrame
        DataFrame containing the query sequence to be aligned.
    - ref_seq_df : DataFrame
        DataFrame containing the reference sequences (HXB2 and SIVMM239).
    - quary_seq_col_nam : str
        Column name in quary_row_df containing the query sequence.
    - mafft_executable : str
        Path to the MAFFT executable.

    Returns:
    - DataFrame
        DataFrame with alignment results including extracted sequences, alignment scores,
        similarity percentages, and HIV type classification.
    """    
    SIMILARITY_THRESHOLD = 75
    # Extracting reference sequences
    hxb2_row = ref_seq_df[ref_seq_df['seq_name'] == 'HXB2']
    sivmm239_row = ref_seq_df[ref_seq_df['seq_name'] == 'SIVMM239']
    hxb2_ref_seq = hxb2_row['pol_ref_seq'].tolist()[0]
    sivmm239_ref_seq = sivmm239_row['pol_ref_seq'].tolist()[0]
    
    # Extracting query sequence
    query_seq = quary_row_df[quary_seq_col_nam].tolist()[0]

    # 1st alignment using HXB2 as reference
    hxb2_pol_start_coord = hxb2_row['hiv_typing_pol_start_coord'].tolist()[0]
    hxb2_pol_end_coord = hxb2_row['hiv_typing_pol_end_coord'].tolist()[0]  
    aligned_ref_seq, aligned_query_seq = perform_mafft_alignment(hxb2_ref_seq, query_seq, mafft_executable)
    extracted_pol_ref_seq, extracted_pol_query_seq, query_pol_start_coord, query_pol_end_coord = extracting_seq_within_pol_region(aligned_ref_seq, aligned_query_seq, hxb2_pol_start_coord, hxb2_pol_end_coord)
    alignment_score, similarity_percentage = calculate_similarity_between_aligned_seqs(extracted_pol_ref_seq, extracted_pol_query_seq)

    # Determining HIV type based on similarity threshold
    if similarity_percentage >= SIMILARITY_THRESHOLD:
        hiv_type_lanl = "HIV-1"
    else:
        # 2nd alignment using SIVMM239 as reference
        sivmm239_pol_start_coord = sivmm239_row['hiv_typing_pol_start_coord'].tolist()[0]
        sivmm239_pol_end_coord = sivmm239_row['hiv_typing_pol_end_coord'].tolist()[0] 
        aligned_ref_seq, aligned_query_seq = perform_mafft_alignment(sivmm239_ref_seq, query_seq, mafft_executable)
        extracted_pol_ref_seq, extracted_pol_query_seq, query_pol_start_coord, query_pol_end_coord = extracting_seq_within_pol_region(aligned_ref_seq, aligned_query_seq, sivmm239_pol_start_coord, sivmm239_pol_end_coord)
        alignment_score, similarity_percentage = calculate_similarity_between_aligned_seqs(extracted_pol_ref_seq, extracted_pol_query_seq)

        if similarity_percentage >= SIMILARITY_THRESHOLD:
            hiv_type_lanl = "HIV-2"
        else:
            hiv_type_lanl = None
            
    # Cleaning the query sequence
    extracted_pol_query_seq_cleaned = remove_consecutive_ends_n_and_hyphens_repeatedly(extracted_pol_query_seq)
    extracted_pol_query_seq_cleaned = extracted_pol_query_seq_cleaned.replace('-', '')

    # Calculate the length of the cleaned sequence
    extracted_pol_query_seq_cleaned_len = len(extracted_pol_query_seq_cleaned)

    # Create a DataFrame for the current file
    df_entry = pd.DataFrame({"extracted_pol_ref_seq": [extracted_pol_ref_seq],
                             "extracted_pol_query_seq": [extracted_pol_query_seq],
                             "extracted_pol_query_seq_start_coord": [query_pol_start_coord],
                             "extracted_pol_query_seq_end_coord": [query_pol_end_coord],
                             "hiv_type_alignment_score": [alignment_score],
                             "hiv_type_similarity_percentage": [similarity_percentage],
                             "hiv_type_lanl": [hiv_type_lanl],
                             "extracted_pol_query_seq_cleaned": [extracted_pol_query_seq_cleaned],
                             "extracted_pol_query_seq_cleaned_len": [extracted_pol_query_seq_cleaned_len]})
    
    # Concatenate the result with the original DataFrame
    result_df = pd.concat([quary_row_df.reset_index(drop=True), df_entry], axis=1)
    return result_df
