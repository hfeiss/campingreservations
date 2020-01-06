import os

srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]

if __name__ == '__main__':
    bashCommand = f'aws2 s3 sync s3://recreationbucket {rootpath}'
    os.system(bashCommand)