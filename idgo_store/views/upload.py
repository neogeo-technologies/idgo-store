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

# from celery import chain
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from idgo_resource.redis_client import Handler as RedisHandler
from idgo_resource.views import CreateResourceUpload
from idgo_resource.views import DeleteResourceUpload
from idgo_resource.views import EditResourceUpload
from idgo_resource.views import EmitResourceUpload
from idgo_resource.views import ShowResourceUpload
from idgo_resource.views import UpdateResourceUpload

from idgo_store.forms import CreateResourceStoreUploadForm
from idgo_store.forms import EditResourceStoreUploadForm
from idgo_store.forms import EmitResourceStoreUploadForm
from idgo_store.forms import UpdateResourceStoreUploadForm
# from idgo_store.tasks import extract_files
# from idgo_store.tasks import save_ckan_resource
from idgo_store.tasks import asynchronous_tasks


Mime = magic.Magic(mime=True)


LOGIN_URL = settings.LOGIN_URL
decorators = [csrf_exempt, login_required(login_url=LOGIN_URL)]


DIRECTORY_STORAGE = settings.DIRECTORY_STORAGE


class EmitResourceStoreUpload(EmitResourceUpload):
    """Emettre un fichier pour la création d'un répertoire de données téléversé."""

    CreateResourceForm = CreateResourceStoreUploadForm
    EmitResourceForm = EmitResourceStoreUploadForm
    template_emit = 'store/upload/emit.html'
    template_create = 'store/upload/create.html'

    default_resource_type = 'service'


class UpdateResourceStoreUpload(UpdateResourceUpload):
    """Emettre un nouveau fichier pour la création d'un répertoire de données téléversé."""

    UpdateResourceForm = UpdateResourceStoreUploadForm
    template_update = 'store/upload/update.html'
    template_edit = 'store/upload/edit.html'
    related_attr = 'storeupload'


@method_decorator(decorators, name='dispatch')
class CreateResourceStoreUpload(CreateResourceUpload):
    """Créer un répertoire de données téléversé."""

    CreateResourceForm = CreateResourceStoreUploadForm
    app_label = 'idgo_store'
    viewname = 'idgo_store:show_resource_store_upload'

    def run_asynchronous_tasks(self, redis_key, *args, **kwargs):
        data = RedisHandler().retreive(redis_key)

        filename = data['filename']
        dir = os.path.join(DIRECTORY_STORAGE, str(data['resource_pk']))

        ckan_data = self.form.ckan_data
        user_pk = data['user']
        dataset_pk = str(self.form.instance.dataset.pk)
        resource_pk = str(self.form.instance.pk)
        package_id = str(self.form.instance.dataset.ckan_id)

        asynchronous_tasks.s(
            filename, dir, data['content_type'],
            ckan_data, user_pk, dataset_pk, resource_pk, package_id,
            redis_key=redis_key
        ).apply_async()


@method_decorator(decorators, name='dispatch')
class EditResourceStoreUpload(EditResourceUpload):
    """Editer un répertoire de données téléversé."""

    EditResourceForm = EditResourceStoreUploadForm
    viewname = 'idgo_store:show_resource_store_upload'

    def run_asynchronous_tasks(self, redis_key, *args, **kwargs):
        data = RedisHandler().retreive(redis_key)

        filename = data['filename']
        dir = os.path.join(DIRECTORY_STORAGE, str(data['resource_pk']))

        ckan_data = self.form.ckan_data
        user_pk = data['user']
        dataset_pk = str(self.form.instance.dataset.pk)
        resource_pk = str(self.form.instance.pk)
        package_id = str(self.form.instance.dataset.ckan_id)

        asynchronous_tasks.s(
            filename, dir, data['content_type'],
            ckan_data, user_pk, dataset_pk, resource_pk, package_id,
            redis_key=redis_key
        ).apply_async()


@method_decorator(decorators, name='dispatch')
class ShowResourceStoreUpload(ShowResourceUpload):
    """Voir un répertoire de données téléversé."""

    template_show = 'store/upload/show.html'

    def get_context(self, dataset, resource):
        location = os.path.join(DIRECTORY_STORAGE, str(resource.pk))
        files = []
        for filename in Path(location).glob('**/[!_\.]*'):
            if not filename.is_dir():
                path = str(filename.relative_to(location))

                content_type = MimeTypes().guess_type(str(filename))[0] or Mime.from_file(str(filename))
                size = filename.stat().st_size

                file = {
                    'path': path,
                    'content_type': content_type,
                    'size': size
                }
                files.append(file)

        return {'dataset': dataset, 'resource': resource, 'files': files}


@method_decorator(decorators, name='dispatch')
class DeleteResourceStoreUpload(DeleteResourceUpload):
    """Supprimer un répertoire de données téléversé."""
