import datetime
import fnmatch
import re

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from project.settings import MEDIA_ROOT
import os
from pathlib import Path
import zipfile
import shutil
from PIL import Image
from image360upload.models import Image360, Model3dArchive


class Command(BaseCommand):
    help = 'Command which makes 3d images'
    path_3d_models = MEDIA_ROOT / '3d_models'

    def __init__(self):
        super(Command, self).__init__()
        Path(self.path_3d_models).mkdir(parents=True, exist_ok=True)

    def handle(self, outer_queryset=None, *args, **options):
        if outer_queryset is None:
            archives = Model3dArchive.objects.all()
        else:
            archives = outer_queryset

        if not archives.count():
            return False

        for archive in archives:
            dir_name = os.path.splitext(os.path.basename(archive.archive.name))[0]
            iframe_src = Path(self.path_3d_models / 'Components/template_1/iframe.html')
            with open(Path(iframe_src), 'rb') as fh:
                with ContentFile(fh.read()) as file_content:
                    # Set the media attribute of the object, but under an other path/filename
                    image360 = Image360()
                    image360.vendor_code = dir_name
                    image360.iframe.save('iframe.html', file_content)
                    # Save object
                    image360.save()

        #
        # for file in files:
        #     dir_model_name = os.path.splitext(os.path.basename(Path(self.root_path_3d) / file))[0]
        #     with open(Path(self.root_path_3d), 'w') as f:





    # def handle(self, *args, **options):
    #     files = [f for f in os.listdir(Path(self.root_path_3d))
    #              if re.search(r'.*\.zip$', f, re.IGNORECASE)]
    #
    #     if not len(files):
    #         return False
    #
    #     for file in files:
    #         dir_model_name = os.path.splitext(os.path.basename(Path(self.root_path_3d) / file))[0]
    #
    #         self.remove_old_models(dir_model_name)
    #
    #         # Create directories
    #         dir_model_path = self.root_path_3d / datetime.date.today().strftime('%Y-%m-%d') / dir_model_name
    #         Path(dir_model_path / 'images').mkdir(parents=True, exist_ok=True)
    #         Path(dir_model_path / 'imageslarge').mkdir(parents=True, exist_ok=True)
    #
    #         # Extract images from archive
    #         with zipfile.ZipFile(Path(self.root_path_3d) / file, 'r') as zip_ref:
    #             zip_ref.extractall(Path(dir_model_path / 'imageslarge'))
    #         # Resize images
    #         images = [f for f in os.listdir(Path(dir_model_path / 'imageslarge'))
    #                   if re.search(r'.*\.(jpeg|jpg|gif|png|tiff|bmp)$', f, re.IGNORECASE)]
    #         if not len(images):
    #             return False
    #
    #         for image in images:
    #             im = Image.open(Path(dir_model_path / 'imageslarge' / image))
    #             newsize = (400, 288)
    #             new_im = im.resize(newsize)
    #             new_im.save(Path(dir_model_path / 'images' / image))
    #         # Copy files
    #         files_to_copy = ['config.js', 'iframe.html', 'index.html']
    #         for file_to_copy in files_to_copy:
    #             shutil.copy(
    #                 Path(self.root_path_3d / 'Components/template_1' / file_to_copy),
    #                 Path(dir_model_path / file_to_copy)
    #             )
    #
    # def remove_old_models(self, dir_model_name):
    #     matches = [Path(m) for m in list(Path(self.root_path_3d).glob(f"**/{dir_model_name}"))
    #                if Path(m).is_dir()]
    #     if not len(matches):
    #         return False
    #
    #     for match in matches:
    #         try:
    #             shutil.rmtree(match)
    #         except OSError as e:
    #             print("Error: %s : %s" % (match, e.strerror))
    #
    #
    #
    #
    #     # archives_path = pathlib.Path(self.root_path_3d).glob('*.zip')
    #     # print(os.listdir(pathlib.Path(self.root_path_3d)))
    #     # def filter_files(zip_path):
    #     #     if not pathlib.Path(self.root_path_3d / zip_path).is_file():
    #     #         return False
    #     #     else:
    #     #         return True
    #     # zip_files_list = os.listdir(pathlib.Path(self.root_path_3d))
    #     # zip_files_list = list(filter(filter_files, zip_files_list))
    #     # print(zip_files_list)
    #     # for file in os.listdir(pathlib.Path(self.root_path_3d)):
    #     #     if fnmatch.fnmatch(file, '*.zip'):
    #     #         print(file)
    #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"'))
