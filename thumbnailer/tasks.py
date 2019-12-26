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
    os.chdir(settings.IMAGE_DIR)
    path, file_name = os.path.split(file_path)
    