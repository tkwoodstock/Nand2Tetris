
import math
import pandas as pd
from tabulate import tabulate


def to_binary(num, first_iteration = True, to_16 = False):

    num = int(num)

    # end recursive function and add number to final 1's column
    if num in [0,1]:
        if not first_iteration:
            return str(num)
        else:
            return "000000000000000" + str(num)
    

    # if not ended, num is at least 2, so add a 1 to start of string
    binary_string = "1"

    # find log2 of the current number, this is the column where the "1" above is placed
    base = math.floor(math.log2(num))

    # find left over to allocate to other columns
    remainder = num - 2**base

    # if no remainder, all the remaining numbers are set to 0
    if remainder == 0:
        rem_base = 0
    # if a remainder, log2 of this is the column where the next 1 is placed
    else:
        rem_base = math.floor(math.log2(remainder))

    # fill string with zeros until the position of the next 1, calculated above in rem_base
    add_zeros = base - rem_base - 1
    for i in range(add_zeros):
        binary_string += "0"

    # recursion, append result to current string
    binary_string += to_binary(remainder, first_iteration=False)

    if to_16:
        # pad with zeros so instruction length is 16
        zero_padding = 16 - len(binary_string)
        for zero in range(zero_padding):
            binary_string = "0" + binary_string


    # return all appended strings of 1 and 0 combinations
    return binary_string



## test functionality:

if __name__ == "__main__":
    results = [["decimal", "from my_func", "from python default"]]
    for i in [21, 9, 31, 2, 0, 1, 35, 65, 88, 124, 155, 5732, 19999]:
        results.append([i, to_binary(i), bin(i)[2:]])


    df_results = pd.DataFrame(data=results[1:], columns=results[0])


    print(tabulate(df_results, headers='keys', tablefmt='psql'))