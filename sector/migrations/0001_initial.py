# Generated by Django 3.2.9 on 2021-11-13 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('user_type', models.CharField(choices=[('STUDENT', 'Estudante'), ('TEACHER', 'Professor'), ('STAFF', 'Funcionario')], max_length=20, verbose_name='Tipo de Usuário')),
                ('active', models.BooleanField(default=True, verbose_name='Ativo')),
            ],
        ),
    ]