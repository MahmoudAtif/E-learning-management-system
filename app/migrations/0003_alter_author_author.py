# Generated by Django 4.1.2 on 2022-12-02 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_author_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='author',
            field=models.ForeignKey(limit_choices_to={'is_instructor': True}, on_delete=django.db.models.deletion.CASCADE, related_name='author_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
