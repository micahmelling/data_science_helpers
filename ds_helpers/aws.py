import boto3
import json
import os
import botocore

from botocore.exceptions import ClientError


def get_secrets_manager_secret(secret_name, region='us-west-2'):
    """
    Retrieves a secret from AWS Secrets Manager, a password manager.

    :param secret_name: name of the secret
    :type secret_name: str
    :param region: name of the AWS region; default is us-west-2
    :type region: str
    :return: dictionary with the secret keys and values
    """
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )
    secret_value_response = client.get_secret_value(SecretId=secret_name)
    for key, value in secret_value_response.items():
        if key == 'SecretString':
            return json.loads(value)


def set_aws_environment_variables(secret_name):
    keys_secret = get_secrets_manager_secret(secret_name)
    os.environ['AWS_ACCESS_KEY_ID'] = keys_secret.get('access_key')
    os.environ['AWS_SECRET_ACCESS_KEY'] = keys_secret.get('secret_key')


def upload_file_to_s3(file_name, bucket, directory=''):
    """
    Uploads a local file to S3, in the specified bucket and directory.

    :param file_name: the name of the local file; this will also be the file name in S3
    :type file_name: str
    :param bucket: name of the bucket to upload the file to; the bucket will be created if it does not exist
    :type bucket: str
    :param directory: the name of the directory in which to put the file; default is root
    :type directory: str
    """
    s3_client = boto3.client('s3')
    s3_client.upload_file(file_name, bucket, os.path.join(directory, file_name))


def upload_directory_to_s3(local_directory, bucket):
    """
    Uploads an entire directory to S3.

    :param local_directory: name of the local directory
    :type local_directory: str
    :param bucket: name of the S3 bucket
    :type bucket: str
    """
    directory_walk = os.walk(local_directory)
    for directory_path, directory_name, file_names in directory_walk:
        if directory_path != os.path.join(local_directory):
            sub_dir = os.path.basename(directory_path)
            for file in file_names:
                upload_file_to_s3(file_name=os.path.join(local_directory, sub_dir, file), bucket=bucket)
        else:
            for file in tqdm(file_names):
                upload_file_to_s3(file_name=os.path.join(local_directory, file), bucket=bucket)


def download_file_from_s3(file_name, bucket, directory=''):
    """
    Downloads a single specified file from S3. If the file is in a directory in S3, the file will be placed in a
    directory of the same name locally.

    :param file_name: the name of the file to download; this will also be the name of the file locally
    :type file_name: str
    :param bucket: the name of the bucket where the file exists
    :type bucket: str
    :param directory: the name of the directory where the file exists; the directory will be created locally if it does
    not exist
    :type directory: str
    :return: None
    """
    s3 = boto3.resource('s3')
    try:
        if not os.path.exists(directory) and directory != '':
            os.makedirs(directory)
        s3.Bucket(bucket).download_file(os.path.join(directory, file_name), os.path.join(directory, file_name))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


def download_directory_from_s3(bucket, directory):
    """
    Downloads a folder in S3 and all of its contents into a local directory.

    :param bucket: name of the bucket in S3 where the directory lives
    :type bucket: str
    :param directory: directory in S3 we want to download
    :type directory: str
    """
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket)
    for object in bucket.objects.filter(Prefix=directory):
        if not os.path.exists(os.path.dirname(object.key)):
            os.makedirs(os.path.dirname(object.key))
        bucket.download_file(object.key, object.key)
