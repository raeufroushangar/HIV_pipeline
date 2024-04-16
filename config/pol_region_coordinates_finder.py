def extracting_seq_within_pol_region(ref_seq, query_seq, ref_seq_pol_start_coord, ref_seq_pol_end_coord):
    """
    Extracts subsequences from reference and query sequences based on pol region start and end coordinates.

    Parameters:
    - ref_seq (str): Reference DNA sequence.
    - query_seq (str): Query DNA sequence.
    - ref_seq_pol_start_coord (int): start coordinate for the pol-region in the reference sequence.
    - ref_seq_pol_end_coord (int):End coordinate for the pol-region in the reference sequence.

    Returns:
    - Tuple of extracted reference sequence, extracted query sequence, start position in query, end position in query.
    """
    if len(ref_seq) != len(query_seq):
        return "ref_seq and query_seq must have the same length."

    current_position_ref = 0  # current position tracker for the reference sequence
    
    start_coord_reached = False
    end_coord_reached = False
    
    query_pol_start_coord = 0
    query_pol_end_coord = 0
    
    extracted_ref_seq = ""

    # Iterate through the reference sequence
    for base in ref_seq:
        if not start_coord_reached:
            query_pol_start_coord += 1
        if not end_coord_reached:
            query_pol_end_coord += 1
        if base != '-':
            current_position_ref += 1

        # Check if the current position matches the start coordinate
        if current_position_ref == ref_seq_pol_start_coord:
            start_coord_reached = True
        # If the start coordinate is reached, extract the reference sequence
        if start_coord_reached:
            extracted_ref_seq += base
            # Check if the current position matches the end coordinate
            if current_position_ref == ref_seq_pol_end_coord:
                end_coord_reached = True
                break
            
    # Extract the corresponding region from the query sequence
    extracted_query_seq = query_seq[query_pol_start_coord-1:query_pol_end_coord]

    return extracted_ref_seq, extracted_query_seq, query_pol_start_coord, query_pol_end_coord