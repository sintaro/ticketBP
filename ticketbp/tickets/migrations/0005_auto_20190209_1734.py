# Generated by Django 2.1.3 on 2019-02-09 08:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0004_remove_answer_answer_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onayamiticket',
            name='bookmark_people',
        ),
        migrations.AddField(
            model_name='onayamiticket',
            name='bookmark_people',
            field=models.ManyToManyField(blank=True, null=True, related_name='onayami_people', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='bookmark_people',
        ),
        migrations.AddField(
            model_name='ticket',
            name='bookmark_people',
            field=models.ManyToManyField(blank=True, null=True, related_name='bookmark_people', to=settings.AUTH_USER_MODEL),
        ),
    ]
