import boto3
import json 

StateMachine = ''
pxStateMachine = ''

def get_step_function_client():
    ACCESS_KEY = ""
    AWS_SECRET_ACCESS_KEY = ""
    stf_client = boto3.client('stepfunctions', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name="ap-southeast-1")
    return stf_client

def list_execution_function(stateMachineArn):
    stf_client = get_step_function_client()
    response = stf_client.list_executions(
            stateMachineArn=stateMachineArn,
            maxResults=100
            )

    list_of_executions = []
    for execution in response['executions']:
        executionArn = execution['executionArn']
        execution = stf_client.describe_execution(executionArn=executionArn)
        list_of_executions.append(execution)
    return list_of_executions


def get_chip_ids():
    return []

def get_execution_status_w_microarray(list_of_executions, chip_ids):
    results = []
    for exec in list_of_executions:
        input = json.loads(exec['input'])
        if input['chip_id'] in chip_ids and exec["status"] != 'ABORTED':
            entry = {
                'chip_id': input['chip_id'],
                'batch_barcode': input['batch_barcode'],
                'startDate': exec['startDate'],
                'status': exec["status"]
            }
            results.append(entry)
            chip_ids.remove(input['chip_id'])
    return results

def get_execution_status_w_pcr(list_of_executions, batch_id):
    result = []
    for exec in list_of_executions:
        input = json.loads(exec['input'])
        if input['batch_id'] == batch_id and exec["status"] != 'ABORTED':
            result = {
                'batch_id': input['batch_id'],
                'startDate': exec['startDate'],
                'status': exec["status"]
            }
            break
    return result

def get_dry_lab_execution_status_for_microarray_batch():
    list_of_executions = list_execution_function(StateMachine)
    chip_ids = get_chip_ids()
    results = get_execution_status_w_microarray(list_of_executions, chip_ids)
    for res in results:
        print(f"CHIP_ID: {res['chip_id']} && STATUS {res['status']}")
    return results

def get_dry_lab_execution_status_for_pcr_batch(batch_id):
    list_of_executions = list_execution_function(pxStateMachine)
    result = get_execution_status_w_pcr(list_of_executions, batch_id)
    print(f"BATCH_NUMBER: {result['batch_id']} && STATUS {result['status']}")
    return result

def main():
    technology = 'PCR'
    batch_id = '5'
    if technology == 'MICROARRAY':
        results = get_dry_lab_execution_status_for_microarray_batch()
    if technology == 'PCR':
        results = get_dry_lab_execution_status_for_pcr_batch(batch_id)

if __name__ == "__main__":
    main()
