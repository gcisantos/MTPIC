# Generated by Django 2.1.2 on 2018-11-18 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processamento', '0007_buscas_tipobusca'),
    ]

    operations = [
        migrations.AddField(
            model_name='buscas',
            name='idioma',
            field=models.TextField(blank=True, null=True),
        ),
    ]