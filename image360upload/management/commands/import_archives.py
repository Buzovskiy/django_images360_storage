import re

from django.core.management.base import BaseCommand
from project.settings import MEDIA_ROOT
import os
from pathlib import Path
from image360upload.models import Image360Archive
from django.core.files.base import ContentFile


class Command(BaseCommand):
    """
    Комманда, которая подтягивает архивы с 3d фото из папки uploaded и для каждого файла
    создает ORM объект c полем archive.
    Если архив уже ранее был подтянут, то файл и объект будет удалены и созданы будут
    новый файл и ORM объект.
    """
    help = 'Command which associates archive file with django orm object'
    path_3d_models = MEDIA_ROOT / '3d_models'

    def __init__(self):
        super(Command, self).__init__()
        Path(self.path_3d_models).mkdir(parents=True, exist_ok=True)

    def handle(self, *args, **options):
        files = [f for f in os.listdir(Path(self.path_3d_models / 'archives/uploaded'))
                 if re.search(r'.*\.zip$', f, re.IGNORECASE)]

        if not len(files):
            return 'error'

        for file in files:
            path_to_archive_uploaded_file = self.path_3d_models / 'archives/uploaded' / file
            with open(Path(path_to_archive_uploaded_file), 'rb') as fh:
                with ContentFile(fh.read()) as file_content:
                    # Set the media attribute of the object, but under an other path/filename
                    model_archive = Image360Archive()
                    model_archive.archive.save(file, file_content)
                    # Save object
                    model_archive.save()

            if os.path.exists(Path(path_to_archive_uploaded_file)):
                os.remove(Path(path_to_archive_uploaded_file))

        return 'success'
