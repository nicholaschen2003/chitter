# Generated by Django 3.2 on 2021-04-12 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_post_replying_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poster',
            name='liked_posts',
            field=models.CharField(default='', max_length=200),
        ),
    ]
