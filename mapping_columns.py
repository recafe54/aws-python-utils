import pandas as pd
import requests
import json
# Read the Excel file
df = pd.read_excel('kit-list-swap.xlsx')

# Convert each row of the DataFrame into a dictionary
data = df.to_dict(orient='records')

rows = []
# Print each dictionary representing a row
for row in data:
    # print(row)
    rows.append(row)


file_path = 'response.json'
with open(file_path, 'r') as json_file:
    # Read the file content
    list_of_dicts = json.load(json_file)

print('list_of_dicts: ',type(list_of_dicts))
# Print the list of dictionaries
mapping_barcode_n_lid = []
for dictionary in list_of_dicts["data"]:
    for row in rows:
        temp_barcode = str(row['Barcode cũ']) if len(str(row['Barcode cũ'])) >= 12 else '0'+str(row['Barcode cũ'])
        if temp_barcode == str(dictionary['barcode']):
            entry = dict()
            entry['old_barcode']=dictionary['barcode']
            entry['lid']=dictionary['lid']
            entry['new_barcode']=str(row['Barcode mới'])
            mapping_barcode_n_lid.append(entry)
            # print(entry)
            query = print(f"UPDATE lab_sample SET barcode='{entry['new_barcode']}' WHERE lid='{entry['lid']}'; ")
            # uPDATE lab_sample SET barcode='xxxx' WHERE lid='aaaa'; 
    


