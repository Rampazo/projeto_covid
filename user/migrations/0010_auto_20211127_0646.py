# Generated by Django 3.2.9 on 2021-11-27 09:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0009_auto_20211119_0210'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userpassword',
            options={'verbose_name': 'Senha de Usuário', 'verbose_name_plural': 'Senha de Usuários'},
        ),
        migrations.AddField(
            model_name='userprofilefile',
            name='example_file',
            field=models.FileField(default='upload_example.xlsx', upload_to='', verbose_name='Arquivo Exemplo de Importação'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 27, 6, 46, 7, 64408), editable=False, verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 27, 6, 46, 7, 64447), editable=False, verbose_name='Data da Última Atualização'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_id',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('Estudante', 'Estudante'), ('Funcionario', 'Funcionario'), ('Gestor', 'Gestor'), ('Professor', 'Professor'), ('RH', 'Recursos Humanos')], max_length=20, verbose_name='Tipo de Usuário'),
        ),
        migrations.AlterField(
            model_name='userprofilefile',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 27, 6, 46, 7, 65719), verbose_name='Data de Criação'),
        ),
    ]
