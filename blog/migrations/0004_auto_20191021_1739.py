# Generated by Django 2.2.4 on 2019-10-21 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20191021_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='Image',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='posts_pics'),
        ),
    ]
