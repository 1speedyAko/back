# Generated by Django 5.0.6 on 2024-08-10 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_alter_usersubscription_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptionplan',
            name='description',
        ),
        migrations.RemoveField(
            model_name='subscriptionplan',
            name='name',
        ),
        migrations.RemoveField(
            model_name='subscriptionplan',
            name='price',
        ),
    ]