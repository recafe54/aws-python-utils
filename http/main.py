import json
import os
import boto3
import zipfile
from io import BytesIO
import requests
os.environ['OPERATION_SERVICE_URL'] = 'http://internal-qa.genestory.ai/operation'

def return_batch_number_given_chip_id(chip_id):
    headers={"Content-Type": "application/json"}
    params = {
        "chip_id": f"{chip_id}"
    }
    operation_service_url = os.environ['OPERATION_SERVICE_URL']
    res = requests.get(f"{operation_service_url}/lims/sample_management/available", params=params, headers=headers)
    batch_number = res.json()['data'][0]['batch_barcode']
    return batch_number
    pass

def main():
    chip_id = '12333'
    res = return_batch_number_given_chip_id(chip_id=chip_id)
    print("Response: ", res)
    pass

if __name__ == "__main__":
    main()
    pass