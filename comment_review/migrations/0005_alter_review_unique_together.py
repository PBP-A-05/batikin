# Generated by Django 5.1.2 on 2024-10-27 11:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment_review', '0004_alter_review_product_delete_product'),
        ('shopping', '0002_alter_order_user_alter_orderitem_order'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('user', 'product')},
        ),
    ]
