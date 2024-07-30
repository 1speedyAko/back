# Generated by Django 5.0.6 on 2024-07-30 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum')], default=1, max_length=10),
        ),
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
