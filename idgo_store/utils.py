# Copyright (c) 2017-2020 Neogeo-Technologies.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from functools import reduce
import magic
from mimetypes import MimeTypes
import os
from pathlib import Path
import shutil
from urllib.parse import urljoin
from zipfile import ZipFile

from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string


Mime = magic.Magic(mime=True)


DIRECTORY_STORAGE = settings.DIRECTORY_STORAGE
DOMAIN = settings.DOMAIN_NAME


def unzip(filename, dir, flush=False):
    with ZipFile(filename, 'r') as z:
        if flush and Path(dir).exists():
            shutil.rmtree(dir)
        Path(dir).mkdir(parents=True, exist_ok=True)
        z.extractall(dir)


def iterate(location, base_url=None):
    files = []
    for filename in Path(location).glob('**/[!_\.]*'):
        if not filename.is_dir():
            href = reduce(
                urljoin, [DOMAIN, base_url, str(filename.relative_to(location))])
            content_type = MimeTypes().guess_type(str(filename))[0] or Mime.from_file(str(filename))
            size = filename.stat().st_size

            files.append({
                'content_type': content_type,
                'href': href,
                'size': size,
            })
    return files


def get_html_content(dataset_id, resource_id):
    location = os.path.join(DIRECTORY_STORAGE, resource_id)
    base_url = reverse('idgo_store:directory_storage', kwargs={
        'dataset_id': dataset_id, 'resource_id': resource_id})

    files = iterate(location, base_url=base_url)

    return render_to_string(
        'store/ckan_resource_template.html', context={'files': files})