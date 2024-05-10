"""
Created on Tues 11/1/2023
@comments: 
1. Replace “\n” with "" to account for any new lines 
2. Replace empty spaces " " with ""
3. Replace all non-IUPAC characters with n 
"""

import re
def replacing_multistate_characters_with_n(seq_unc):

    #---------
    seq_unc = seq_unc.lower().replace('\n', '').replace(' ', '')
    # replace non-IUPAC/non-hyphen characters with n
    cleaned_seq_unc = re.sub(r'[^acgtmrwsykvhdb]', 'n', seq_unc)
    seq_unc_temp = cleaned_seq_unc   
    #---------

    # Replace all IUPAC plus n with x
    seq_copy = re.sub(r"[ryswkmbdhvn]", "x", cleaned_seq_unc)  
    matches = list(re.finditer(r"x+", seq_copy))

    pos_list = []
    remove_vector = []
   

    for match in matches:
        start, end = match.span()
        length = end - start 
        pos_list.append((start, end-1, length))
        

    if len(pos_list) != 0:
        max_index = len(pos_list)
        pen = max_index - 1

        if max_index == 1:
            if pos_list[0][2] > 2:
                seq_unc_temp = seq_unc_temp[: pos_list[0][0]] + "n" * pos_list[0][2] + seq_unc_temp[pos_list[0][1] + 1 :]
            else:
                remove_vector.append(0)
        else:
            for j in range(max_index):
                if j == max_index - 1:
                    if pos_list[j][2] < 3 and pos_list[j][0] - pos_list[j - 1][1] > 3:
                        remove_vector.append(j)
                    elif max_index == 2 and pos_list[j][2] < 3:
                        remove_vector.append(j)
                    elif pos_list[j - 1][0] - pos_list[j - 2][1] > 3 and pos_list[j][2] < 3 and pos_list[j - 1][2] < 3:
                        remove_vector.append(j)
                elif j == pen:
                    if (pos_list[j + 1][0] - pos_list[j][1]) > 3 and pos_list[j][2] < 3:
                        remove_vector.append(j)
                    elif (
                        (pos_list[j + 1][0] - pos_list[j][1]) <= 3
                        and pos_list[j][2] < 3
                        and pos_list[j + 1][2] < 3
                    ):
                        if j == 0:
                            remove_vector.append(j)
                    elif (
                        (pos_list[j][0] - pos_list[j - 1][1]) > 3
                        and pos_list[j][2] < 3
                    ):
                        remove_vector.append(j)
                else:
                    if j == 0:
                        if (pos_list[j + 1][0] - pos_list[j][1]) > 3 and pos_list[j][2] < 3:
                            remove_vector.append(j)
                        elif (
                            (pos_list[j + 1][0] - pos_list[j][1]) <= 3
                            and pos_list[j][2] < 3
                        ):
                            if max_index >= 3 and (pos_list[j + 2][0] - pos_list[j + 1][1]) > 3:
                                remove_vector.append(j)
                            elif (
                                max_index >= 3
                                and pos_list[j + 2][0] - pos_list[j + 1][1] <= 3
                                and pos_list[j + 2][2] < 3
                                and pos_list[j + 1][2] < 3
                                and pos_list[j][2] < 3
                            ):
                                remove_vector.append(j)
                    elif j == 1:
                        if (pos_list[j + 1][0] - pos_list[j][1]) > 3 and pos_list[j][2] < 3:
                            if (pos_list[j][0] - pos_list[j - 1][1]) > 3:
                                remove_vector.append(j)
                            elif (
                                (pos_list[j][0] - pos_list[j - 1][1]) <= 3
                                and pos_list[j - 1][2] < 3
                            ):
                                remove_vector.append(j)
                        elif (
                            (pos_list[j + 1][0] - pos_list[j][1]) <= 3
                            and pos_list[j][2] < 3
                        ):
                            if (
                                (pos_list[j][0] - pos_list[j - 1][1]) > 3
                                and pos_list[j + 1][2] < 3
                                and pos_list[j][2] < 3
                            ):
                                remove_vector.append(j)
                            elif (
                                (pos_list[j][0] - pos_list[j - 1][1]) <= 3
                                and pos_list[j + 1][2] < 3
                            ):
                                if (
                                    pos_list[j + 1][2] < 3
                                    and pos_list[j][2] < 3
                                    and pos_list[j - 1][2] < 3
                                ):
                                    remove_vector.append(j)
                    else:
                        if (pos_list[j + 1][0] - pos_list[j][1]) > 3 and pos_list[j][2] < 3:
                            if (pos_list[j][0] - pos_list[j - 1][1]) > 3:
                                remove_vector.append(j)
                            elif (
                                (pos_list[j][0] - pos_list[j - 1][1]) <= 3
                                and pos_list[j][2] < 3
                                and pos_list[j - 1][2] < 3
                            ):
                                if (
                                    max_index >= 3
                                    and (pos_list[j - 1][0] - pos_list[j - 2][1]) > 3
                                ):
                                    remove_vector.append(j)
                                elif (
                                    max_index >= 3
                                    and (pos_list[j - 1][0] - pos_list[j - 2][1]) <= 3
                                    and pos_list[j - 2][2] < 3
                                    and pos_list[j - 1][2] < 3
                                    and pos_list[j][2] < 3
                                ):
                                    remove_vector.append(j)
                            elif (
                                (pos_list[j][0] - pos_list[j - 1][1]) <= 3
                                and pos_list[j + 1][2] < 3
                                and pos_list[j][2] < 3
                                and pos_list[j - 1][2] < 3
                            ):
                                remove_vector.append(j)
        if remove_vector:
            # Calculate the new max_index after removing elements
            pos_list = [ele for idx, ele in enumerate(pos_list) if idx not in remove_vector]
        if pos_list:
            max_index = len(pos_list)
            for j in range(max_index):
                if pos_list[j][2] >= 1:
                    seq_unc_temp = (
                        seq_unc_temp[: pos_list[j][0]]
                        + "n" * pos_list[j][2]
                        + seq_unc_temp[pos_list[j][1] + 1 :]
                    )
                if j != max_index - 1 and max_index != 1:
                    if pos_list[j + 1][0] - pos_list[j][1] <= 4:
                        seq_unc_temp = (
                            seq_unc_temp[: pos_list[j][1] + 1]
                            + "n" * (pos_list[j + 1][0] - pos_list[j][1] - 1)
                            + seq_unc_temp[pos_list[j + 1][0] :]
                        )
    seq_copy_final = seq_unc_temp

    return seq_copy_final 