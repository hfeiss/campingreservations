import os

srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]
src_datapath = os.path.join(srcpath, 'data')
vispath = os.path.join(srcpath, 'visualizations')

if __name__ == '__main__':
    '''
    folders = [srcpath, vispath]
    for folder in folders:
        folder_name = os.path.basename(folder)
        bashCommand = f'aws2 s3 sync {folder} s3://recreationbucket/{folder_name}'
        os.system(bashCommand)
    '''
    bashCommand = f'aws2 s3 sync s3://recreationbucket {rootpath}'
    os.system(bashCommand)