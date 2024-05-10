# Dependences:
from scipy.stats import fisher_exact

MUT_PROBS = {'a': 1, 'r': 1/2, 'm': 1/2, 'w': 1/2, 'h': 1/3, 'v': 1/3, 'd': 1/3, 'n': 1/4}

def hypermut_pattern_finder(query_seq, ref_seq, mut_probs):
    
    """
    Find hypermutation patterns and calculate mutation probabilities.
    Args:
        query_seq (str): The query sequence.
        ref_seq (str): The reference sequence.
        mut_probs (dict): Dictionary of mutation probabilities.
    Returns:
        tuple: A tuple containing the sum of mutation probabilities and the count of mutations.
    """
    
    if len(ref_seq) != len(query_seq):
        return "query_seq and ref_seq must have the same length."
    
    aRD_to_g_mut_prob_list = []
    r = ['g', 'a']
    d = ['g', 'a', 't']
    
    i = 0
    while i < len(query_seq):
        if query_seq[i] in mut_probs:
            aPos = i
            i += 1
            while i < len(query_seq) and query_seq[i] == '-':
                i += 1
            if i < len(query_seq) and query_seq[i] in r:
                i += 1
                while i < len(query_seq) and query_seq[i] == '-':
                    i += 1
                if i < len(query_seq) and query_seq[i] in d:
                    if ref_seq[aPos] == 'g':
                        mut_prob = mut_probs[query_seq[aPos]]
                        aRD_to_g_mut_prob_list.append(round(mut_prob, 2))
                    else:
                        aRD_to_g_mut_prob_list.append(0)
        i += 1

    aRD_to_g_mut_prob = [x for x in aRD_to_g_mut_prob_list if x != 0]
    aRD_to_g_mut_prob_sum = sum(aRD_to_g_mut_prob)
    aRD_to_g_count = len(aRD_to_g_mut_prob)

    return aRD_to_g_mut_prob_sum, aRD_to_g_count

def control_pattern_finder(query_seq, ref_seq, mut_probs):
    
    """
    Find control patterns and calculate mutation probabilities.
    Args:
        query_seq (str): The query sequence.
        ref_seq (str): The reference sequence.
        mut_probs (dict): Dictionary of mutation probabilities.
    Returns:
        tuple: A tuple containing the sum of mutation probabilities and the count of mutations.
    """
    
    if len(ref_seq) != len(query_seq):
        return "query_seq and ref_seq must have the same length."

    aYNRC_to_g_mut_prob_list = []
    y = ['t', 'c']
    n = ['g', 'a', 't', 'c']
    r = ['g', 'a']
    
    i = 0
    while i < len(query_seq):
        if query_seq[i] in mut_probs:
            aPos = i
            i += 1
            while i < len(query_seq) and query_seq[i] == '-':
                i += 1
            if i < len(query_seq) and query_seq[i] in y:
                i += 1
                while i < len(query_seq) and query_seq[i] == '-':
                    i += 1
                if i < len(query_seq) and query_seq[i] in n:
                    if ref_seq[aPos] == 'g':
                        mut_prob = mut_probs[query_seq[aPos]]
                        aYNRC_to_g_mut_prob_list.append(round(mut_prob, 2))
                    else:
                        aYNRC_to_g_mut_prob_list.append(0)
            elif i < len(query_seq) and query_seq[i] in r:
                i += 1
                while i < len(query_seq) and query_seq[i] == '-':
                    i += 1
                if i < len(query_seq) and query_seq[i] == 'c':
                    if ref_seq[aPos] == 'g':
                        mut_prob = mut_probs[query_seq[aPos]]
                        aYNRC_to_g_mut_prob_list.append(round(mut_prob, 2))
                    else:
                        aYNRC_to_g_mut_prob_list.append(0)
        i += 1

    aYNRC_to_g_mut_prob = [x for x in aYNRC_to_g_mut_prob_list if x != 0]
    aYNRC_to_g_mut_prob_sum = sum(aYNRC_to_g_mut_prob)
    aYNRC_to_g_count = len(aYNRC_to_g_mut_prob)
    
    return aYNRC_to_g_mut_prob_sum, aYNRC_to_g_count

def analyze_mutations(query_seq, ref_seq):
    
    """
    Analyze mutations in query sequence compared to reference sequence.
    Args:
        query_seq (str): The query sequence.
        ref_seq (str): The reference sequence.
    Returns:
        tuple: A tuple containing the rate ratio and p-value.
    """
    
    # Call hypermut_pattern_finder
    result_aRD = hypermut_pattern_finder(query_seq, ref_seq, MUT_PROBS)
    if isinstance(result_aRD, str):
        return "Error in hypermut_pattern_finder: " + result_aRD

    aRD_to_g_mut_prob_sum, aRD_to_g_count = result_aRD

    # Call control_pattern_finder
    result_aYNRC = control_pattern_finder(query_seq, ref_seq, MUT_PROBS)
    if isinstance(result_aYNRC, str):
        return "Error in control_pattern_finder: " + result_aYNRC

    aYNRC_to_g_mut_prob_sum, aYNRC_to_g_count = result_aYNRC

    # Perform Fisher's exact test
    contingency_table = [[aRD_to_g_mut_prob_sum, aRD_to_g_count - aRD_to_g_mut_prob_sum],
                         [aYNRC_to_g_mut_prob_sum, aYNRC_to_g_count - aYNRC_to_g_mut_prob_sum]]
    _, p_value = fisher_exact(contingency_table, alternative='greater')
    p_value_rounded = float("{:.5e}".format(p_value))
    
    # return rate_ratio, p_value_rounded
    return p_value_rounded
