from PIL import Image
import os

# Create filepaths within df directory
srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]
datapath = os.path.join(rootpath, 'data/')
imagepath = os.path.join(rootpath, 'images/')


def make_gif(sourcepath, folder, years=None):
    list_years = []
    if years:
        list_years = years
    else:
        for root, dirs, file in os.walk(sourcepath):
            list_years.extend(file)
    list_years.sort()

    frames = []
    for year in list_years:
        new_frame = Image.open(sourcepath + year)
        frames.append(new_frame)

    frames[0].save(f'{imagepath}/{folder}.gif',
                   format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=1200,
                   loop=0)


if __name__ == '__main__':
    make_gif(imagepath + 'maps/CustomerState/', 'CustomerState')
    make_gif(imagepath + 'maps/FacilityState/', 'FacilityState')
