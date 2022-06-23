# Generated by Django 3.2.13 on 2022-06-17 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import student_management.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student_management', '0005_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='アクティブ'),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='自習日')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='student_management.student', validators=[student_management.models.validate_student_is_active], verbose_name='生徒')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
            options={
                'unique_together': {('date', 'student')},
            },
        ),
    ]
