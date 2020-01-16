import logging
import boto3
import os
import botocore
from botocore.exceptions import ClientError


def create_bucket_if_not_exists(bucket):
    """
    Creates and S3 bucket if it does not already exists.
    :param bucket: name of S3 bucket
    :type bucket: str
    :return: None
    """
    s3 = boto3.resource('s3')
    exists = s3.Bucket(bucket) in s3.buckets.all()
    if not exists:
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={
            'LocationConstraint': 'us-west-2'})


def upload_file_to_s3(file_name, bucket, directory=''):
    """
    Uploads a local file to S3, in the specified bucket and directory.
    :param file_name: the name of the local file; this will also be the file name in S3
    :type file_name: str
    :param bucket: name of the bucket to upload the file to; the bucket will be created if it does not exist
    :type bucket: str
    :param directory: the name of the directory in which to put the file; default is root
    :type directory: str
    :return: None
    """
    create_bucket_if_not_exists(bucket)
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, os.path.join(directory, file_name))
    except ClientError as e:
        logging.error(e)
        return False
    return True


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


def download_folder_from_s3(bucket, directory):
    """
    Downloads a folder in S3 and all of its contents into a local directory.
    :param bucket: name of the bucket in S3 where the directory lives
    :type bucket: str
    :param directory: directory in S3 we want to download
    :type directory: str
    :return: None
    """
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket)
    for object in bucket.objects.filter(Prefix=directory):
        if not os.path.exists(os.path.dirname(object.key)):
            os.makedirs(os.path.dirname(object.key))
        bucket.download_file(object.key, object.key)


# if __name__ == "__main__":
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    # aws key and secret in bash_profile

    # file = open("sample.txt", "w")
    # file.write("testing...testing...testing")
    # file.close()

    # upload_file_to_s3('sample.txt', 'full-stack-data-science', 'data-science-files2')
    # download_file_from_s3('sample.txt', 'full-stack-data-science')
    # download_folder_from_s3('full-stack-data-science', 'data-science-files2')

