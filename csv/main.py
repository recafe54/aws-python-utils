import csv

def export_list_dicts_to_csv(results, file_path):
    field_names = ['LabID','Barcode']

    with open(file_path, 'w', newline= '') as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

        for data_dict in results:
            writer.writerow(data_dict)

            pass
    pass