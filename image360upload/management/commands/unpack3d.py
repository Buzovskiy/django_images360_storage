import fnmatch
import re

from django.core.management.base import BaseCommand, CommandError
from project.settings import MEDIA_ROOT
import os
import pathlib
import zipfile
import shutil
from PIL import Image


class Command(BaseCommand):
    help = 'Command which makes 3d images'
    root_path_3d = MEDIA_ROOT / '3d_models'

    def __init__(self):
        super(Command, self).__init__()
        pathlib.Path(self.root_path_3d).mkdir(parents=True, exist_ok=True)

    def handle(self, *args, **options):
        files = [f for f in os.listdir(pathlib.Path(self.root_path_3d))
                 if re.search(r'.*\.zip$', f, re.IGNORECASE)]

        if not len(files):
            return False

        for file in files:
            dir_model_3d = os.path.splitext(pathlib.Path(self.root_path_3d) / file)[0]
            # try:
            #     shutil.rmtree(pathlib.Path(self.root_path_3d) / dir_model_3d)
            # except OSError as e:
            #     print("Error: %s : %s" % (pathlib.Path(self.root_path_3d) / dir_model_3d, e.strerror))
            # Create directories
            datetime.date.today().strftime('%Y-%m-%d')
            pathlib.Path(self.root_path_3d / dir_model_3d / 'images').mkdir(parents=True, exist_ok=True)
            pathlib.Path(self.root_path_3d / dir_model_3d / 'imageslarge').mkdir(parents=True, exist_ok=True)
            # Extract images from archive
            with zipfile.ZipFile(pathlib.Path(self.root_path_3d) / file, 'r') as zip_ref:
                zip_ref.extractall(pathlib.Path(self.root_path_3d / dir_model_3d / 'imageslarge'))
            # Resize images
            images = [f for f in os.listdir(pathlib.Path(self.root_path_3d / dir_model_3d / 'imageslarge'))
                      if re.search(r'.*\.(jpeg|jpg|gif|png|tiff|bmp)$', f, re.IGNORECASE)]
            if not len(images):
                return False

            for image in images:
                im = Image.open(pathlib.Path(self.root_path_3d / dir_model_3d / 'imageslarge' / image))
                newsize = (400, 288)
                new_im = im.resize(newsize)
                new_im.save(pathlib.Path(self.root_path_3d / dir_model_3d / 'images' / image))


        # archives_path = pathlib.Path(self.root_path_3d).glob('*.zip')
        # print(os.listdir(pathlib.Path(self.root_path_3d)))
        # def filter_files(zip_path):
        #     if not pathlib.Path(self.root_path_3d / zip_path).is_file():
        #         return False
        #     else:
        #         return True
        # zip_files_list = os.listdir(pathlib.Path(self.root_path_3d))
        # zip_files_list = list(filter(filter_files, zip_files_list))
        # print(zip_files_list)
        # for file in os.listdir(pathlib.Path(self.root_path_3d)):
        #     if fnmatch.fnmatch(file, '*.zip'):
        #         print(file)
        self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"'))
