# Generated by Django 3.2.3 on 2021-06-01 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_row', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('Processing', 'Processing'), ('Ready', 'Ready')], default='Processing', max_length=50)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('file', models.FileField(null=True, upload_to='data_sets/')),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schemas.schema')),
            ],
        ),
        migrations.CreateModel(
            name='Column_m',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('from_int', models.IntegerField(blank=True, null=True)),
                ('to_int', models.IntegerField(blank=True, null=True)),
                ('data_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schemas.type')),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schemas.schema')),
            ],
        ),
    ]
