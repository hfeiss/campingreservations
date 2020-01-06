import os

srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]
src_datapath = os.path.join(srcpath, 'data')
vispath = os.path.join(srcpath, 'visualizations')

if __name__ == '__main__':
    bashCommand = f'aws2 s3 sync {rootpath} s3://recreationbucket/ --exclude ".git/*" --exclude ".DS_Store" --size-only true'
    os.system(bashCommand)