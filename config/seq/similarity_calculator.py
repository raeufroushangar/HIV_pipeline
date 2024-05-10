from end_characters_cleaner import remove_consecutive_ends_n_and_hyphens_repeatedly

def calculate_similarity_between_aligned_seqs(aligned_ref_seq, aligned_query_seq):
    """
    Calculates the similarity between two aligned DNA sequences.

    Args:
    - aligned_ref_seq (str): Aligned reference DNA sequence.
    - aligned_query_seq (str): Aligned query DNA sequence.

    Returns:
    - alignment_score (int): The count of matching bases in the aligned sequences.
    - similarity_percentage (float): The percentage of similarity between the sequences.

    The function removes consecutive 'n' characters from both ends of each sequence,
    then computes the alignment score based on matching bases and calculates the
    similarity percentage between the cleaned query sequence and the reference sequence.

    Note: This function assumes that the input sequences are aligned and of the same length.
    """
    alignment_score = sum(1 for base1, base2 in zip(aligned_ref_seq, aligned_query_seq) if base1 == base2 and base1 != '-')
    
    # Remove consecutive 'n' and '-' characters from both ends of each sequence
    cleaned_query_seq = remove_consecutive_ends_n_and_hyphens_repeatedly (aligned_query_seq)
    # Handle empty sequence
    if len(cleaned_query_seq) == 0:
        return alignment_score, 0.0

    similarity_percentage = round((alignment_score / len(cleaned_query_seq)) * 100, 1)
    
    return alignment_score, similarity_percentage
