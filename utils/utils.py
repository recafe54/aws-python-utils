import re

def split_text_n_number(data):
    match = re.match(r"([a-z]|[A-Z]+)([0-9]+)", data, re.I)
    if match:
        items = match.groups()
        text = items[0]
        num = items[1] 
        return text, num
    else:
        return None, None
    
data = "A2"

row, col = split_text_n_number(data=data)
print(f"row {row} col {col}")

def calculate_weight_of_well_position(well_position):
    row, col = split_text_n_number(well_position)
    return ord(row) + int(col)*10

weight = calculate_weight_of_well_position(data)
print(f"well_position {data} - weight {weight} ")

list_pos = ["A1","B1","C1","D1","E1","F1","G1","H1","A2","B2","C2","D2","E2","F2","G2","H2","A3","B3","C3","D3","E3","F3","G3","H3"]
list_pos_2 = ["A1","A2","B1","B2","C1","D1","E1","F1","G1","H1"]
list_weight = [ calculate_weight_of_well_position(pos) for pos in list_pos_2]
indices = sorted(
    range(len(list_weight)),
    key=lambda index: list_weight[index]
)
print(sorted(list_weight))
print(indices)