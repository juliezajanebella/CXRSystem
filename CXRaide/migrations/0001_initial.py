# Generated by Django 4.1.6 on 2024-05-20 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnnotatedImage',
            fields=[
                ('annotated_cxray_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Annotated CXray Image ID')),
                ('annotated_cxray_filename', models.CharField(max_length=100, verbose_name='Annotated CXRay File Name')),
                ('annotated_cxray_image', models.ImageField(upload_to='annotated_images/', verbose_name='Annotated CXray Image')),
            ],
        ),
        migrations.CreateModel(
            name='AnnotatedImageByAi',
            fields=[
                ('annotated_cxray_id_ai', models.AutoField(primary_key=True, serialize=False, verbose_name='Annotated CXray Image By AI ID')),
                ('annotated_cxray_filename_ai', models.CharField(max_length=100, verbose_name='Annotated CXRay By AI File Name')),
                ('annotated_cxray_ai_image', models.ImageField(upload_to='annotated_images/', verbose_name='Annotated CXray Image By AI')),
            ],
        ),
        migrations.CreateModel(
            name='Radiologist',
            fields=[
                ('radiologist_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Radiologist ID')),
                ('radiologist_username', models.CharField(max_length=100, verbose_name='Username')),
                ('radiologist_firstname', models.CharField(max_length=100, verbose_name='First Name')),
                ('radiologist_lastname', models.CharField(max_length=100, verbose_name='Last Name')),
                ('radiologist_password', models.CharField(max_length=100, verbose_name='Password')),
                ('radiologist_email', models.CharField(max_length=100, verbose_name='Email')),
            ],
        ),
        migrations.CreateModel(
            name='RawXray',
            fields=[
                ('raw_cxray_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Raw CXray Image ID')),
                ('raw_cxray_filename', models.CharField(max_length=100, verbose_name='Raw CXRay File Name')),
                ('raw_cxray_image', models.ImageField(upload_to='raw_images/', verbose_name='Raw CXray Image')),
            ],
        ),
    ]
