import math
import string

def get_alphabet_position_vertical(index: int, MAX_ROWS = 8):
    """
    index: 1-based indexing
    MAX_ROWS: number of rows
    return: 
        8x12: A1-H12 (96)
        10x10: A1-J10 (100)

        Vertical: 
            A1  A2  A3  A4        A12
            B1  B2  B3  B4        B12
            C1  C2  C3  C4        C12
            ..  ..  ..  ..        ..
            H1  H2  H3  H4   .... H12
            ..  ..  ..  ..
            (J1)(J2)(J3)(J4) .... 
    """


    # alphabet_idx = index%8 - 1
    alphabet_idx = ( index%MAX_ROWS if index%MAX_ROWS > 0 else MAX_ROWS ) - 1
    pos_prefix = list(string.ascii_uppercase)[alphabet_idx]
    pos_suffix = math.ceil(index/MAX_ROWS)
    return pos_prefix + str(pos_suffix), alphabet_idx

# 100
for i in range(1,101,1):
  res, alphabet_idx = get_alphabet_position_vertical(i,10)
  print(res,' ',alphabet_idx)

# 96
# for i in range(1,97,1):
#   res, alphabet_idx = get_alphabet_position_vertical(i,8)
#   print(res,' ',alphabet_idx)