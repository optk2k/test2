# Generated by Django 3.1.4 on 2020-12-03 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileProcessing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.FileField(upload_to='file_upload')),
                ('date_time_upload', models.DateTimeField(auto_now_add=True)),
                ('date_time_end', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('result', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
