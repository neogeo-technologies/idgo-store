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
import json
import magic
from operator import iconcat

from django.conf import settings
from django import forms

from idgo_resource.forms.upload import BaseResourceUploadForm
from idgo_resource.forms.upload import ResourceUploadForm
from idgo_resource.models import ResourceFormats

from idgo_store.models import StoreUpload


Mime = magic.Magic(mime=True)


DIRECTORY_STORAGE = settings.DIRECTORY_STORAGE
DOMAIN = settings.DOMAIN_NAME


EXTENSIONS = getattr(settings, 'RESOURCE_STORE_EXTENSIONS', ['zip'])
try:
    filter = {'extension__in': EXTENSIONS, 'is_gis_format': False}
    RESOURCE_FORMATS = ResourceFormats.objects.filter(**filter).order_by('extension')
except:
    RESOURCE_FORMATS = []


class ModelResourceStoreUploadForm(ResourceUploadForm, forms.ModelForm):

    class Meta:
        model = StoreUpload
        fields = (
            'file_path',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extensions = EXTENSIONS
        self.mimetypes = list(set(reduce(iconcat, [item.mimetype for item in RESOURCE_FORMATS], [])))
        self.fields['file_path'].widget.attrs['accept'] = ', '.join(self.mimetypes)


class EmitResourceStoreUploadForm(ModelResourceStoreUploadForm):
    pass


class UpdateResourceStoreUploadForm(ModelResourceStoreUploadForm):
    pass


class BaseResourceStoreUploadForm(BaseResourceUploadForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['format_type'].queryset = RESOURCE_FORMATS

    def save(self, *args, **kwargs):
        kwargs['app_label'] = 'idgo_store'
        return super().save(*args, **kwargs)

    @property
    def ckan_data(self):
        return {
            'id': str(self.instance.ckan_id),
            'url': self.instance.storeupload.url,
            'name': self.instance.title,
            'description': self.instance.description,
            'lang': self.instance.language,
            'data_type': self.instance.resource_type,
            'upload': None,
            'size': '',
            'format': '',
            'mimetype': 'text/html',
            'view_type': 'text_view',
            'api': '{}',
            'restricted_by_jurisdiction': '',
            'extracting_service': 'False',
            'crs': '',
            'restricted': json.dumps({'level': 'public'}),
        }


class CreateResourceStoreUploadForm(BaseResourceStoreUploadForm):
    """Formulaire de création d'un répertoire de données téléversé."""


class EditResourceStoreUploadForm(BaseResourceStoreUploadForm):
    """Formulaire d'édition d'un répertoire de données téléversé."""
