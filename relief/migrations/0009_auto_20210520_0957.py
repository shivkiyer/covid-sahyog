# Generated by Django 3.2.2 on 2021-05-20 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relief', '0008_auto_20210513_1549'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requesthelp',
            options={'ordering': ['-created_on']},
        ),
        migrations.AddField(
            model_name='requesthelp',
            name='volunteers',
            field=models.TextField(blank=True),
        ),
    ]
