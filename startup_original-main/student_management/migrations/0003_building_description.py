# Generated by Django 4.0.3 on 2022-06-12 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management', '0002_building_dt'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='description',
            field=models.CharField(default='default test', max_length=500, verbose_name='備考'),
            preserve_default=False,
        ),
    ]
