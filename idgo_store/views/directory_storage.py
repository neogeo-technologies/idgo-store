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


import magic
from mimetypes import MimeTypes
import os
import os.path
from pathlib import Path
from urllib.parse import urljoin

from django.conf import settings
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from idgo_admin.models import Dataset
from idgo_resource.models import Resource


Mime = magic.Magic(mime=True)


DIRECTORY_STORAGE = settings.DIRECTORY_STORAGE


class ShowDirectory(object):

    def __init__(self, *args, **kwargs):
        self.location = None

    def iter_files(self, filename=None):
        for filename in Path(self.location).glob(filename or '**/[!_\.]*'):
            yield filename

    def get_file(self, filename):
        try:
            return next(self.iter_files(filename=filename))
        except (StopIteration, SystemError):
            raise KeyError(filename)

    def has_file(self, filename):
        try:
            self.get_file(filename)
        except KeyError:
            return False
        return True


@method_decorator([csrf_exempt], name='dispatch')
class ShowDirectoryStorage(ShowDirectory, View):

    def get(self, request, dataset_id=None, resource_id=None, *args, **kwargs):

        dataset = get_object_or_404(Dataset, id=dataset_id)
        resource = get_object_or_404(Resource, id=resource_id)

        self.location = os.path.join(DIRECTORY_STORAGE, str(resource.pk))
        base_url = request.build_absolute_uri()

        data = []
        for filename in self.iter_files():
            if not filename.is_dir():
                path = str(filename.relative_to(self.location))
                url = urljoin(base_url, path)

                content_type = MimeTypes().guess_type(str(filename))[0] or Mime.from_file(str(filename))
                size = filename.stat().st_size

                data.append({
                    'url': url,
                    'content-type': content_type,
                    'size': size
                })

        return JsonResponse(data, safe=False)


@method_decorator([csrf_exempt], name='dispatch')
class ShowDirectoryStorageGlob(ShowDirectory, View):

    def get(self, request, dataset_id=None, resource_id=None, glob_path=None, *args, **kwargs):

        get_object_or_404(Dataset, id=dataset_id)
        get_object_or_404(Resource, id=resource_id)

        self.location = os.path.join(DIRECTORY_STORAGE, resource_id)
        if not self.has_file(glob_path):
            raise Http404()

        filename = str(Path(self.location).joinpath(glob_path))
        content_type = MimeTypes().guess_type(str(filename))[0] or mime.from_file(str(filename))

        with open(filename, 'rb') as data:
            return HttpResponse(data, content_type=content_type)
