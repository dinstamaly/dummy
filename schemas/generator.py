import os

from .models import Schema, DataSet
from django.conf import settings
from celery import shared_task
from faker import Faker
import pandas as pd
import io
import boto3


class Csv:
    def __init__(self, schema, rows, pk):
        self.Schema = Schema.objects.get(id=schema)
        self.columns = self.Schema.column_m_set.order_by("order")
        self.rows = int(rows)
        self.DataSet = DataSet.objects.get(id=pk)
        self.fake = Faker()

    def data_gen(self):
        head, data = self.serialize()
        csv_text = self.fake.dsv(header=head, data_columns=data,
                                 num_rows=self.rows, delimiter=',')
        text = io.StringIO(csv_text)
        csv = io.StringIO()
        df = pd.read_csv(text, sep=",", index_col=head[0])
        df.to_csv(csv)
        filename = f'result_{self.DataSet.id}.csv'
        session = boto3.session.Session()  #
        # session = boto3.Session(
        #     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        #     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        #     region_name='nyc3',
        # )
        client = session.client(
            's3',
            region_name='nyc3',
            endpoint_url='https://nyc3.digitaloceanspaces.com',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        client.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=settings.AWS_STORAGE_BUCKET_NAME+'/mediafiles/' + filename,
            Body=csv.getvalue(),
                          # Metadata={
                          #     'x-amz-meta-my-key': 'your-value'
                          # }
            )
        client.put_object_acl(
            ACL='public-read', Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=settings.AWS_STORAGE_BUCKET_NAME+'/mediafiles/' + filename,
        )
        # s3 = session.resource('s3')
        # obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME,
        #                 'mediafiles/' + filename)
        # print(obj)
        # print(csv.getvalue())
        # obj.put(Body=csv.getvalue(), Key='mediafiles/' + filename)
        url = settings.MEDIA_URL + filename
        self.DataSet.status = 'Ready'
        self.DataSet.file = str(url)
        self.DataSet.save()
        return str(url)

    def serialize(self):
        data = []
        head = []
        for idc, column in enumerate(self.columns):
            if column.from_int and column.to_int is not None:
                if str(column.data_type) == 'integer':
                    data.append("{{pyint:range" + str(idc) + "}}")
                    self.fake.set_arguments(
                        'range' + str(idc),
                        {
                            'min_value': column.from_int,
                            'max_value': column.to_int
                        }
                    )
                else:
                    data.append("{{" + str(column.data_type) + "}}")
            else:
                if str(column.data_type) == 'integer':
                    data.append("{{pyint}}")
                else:
                    data.append("{{" + str(column.data_type) + "}}")
            head.append(column.name)
        return tuple(head), tuple(data)
