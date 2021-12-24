import re

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from project.settings import MEDIA_ROOT
import os
from pathlib import Path
import zipfile
import shutil
from PIL import Image
from image360upload.models import Image360, Image360Archive
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    """
    The programm for creation of images 360:
    -  get imported archives with images by requesting the database;
    - look for the duplicated of images 360 by archive name. If the copies are found they are to be deleted;
    - Create object of image 360 in the datebase. Associate it with the file iframe.html. As a result the directory of
      image 360 is created with the vendor code name where iframe.html is put;
    - unzip archive.
    - in specified directory the imageslarge folder is created and images from the archive are put;
    - create images folder and put there resized images;
    - copy necessary components in image 360 folder.
    """
    help = 'Command which makes images 360'
    path_3d_models = MEDIA_ROOT / '3d_models'

    def __init__(self):
        super(Command, self).__init__()
        Path(self.path_3d_models).mkdir(parents=True, exist_ok=True)

    def handle(self, outer_queryset=None, request=None, *args, **options):
        if outer_queryset is None:
            archives = Image360Archive.objects.all()
        else:
            archives = outer_queryset

        if not archives.count():
            return False

        for archive in archives:
            # Название папки, куда ложим файлы модели 360
            dir_name = os.path.splitext(os.path.basename(archive.archive.name))[0]
            # Если в базе есть такой же артикул, удаляем запись из базы с файлами.
            for model360 in Image360.objects.filter(vendor_code=dir_name):
                model360.delete()

            iframe_src = Path(self.path_3d_models / 'Components/template_1/iframe.html')
            with open(Path(iframe_src), 'rb') as fh:
                with ContentFile(fh.read()) as file_content:
                    # Set the media attribute of the object, but under an other path/filename
                    image360 = Image360()
                    image360.vendor_code = dir_name
                    image360.iframe.save('iframe.html', file_content)
                    # Save object
                    image360.save()

            # Get path to parent directory of the image 360
            image360_path = Path(image360.iframe.path).parent
            Path(image360_path / 'images').mkdir(parents=True, exist_ok=True)

            # Extract images from archive
            with zipfile.ZipFile(Path(archive.archive.path), 'r') as zip_ref:
                zip_ref.extractall(Path(image360_path / 'imageslarge'))
            # Resize images
            images = [f for f in os.listdir(Path(image360_path / 'imageslarge'))
                      if re.search(r'.*\.(jpeg|jpg|gif|png|tiff|bmp)$', f, re.IGNORECASE)]
            if not len(images):
                print(_('No images found in archive'))
                messages.warning(request, _('No images found in archive'))

            for image in images:
                im = Image.open(Path(image360_path / 'imageslarge' / image))
                newsize = (400, 288)
                new_im = im.resize(newsize)
                new_im.save(Path(image360_path / 'images' / image))
            # Copy files
            files_to_copy = ['config.js', 'index.html']
            for file_to_copy in files_to_copy:
                shutil.copy(
                    Path(self.path_3d_models / 'Components/template_1' / file_to_copy),
                    Path(image360_path / file_to_copy)
                )

            archive.delete()

