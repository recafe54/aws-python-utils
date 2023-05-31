import os
import boto3
from pathlib import Path
from utils.utils import Logger
import tarfile
from botocore.exceptions import ClientError
import logging
from datetime import datetime

logger = Logger()
FILE_SYSTEM_PATH = Path("/app")

"""Environment Variables

:param INPUT_DATA_BUCKET: Input Source where input downloaded from
:param BATCH_ID: Name of specific folder in the Input Source (also Identity used for Batch Input)
:param OUTPUT_DATA_BUCKET: Output Source where output uploaded to
:return: 
"""


def download_s3_bucket(bucket_name, batch_name, file_system_path):
    s3_resource =  boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    # Prefix for specific directory
    for obj in bucket.objects.filter(Prefix=batch_name):
        key = obj.key
        if not key.endswith("/"):
            dir_name = os.path.dirname(key)
            if batch_name not in dir_name: 
                destination_dir = os.path.join(file_system_path, batch_name, dir_name)
                destination = os.path.join(file_system_path, batch_name, key)
            else:
                destination_dir = os.path.join(file_system_path, dir_name)
                destination = os.path.join(file_system_path, key)
                
            Path(destination_dir).mkdir(parents=True, exist_ok=True)
            bucket.download_file(key, destination)
            input_file_name = os.path.basename(key)
            if input_file_name.startswith('PCR'):
                os.environ['INPUT_FILE'] = os.path.join('/app',os.environ['BATCH_ID'],os.path.basename(input_file_name))
                logger.info("INPUT FILE: {}".format(os.environ['INPUT_FILE']))
            if key.endswith(".tar.xz") or key.endswith(".tar.gz"):
                file_name = os.path.join(destination_dir, os.path.basename(key))
                f = tarfile.open(file_name)
                f.extractall(destination_dir)
                print('file_name :',file_name)
                f.close()

def preprocessing():
    logger.info("Start preprocessing process")
    pcr_data_bucket = os.environ["INPUT_DATA_BUCKET"]
    batch_name = os.environ["BATCH_ID"]
    logger.info("Downloading pcr input data into mount path: app/{}".format(batch_name))
    download_s3_bucket(pcr_data_bucket, batch_name, FILE_SYSTEM_PATH)
    logger.info("Done preprocessing process")

def upload_file(s3_client,prefix,file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket,prefix+'/'+object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def postprocessing(folder_path):
    # Get a list of all files in the folder
    s3_client = boto3.client('s3')
    files = os.listdir(folder_path)
    prefix = os.environ["BATCH_ID"]
    bucket = os.environ["OUTPUT_DATA_BUCKET"]
    # Print the file names
    for name in files:
        obj_path = os.path.join(folder_path,name)
        upload_file(s3_client,prefix,obj_path,bucket)
        logger.info("Obj_path: {}".format(obj_path))
    pass

if __name__ == "__main__":
    # DOWNLOAD FROM INPUT SOURCE
    preprocessing()
    INPUT_FILE = os.environ['INPUT_FILE']
    BARCODE_MAPPING_FILE = os.path.join('/app',os.environ['BATCH_ID'],os.path.basename(os.environ['BARCODE_MAPPING_FILE']))

    # ----
    RESULT_PATH = os.path.join('results', datetime.now().strftime('%Y%m%d'))
    # PROCESSING INPUT HERE --> OUTPUT TO LOCAL PATH (e.g: RESULT_PATH)
    # ---
    
    # UPLOAD TO OUTPUT SOURCE
    postprocessing(RESULT_PATH)
    pass