from PIL import Image
import glob
from random import randrange

sizes = []
size1 = 292, 140
sizes.append(size1)
size2 = 292, 292
sizes.append(size2)
size3 = 292, 444
sizes.append(size3)
size4 = 140, 140
sizes.append(size4)
size5 = 140, 292
sizes.append(size5)
size6 = 140, 444
sizes.append(size6)


def resize_images():
    file_list = glob.glob('app/static/photography/photos/*')

    for filename in file_list:
        image = Image.open(filename)
        new_size = 350, 350
        image.thumbnail(new_size, Image.ANTIALIAS)
        image.save(filename)

print sizes
resize_images()

