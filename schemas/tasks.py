from __future__ import absolute_import, unicode_literals

import os

from celery import shared_task
from django.conf import settings

from .generator import Csv


@shared_task
def form_fake_data(schema, rows, pk):
    csv = Csv(schema, rows, pk)

    print(f'Task {pk} Done')
    print(csv.data_gen())
    return csv.data_gen()