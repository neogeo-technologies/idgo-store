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


from django.conf.urls import url

from idgo_store.views import CreateResourceStoreFtp
from idgo_store.views import CreateResourceStoreUpload
from idgo_store.views import DeleteResourceStoreFtp
from idgo_store.views import DeleteResourceStoreUpload
from idgo_store.views import EditResourceStoreFtp
from idgo_store.views import EditResourceStoreUpload
from idgo_store.views import EmitResourceStoreFtp
from idgo_store.views import EmitResourceStoreUpload
from idgo_store.views import ShowDirectoryStorage
from idgo_store.views import ShowDirectoryStorageGlob
from idgo_store.views import ShowResourceStoreFtp
from idgo_store.views import ShowResourceStoreUpload
from idgo_store.views import UpdateResourceStoreFtp
from idgo_store.views import UpdateResourceStoreUpload


urlpatterns = [
    url('^dataset/(?P<dataset_id>(\d+))/resource/new/store/ftp/$', EmitResourceStoreFtp.as_view(), name='emit_resource_store_ftp'),
    url('^dataset/(?P<dataset_id>(\d+))/resource/new/store/ftp/create/$', CreateResourceStoreFtp.as_view(), name='create_resource_store_ftp'),
    url('^dataset/(?P<dataset_id>(\d+))/resource/(?P<resource_id>(\d+))/store/ftp/show/$', ShowResourceStoreFtp.as_view(), name='show_resource_store_ftp'),
    url('^dataset/(?P<dataset_id>(\d+))/resource/(?P<resource_id>(\d+))/store/ftp/edit/$', EditResourceStoreFtp.as_view(), name='edit_resource_store_ftp'),
    url('^dataset/(?P<dataset_id>(\d+))/resource/(?P<resource_id>(\d+))/store/ftp/update/$', UpdateResourceStoreFtp.as_view(), name='update_resource_store_ftp'),
    url('^dataset/(?P<dataset_id>(\d+))/resource/(?P<resource_id>(\d+))/store/ftp/delete/$', DeleteResourceStoreFtp.as_view(), name='delete_resource_store_ftp'),
    url('^dataset/(?P<dataset_id>(\d+))/resource/new/store/upload/$', EmitResourceStoreUpload.as_view(), name='emit_resource_store_upload'),
    url('^dataset/(?P<dataset_id>(\d+))/resource/new/store/upload/create/$', CreateResourceStoreUpload.as_view(), name='create_resource_store_upload'),
    url('^dataset/(?P<dataset_id>(\d+))/resource/(?P<resource_id>(\d+))/store/upload/show/$', ShowResourceStoreUpload.as_view(), name='show_resource_store_upload'),
    url('^dataset/(?P<dataset_id>(\d+))/resource/(?P<resource_id>(\d+))/store/upload/edit/$', EditResourceStoreUpload.as_view(), name='edit_resource_store_upload'),
    url('^dataset/(?P<dataset_id>(\d+))/resource/(?P<resource_id>(\d+))/store/upload/update/$', UpdateResourceStoreUpload.as_view(), name='update_resource_store_upload'),
    url('^dataset/(?P<dataset_id>(\d+))/resource/(?P<resource_id>(\d+))/store/upload/delete/$', DeleteResourceStoreUpload.as_view(), name='delete_resource_store_upload'),
    url('^dataset/(?P<dataset_id>(\d+))/resource/(?P<resource_id>(\d+))/store/directory/$', ShowDirectoryStorage.as_view(), name='directory_storage'),
    url('^dataset/(?P<dataset_id>(\d+))/resource/(?P<resource_id>(\d+))/store/directory/(?P<glob_path>(.+))/?$', ShowDirectoryStorageGlob.as_view(), name='directory_storage_glob'),
]
