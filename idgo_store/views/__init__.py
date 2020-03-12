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

from idgo_store.views.ftp import CreateResourceStoreFtp
from idgo_store.views.ftp import EditResourceStoreFtp
from idgo_store.views.ftp import EmitResourceStoreFtp
from idgo_store.views.ftp import DeleteResourceStoreFtp
from idgo_store.views.ftp import ShowResourceStoreFtp
from idgo_store.views.ftp import UpdateResourceStoreFtp
from idgo_store.views.directory_storage import ShowDirectoryStorage
from idgo_store.views.directory_storage import ShowDirectoryStorageGlob
from idgo_store.views.upload import CreateResourceStoreUpload
from idgo_store.views.upload import EditResourceStoreUpload
from idgo_store.views.upload import EmitResourceStoreUpload
from idgo_store.views.upload import DeleteResourceStoreUpload
from idgo_store.views.upload import ShowResourceStoreUpload
from idgo_store.views.upload import UpdateResourceStoreUpload


__all__ = [
    CreateResourceStoreFtp,
    CreateResourceStoreUpload,
    EditResourceStoreFtp,
    EditResourceStoreUpload,
    EmitResourceStoreFtp,
    EmitResourceStoreUpload,
    DeleteResourceStoreFtp,
    DeleteResourceStoreUpload,
    ShowDirectoryStorage,
    ShowDirectoryStorageGlob,
    ShowResourceStoreFtp,
    ShowResourceStoreUpload,
    UpdateResourceStoreFtp,
    UpdateResourceStoreUpload,
]
