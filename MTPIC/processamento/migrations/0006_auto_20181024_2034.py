# Generated by Django 2.1.2 on 2018-10-24 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('processamento', '0005_auto_20181023_1913'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buscas',
            old_name='qtdAssuntos_proximidades_busca',
            new_name='euristicaProcessamento',
        ),
        migrations.RenameField(
            model_name='buscas',
            old_name='qtdTema_proximidades_busca',
            new_name='taxaAceitacao',
        ),
    ]
