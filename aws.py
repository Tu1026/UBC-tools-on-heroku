from dotenv import load_dotenv
import os



def upload_file(s3, file_name):
    load_dotenv()
    bucket = os.environ.get('AWS_BUCKET_NAME')
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    response = s3.upload_file(file_name, bucket, object_name)
    return response


# def download_file(file_name):
#     s3 = initiation()
#     bucket = os.environ.get('AWS_BUCKET_NAME')
#     """
#     Function to download a given file from an S3 bucket
#     """
#     # s3 = boto3.resource('s3')
#     file = s3.get_object(Bucker=bucket, key='extraction.zip')
#     output = f"downloads/{file_name}"
#     s3.Bucket(bucket).download_file(file_name, output)

#     # return output
#     return Response(
#         file['Body'].read(),
#         mimetype='text/plain',
#         headers={"Content-Disposition": "attachment;filename=course.zip"}
#     )



def list_files(s3):
    load_dotenv()
    bucket = os.environ.get('AWS_BUCKET_NAME')
    """
    Function to list files in a given S3 bucket
    """
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents
    



def get_total_bytes(s3):
    load_dotenv()
    result = s3.list_objects(Bucket=os.environ.get('AWS_BUCKET_NAME'))
    for item in result['Contents']:
        if item['Key'] == 'extraction.zip':
            return item['Size']


def get_object(s3, total_bytes):
    load_dotenv()
    if total_bytes > 1000000:
        return get_object_range(s3, total_bytes)
    return s3.get_object(Bucket= os.environ.get('AWS_BUCKET_NAME'), Key='extraction.zip')['Body'].read()


def get_object_range(s3, total_bytes):
    load_dotenv()
    offset = 0
    while total_bytes > 0:
        end = offset + 999999 if total_bytes > 1000000 else ""
        total_bytes -= 1000000
        byte_range = 'bytes={offset}-{end}'.format(offset=offset, end=end)
        offset = end + 1 if not isinstance(end, str) else None
        yield s3.get_object(Bucket= os.environ.get('AWS_BUCKET_NAME'), Key='extraction.zip', Range=byte_range)['Body'].read()

