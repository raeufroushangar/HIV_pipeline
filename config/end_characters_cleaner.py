import re

def remove_consecutive_ends_n_and_hyphens_repeatedly(sequence):
    """
    Remove consecutive '-' characters and 'n' characters from both ends of a sequence repeatedly until none are left.
    
    Args:
        sequence (str): The sequence to clean.
        
    Returns:
        str: The cleaned sequence.
    
    Example:
        >>> remove_n_and_hyphens_repeatedly("nnn--nnnA--TG-CGnnn--nnn--")
        'A--TG-CG'
    """
    while True:
        # Check if the sequence starts or ends with 'n' or '-'
        if sequence.startswith('n') or sequence.endswith('n') or sequence.startswith('-') or sequence.endswith('-'):
            # Remove consecutive 'n' characters from both ends
            sequence = re.sub(r'^n+|n+$', '', sequence, flags=re.IGNORECASE)
            # Remove consecutive '-' characters from both ends
            sequence = re.sub(r'^-+|-+$', '', sequence, flags=re.IGNORECASE)
        else:
            break  # Break out of the loop if no more 'n' or '-' characters are found
    return sequence.strip()