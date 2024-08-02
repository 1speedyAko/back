# Generated by Django 5.0.6 on 2024-07-30 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_alter_subscriptionplan_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='category',
            field=models.CharField(blank=True, choices=[('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum')], default='1', max_length=50),
        ),
    ]