# Generated by Django 3.1.4 on 2020-12-24 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pccomponents', '0010_storage_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storage',
            name='type',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
