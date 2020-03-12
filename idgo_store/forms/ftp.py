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


import json
import magic

from django.conf import settings
from django import forms

from idgo_resource.forms.ftp import BaseResourceFtpForm
from idgo_resource.forms.ftp import ResourceFtpForm
from idgo_resource.models import ResourceFormats

from idgo_store.models import StoreFtp


Mime = magic.Magic(mime=True)


DIRECTORY_STORAGE = settings.DIRECTORY_STORAGE
DOMAIN = settings.DOMAIN_NAME


EXTENSIONS = getattr(settings, 'RESOURCE_STORE_EXTENSIONS', ['zip'])
try:
    filter = {'extension__in': EXTENSIONS, 'is_gis_format': False}
    RESOURCE_FORMATS = ResourceFormats.objects.filter(**filter).order_by('extension')
except:
    RESOURCE_FORMATS = []


class ResourceStoreFtpForm(ResourceFtpForm):

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, user=user, resource_formats=RESOURCE_FORMATS, **kwargs)


class ModelResourceStoreFtpForm(ResourceStoreFtpForm, forms.ModelForm):

    class Meta:
        model = StoreFtp
        fields = (
            'file_path',
        )


class EmitResourceStoreFtpForm(ModelResourceStoreFtpForm):
    pass


class UpdateResourceStoreFtpForm(ModelResourceStoreFtpForm):
    pass


class BaseResourceStoreFtpForm(BaseResourceFtpForm):

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
            'url': self.instance.storeftp.url,
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


class CreateResourceStoreFtpForm(BaseResourceStoreFtpForm):
    """Formulaire de création d'un répertoire de données téléversé."""


class EditResourceStoreFtpForm(BaseResourceStoreFtpForm):
    """Formulaire d'édition d'un répertoire de données téléversé."""
