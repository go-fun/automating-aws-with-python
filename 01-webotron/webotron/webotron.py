import boto3
import click
import mimetypes
from botocore.exceptions import ClientError
from pathlib import Path

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.group()
def cli():
    "Webotron deploys websites to AWS"
    pass

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    "List objects in an s3 bucket"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)

@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    "Create and configure S3 bucket"
    s3_bucket = s3.create_bucket(Bucket=bucket)

    policy="""{
      "Version":"2012-10-17",
      "Statement":[{
      "Sid":"PublicReadGetObject",
      "Effect":"Allow",
      "Principal": "*",
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::%s/*"
          ]
        }
      ]
    }""" % s3_bucket.name

    pol = s3_bucket.Policy()
    pol.put(Policy=policy)

    ws = s3_bucket.Website()
    ws.put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
    })

    s3_bucket.upload_file('index.html', 'index.html', ExtraArgs={'ContentType': 'text/html'})
    return

def upload_file(s3_bucket, path, key):
    ContentType = mimetypes.guess_type(key)[0] or 'text/plain'
    s3_bucket.upload_file(
        path,
        key,
        ExtraArgs={
            'ContentType': 'text/html'
        }
    )

@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    "sync contents of Pathname to Bucket"
    s3_bucket = s3.Bucket(bucket)

    root = Path(pathname).expanduser().resolve()

    def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir(): handle_directory(p)
                if p.is_file(): upload_file(s3_bucket, str(p), str(p.relative_to(root)))

    handle_directory(root)

if __name__ == '__main__':
     cli()


# troubleshoot in ipython
# from botocore.exception import ClientError
# try:
# the python code to test
# except ClientError as e:
#    print(e.response)
