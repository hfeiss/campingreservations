import os

srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]


def upload_to_S3(destination, exclusions):
    options = ' --delete --size-only'
    no_upload = str()
    for exclusion in exclusions:
        no_upload += (f' --exclude "{exclusion}"')
    bashCommand = f'aws2 s3 sync {rootpath}{no_upload}{options}'
    print(bashCommand)
    # os.system(bashCommand)


if __name__ == '__main__':
    upload_to_S3('s3://recreationbucket/',
                 ['*/.git/*', '*/.DS_Store'])
