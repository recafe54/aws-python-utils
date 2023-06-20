import json
import os
import boto3
import zipfile
from io import BytesIO
import requests

# 2048 GB
# Timeout 2 mins
os.environ['OPERATION_SERVICE_URL'] =  "http://0.0.0.0:8000" # "http://0.0.0.0:8000" # "http://internal-qa.genestory.ai/operation"
os.environ['NOTIFICATION_SQS_QUEUE'] = "gx-notification-qa"
os.environ['SENDER_ID'] = "444c44cd-4444-4d44-b4f4-44fd444b4ad4" # Edited


def post_processing(chip_id):
    # CHECK & UPDATE TIMELINE
    batch_number = return_batch_number_given_chip_id(chip_id)
    print(f"batch number: {batch_number}")
    is_uploaded_whole_batch = check_sum_n_update_uploaded_date(batch_number)
    print(f"is_uploaded_whole_batch: {is_uploaded_whole_batch}")
    title = create_appropriate_title(batch_number, chip_id)
    content = ""
    print(f"title: {title} && content: {content}")
    
    # SEND NOTIFICATION
    if is_uploaded_whole_batch:
        # SEND SUCCESS NOTIFICATION
        content = f"All chips in BATCH {batch_number} is ready to run drylab"
        MessageBody = get_notification_body(title, content)
        print('MESSAGE BODY: ', MessageBody)
        send_notification(MessageBody)
    else:
        content = f"All chips in BATCH {batch_number} raw data is not ready to run drylab"
        MessageBody = get_notification_body(title, content)
        print('MESSAGE BODY: ', MessageBody)
        send_notification(MessageBody)
    #     # SEND FAILURE NOTIFICATION
    pass

def return_batch_number_given_chip_id(chip_id):
    headers={"Content-Type": "application/json"}
    params = {
        "chip_id": f"{chip_id}",
        "export": "true"
    }
    operation_service_url = os.environ['OPERATION_SERVICE_URL']
    res = requests.get(f"{operation_service_url}/available", params=params, headers=headers) # Edited
    print("res: ",res)
    batch_number = res.json()['data'][0]['batch_barcode']
    return batch_number

def check_sum_n_update_uploaded_date(batch_number):
    try:
        
        headers={"Content-Type": "application/json"}
        json={"raw_data_uploaded_date": "2023-06-20"}
        operation_service_url = os.environ['OPERATION_SERVICE_URL']
        validate_res = requests.put(f"{operation_service_url}/raw/microarray/{batch_number}", json=json, headers=headers) # Edited
        print('validate_res: ',validate_res)
        print('validate_res: ',validate_res.json())
        if validate_res.status_code == 400:
            print(f"check response {validate_res.json()['detail'][0]['msg']}")
            return False
        return True
    except Exception as err:
        print('RAW DATA NOT READY!!: ',str(err))
        return False
        pass

def create_appropriate_title( batch_number, chip_id):
    return f"RAW DATA for BATCH {batch_number} - chip {chip_id} is READY!!"
    pass


def get_notification_body(title, content):
    sender_id = os.environ['SENDER_ID']
    message_req = {
        "METHOD": "POST",
        "ACTION": "SEND_NOTIFICATION_TO_GROUP",
        "BODY": { "group_id":"lims", "sender_id":sender_id, "title": title ,"content": content} ,
    }
    
    MessageBody=json.dumps(message_req)
    
    return MessageBody

def send_notification(MessageBody):
    sqs_client = boto3.client('sqs',region_name='ap-southeast-1')
    queue = sqs_client.get_queue_url(QueueName=os.environ['NOTIFICATION_SQS_QUEUE'])
    queue_url = queue['QueueUrl']
    res = sqs_client.send_message(QueueUrl=queue_url, MessageBody=MessageBody)
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"Successfully send notification to user group: lims")
    else:
        print(f"Cannot send notification to user group: lims")
    pass

def main():
    CHIP_ID = "12333"
    post_processing(CHIP_ID)
    pass

if __name__ == "__main__":
    main()