import subprocess
import logging

def perform_mafft_alignment(ref_seq, query_seq, mafft_executable):
    """
    Perform sequence alignment using MAFFT.

    Args:
        ref_seq (str): The reference sequence.
        query_seq (str): The query sequence.
        mafft_executable (str): Path to the MAFFT executable.

    Returns:
        Tuple[str, str] or str: Aligned reference and query sequences, or an error message.
    """
    try:
        # Validate input data
        if not ref_seq or not query_seq:
            raise ValueError("Invalid input sequences")

        # MAFFT command and input data
        mafft_command = [mafft_executable, "--auto", "--text", "--quiet", "-"]
        input_data = f">reference\n{ref_seq}\n>query\n{query_seq}"

        # Run MAFFT and capture output
        process = subprocess.run(mafft_command, input=input_data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check for errors in MAFFT execution
        if process.returncode != 0:
            raise RuntimeError("Error running MAFFT: " + process.stderr)

        # Parse MAFFT output
        aligned_output = process.stdout.strip().split('\n')

        # Check for errors in parsing MAFFT output
        if '>reference' not in aligned_output or '>query' not in aligned_output:
            raise RuntimeError("Error parsing MAFFT output.")

        # Extract aligned sequences
        aligned_ref_seq_index = aligned_output.index('>reference')
        aligned_query_seq_index = aligned_output.index('>query')

        aligned_ref_seq = ''.join(aligned_output[aligned_ref_seq_index + 1:aligned_query_seq_index])
        aligned_query_seq = ''.join(aligned_output[aligned_query_seq_index + 1:])

        return aligned_ref_seq, aligned_query_seq

    except Exception as e:
        # Log the exception for debugging purposes
        logging.error(f"An error occurred: {str(e)}")
        # Provide a generic error message
        return "An unexpected error occurred during sequence alignment."

