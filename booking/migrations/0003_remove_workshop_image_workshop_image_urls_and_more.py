# Generated by Django 4.2.15 on 2024-10-25 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_workshop_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshop',
            name='image',
        ),
        migrations.AddField(
            model_name='workshop',
            name='image_urls',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='workshop',
            name='open_time',
            field=models.CharField(default='', max_length=50),
        ),
    ]
