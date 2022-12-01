import boto3
import os

# fetch credentials from env variables
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

# setup a AWS S3 client/resource
s3 = boto3.resource(
    's3', 
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    )
s3_client = boto3.client(
    's3', 
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    )

# point the resource at the existing bucket
bucket = s3.Bucket('anyoneai-datasets')


def list_s3_files_using_resource():
    """
    This functions list files from s3 bucket using s3 resource object.
    :return: None
    """

    # s3 = boto3.resource(
    # 's3', 
    # aws_access_key_id=aws_access_key_id,
    # aws_secret_access_key=aws_secret_access_key,
    # )
    s3 = boto3.resource(
    's3', 
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    )

    s3_bucket = s3.Bucket("anyoneai-datasets")
    files = s3_bucket.objects.all()
    for file in files:
        print(file)

# list_s3_files_in_folder_using_client()
def list_s3_files_in_folder_using_client():
    """
    This function will list down all files in a folder from S3 bucket
    :return: None
    """
    s3_client = boto3.client("s3", 
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    )
    bucket_name = "anyoneai-datasets"
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix="SKU-110K/SKU110K_fixed/")
    files = response.get("Contents")
    for file in files:
        print(f"file_name: {file['Key']}, size: {file['Size']}")

def download_dir(prefix, local, bucket, client=s3_client):
    """
    params:
    - prefix: pattern to match in s3
    - local: local path to folder in which to place files
    - bucket: s3 bucket with target contents
    - client: initialized s3 client object
    """
    keys = []
    dirs = []
    next_token = ''
    base_kwargs = {
        'Bucket':bucket,
        'Prefix':prefix,
    }
    while next_token is not None:
        kwargs = base_kwargs.copy()
        if next_token != '':
            kwargs.update({'ContinuationToken': next_token})
        results = client.list_objects_v2(**kwargs)
        contents = results.get('Contents')
        for i in contents:
            k = i.get('Key')
            print(k)
            print(k.split('/')[1:])
            
            if k[-1] != '/':
                keys.append(k)
            else:
                dirs.append(k)
        next_token = results.get('NextContinuationToken')
    print(dirs)
    for d in dirs:
        dest_pathname = os.path.join(local, d.split('/')[1:])
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
    for k in keys:
        dest_pathname = os.path.join(local, *k.split('/')[1:])
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
        client.download_file(bucket, k, dest_pathname)


download_dir("SKU-110K/SKU110K_fixed/", "/home/app/src/data", "anyoneai-datasets",s3_client)
