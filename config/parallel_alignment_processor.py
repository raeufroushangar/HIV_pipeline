import psutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd   
import numpy as np

def process_sequence_alignment_parallel(query_df, ref_seq_df, query_seq_col_name, worker_func,
                                        mafft_executable):
    """
    Process sequence alignment in parallel using ThreadPoolExecutor.

    Args:
    - query_df (pandas.DataFrame): DataFrame containing query sequences.
    - ref_seq_df (pandas.DataFrame): DataFrame containing reference sequences.
    - query_seq_col_name (str): Name of the column containing query sequences.

    Returns:
    - pandas.DataFrame or str: Result DataFrame if successful, error message if failed.
    """
    try:
        # Attempt to retrieve the number of physical CPU cores
        num_physical_cores = psutil.cpu_count(logical=False)
        if num_physical_cores is None:
            # Fallback to a default if the number of physical cores cannot be determined
            num_physical_cores = 1
        total_threads = max(2 * num_physical_cores, 1)  # Ensure at least 1 thread is used
    except Exception as e:
        # Directly return the error message without proceeding to processing
        return f"Error getting system cores: {e}"

    with ThreadPoolExecutor(max_workers=total_threads) as executor:
        
        futures = []
        def process_chunk(chunk):
            result_df = []
            for _, row in chunk.iterrows():
                query_row_df = pd.DataFrame(row).transpose()
                result = worker_func(query_row_df, ref_seq_df, query_seq_col_name, mafft_executable)
                if result is not None and not result.empty:
                    result_df.append(result)
            if result_df:
                return pd.concat(result_df, ignore_index=True)
            else:
                return pd.DataFrame()
        chunks = np.array_split(query_df, total_threads) if len(query_df) > 2 else [query_df]

        for chunk in chunks:
            future = executor.submit(process_chunk, chunk)
            futures.append(future)

        results = []
        for future in as_completed(futures):
            results.append(future.result())

    # Return the concatenated results as a single DataFrame
    return pd.concat(results, ignore_index=True)
