# Generated by Django 3.1.4 on 2020-12-24 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pccomponents', '0009_auto_20201224_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='type',
            field=models.CharField(default='', max_length=50),
        ),
    ]