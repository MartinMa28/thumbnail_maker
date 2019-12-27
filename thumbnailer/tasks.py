import os
from zipfile import ZipFile
from celery import shared_task
from PIL import Image

from django.conf import settings


@shared_task
def adding_task(x, y):
    return x + y


@shared_task
def make_thumbnails(file_path, thumbnails=[]):
    os.chdir(settings.IMAGES_DIR)
    path, file_name_with_ext = os.path.split(file_path)
    file_name, ext = os.path.splitext(file_name_with_ext)

    zip_file = f'{file_name}.zip'
    results = {'archive_path': f'{settings.MEDIA_URL}images/{zip_file}'}

    try:
        img = Image.open(file_path)
        zipper = ZipFile(zip_file, 'w')
        zipper.write(file_name_with_ext)
        os.remove(file_path)

        for w, h in thumbnails:
            img_copy = img.copy()
            img_copy.thumbnail((w, h))
            thumbnail_file = f'{file_name}_{w}x{h}.{ext}'
            img_copy.save(thumbnail_file)
            zipper.write(thumbnail_file)
            os.remove(thumbnail_file)

        img.close()
        zipper.close()
    except IOError as e:
        print(e)

    return results
