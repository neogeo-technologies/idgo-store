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


import io
from uuid import UUID

from celery.decorators import task
# from celery.signals import after_task_publish
from celery.signals import before_task_publish
# from celery.signals import task_failure
# from celery.signals import task_postrun
# from celery.signals import task_prerun
# from celery.signals import task_rejected
# from celery.signals import task_revoked
# from celery.signals import task_success
# from celery.signals import task_unknown
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from django.conf import settings

from celeriac.models import TaskTracking
from idgo_admin.ckan_module import CkanHandler
from idgo_admin.ckan_module import CkanUserHandler
# from idgo_resource.redis_client import Handler as RedisHandler

from idgo_store.utils import get_html_content
from idgo_store.utils import unzip


logger = get_task_logger(__name__)


DIRECTORY_STORAGE = settings.DIRECTORY_STORAGE
DOMAIN = settings.DOMAIN_NAME


@before_task_publish.connect
def on_beforehand(headers=None, body=None, sender=None, **kwargs):
    TaskTracking.objects.create(
        uuid=UUID(body.get('id')), task=body.get('task'), detail=body)

#     id = body['id']
#     task = body['task']
#     redis_key = body['kwargs'].get('redis_key')
#
#     if redis_key:
#         data = RedisHandler().retreive(redis_key)
#         if 'tasks' not in data.keys():
#             data['tasks'] = []
#         data['tasks'].append({'id': id, 'task': task})
#         RedisHandler().update(redis_key, **data)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ #


# @task(name='extract_files', ignore_result=False)
# def extract_files(filename, dir, content_type, flush=False, **kwargs):
#
#     if content_type.endswith('zip'):
#         unzip(filename, dir, flush=flush)
#     else:
#         raise NotImplementedError('TODO')


# @task(name='save_ckan_resource', ignore_result=False)
# def save_ckan_resource(data, user_pk, dataset_pk, resource_pk, package_id, **kwargs):
#
#     username = User.objects.get(pk=user_pk).username
#     apikey = CkanHandler.get_user(username)['apikey']
#
#     html = get_html_content(dataset_pk, resource_pk)
#     upload = io.BytesIO(html.encode('utf-8'))
#     data['upload'] = upload
#
#     ckan_package = CkanHandler.get_package(package_id)
#     apikey = CkanHandler.get_user(username)['apikey']
#     with CkanUserHandler(apikey=apikey) as ckan:
#         ckan.publish_resource(ckan_package, **data)
#
#     upload.close()


@task(name='asynchronous_tasks', ignore_result=False)
def asynchronous_tasks(
        filename, dir, content_type,
        data, user_pk, dataset_pk, resource_pk, package_id,
        **kwargs):

    if content_type.endswith('zip'):
        unzip(filename, dir, flush=True)
    else:
        raise NotImplementedError('TODO')

    username = User.objects.get(pk=user_pk).username
    apikey = CkanHandler.get_user(username)['apikey']

    html = get_html_content(dataset_pk, resource_pk)
    upload = io.BytesIO(html.encode('utf-8'))
    data['upload'] = upload

    ckan_package = CkanHandler.get_package(package_id)
    apikey = CkanHandler.get_user(username)['apikey']
    with CkanUserHandler(apikey=apikey) as ckan:
        ckan.publish_resource(ckan_package, **data)

    upload.close()