import boto3
import os

srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]
datapath = os.path.join(srcpath, 'data/')
rawpath = os.path.join(datapath, 'raw/')

boto3_connection = boto3.resource('s3')
s3_client = boto3.client('s3')


def download_raw_data(bucketname, filename, writeas=None):
    if not writeas:
        writeas =  filename
    s3_client.download_file(bucketname, filename, writeas)

def upload_file(bucketname, filename, writeas=None):
    if not writeas:
        writeas =  filename
    s3_client.upload_file(bucketname, filename, writeas)


if __name__ == '__main__':
    respath = os.path.join(rawpath, 'reservations_rec_gov/')
    tabpath = os.path.join(rawpath, 'tables_rec_gov/')
    bucketname = 'recreationbucket'
    directories = ['reservations_rec_gov', 'tables_rec_gov']