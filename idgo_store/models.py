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


import os
import shutil
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.gis.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

from idgo_resource import logger

from idgo_resource.models import AbstractResourceFile


class Store(models.Model):
    """Modèle de classe abstrait de répertoires de données."""

    class Meta:
        abstract = True

    @property
    def url(self):
        domain = settings.DOMAIN_NAME
        path = reverse('idgo_store:directory_storage', kwargs={
            'dataset_id': self.resource.dataset.pk,
            'resource_id': self.resource.pk
        })
        return urljoin(domain, path)


class StoreUpload(AbstractResourceFile, Store):
    """Modèle de classe de répertoires de données téléversées."""

    class Meta(object):
        db_table = 'idgo_store_upload'
        verbose_name = "Répertoire de données téléversée"
        verbose_name_plural = "Répertoire de données téléversées"


class StoreFtp(AbstractResourceFile, Store):
    """Modèle de classe de répertoires de données issus du FTP."""

    class Meta(object):
        db_table = 'idgo_store_ftp'
        verbose_name = "Répertoire de données issu du FTP."
        verbose_name_plural = "Répertoire de données issus du FTP."


@receiver(pre_save, sender=Store)
def auto_delete_file_on_store_delete(sender, instance, **kwargs):
    """Supprimer le fichier du dossier de stockage
    à la suppression d'une instance Store."""

    if hasattr(instance, 'file_path'):
        # Django > 2.x
        # instance.file_path.storage.delete(instance.file_path.name)
        # Django 1.11
        if os.path.isfile(instance.file_path.path):
            os.remove(instance.file_path.path)

    if hasattr(instance, 'resource'):
        dir = os.path.join(settings.DIRECTORY_STORAGE, str(instance.resource.pk))
        try:
            shutil.rmtree(dir)
        except FileNotFoundError as e:
            logger.warning(e)


@receiver(pre_save, sender=Store)
def auto_delete_file_on_store_change(sender, instance, **kwargs):
    """Supprimer l'ancien fichier du dossier de stockage
    à la modification d'une instance Store si le fichier est différent."""

    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).file_path
    except sender.DoesNotExist:
        return False

    new_file = instance.file_path
    if not old_file == new_file:
        # Django > 2.x
        # instance.file_path.storage.delete(old_file.name)
        # Django 1.11
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
