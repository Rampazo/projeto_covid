import os
import openpyxl
import secrets
import string

from datetime import datetime
from django.contrib.auth.models import Group, User
from django.db import models
from pathlib import Path

from sector.models import Sector
from user.schema import UserProfileFileSchema


def create_password(size=6):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(size))


def get_group(user_type):

    if user_type in ['Estudante', 'Funcionario', 'Professor']:
        return Group.objects.get(name='simple_user')
    elif user_type == 'Gestor':
        return Group.objects.get(name='manager_user')
    elif user_type == 'RH':
        return Group.objects.get(name='hr_user')
    else:
        return False


class UserProfile(models.Model):

    USER_TYPE_CHOICES = [
        ('Estudante', 'Estudante'),
        ('Funcionario', 'Funcionario'),
        ('Gestor', 'Gestor'),
        ('Professor', 'Professor'),
        ('RH', 'Recursos Humanos')
    ]

    id_user = models.CharField(max_length=20, verbose_name='Identificação do Usuário')
    name = models.CharField(max_length=200, verbose_name='Nome')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário', null=True, blank=True, editable=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, verbose_name='Tipo de Usuário')
    sector_id = models.ForeignKey(Sector, on_delete=models.CASCADE, verbose_name='Setor')
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    city = models.CharField(max_length=50, verbose_name='Cidade')
    state = models.CharField(max_length=2, verbose_name='UF')
    create_at = models.DateTimeField(verbose_name="Data de Criação", default=datetime.now(), editable=False)
    update_at = models.DateTimeField(verbose_name="Data da Última Atualização", default=datetime.now(), editable=False)

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfil de Usuários'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        password = create_password()
        group = get_group(self.user_type)

        # Create User
        user = User(
            username=str(self.id_user),
            first_name=self.name,
            is_staff=True
        )
        user.set_password(password)
        user.save()

        group.user_set.add(user)

        # Create UserPassword
        user_password = UserPassword(
            user_id_id=user.id,
            password=password
        )
        user_password.save()

        self.user_id_id = user.id
        super(UserProfile, self).save(*args, **kwargs)


def create_filename(extension_file):
    return f'Upload_UserProfile_{datetime.now().strftime("%Y-%m-%d_%H%M%S")}.{extension_file}'


class UserProfileFile(models.Model):

    import_file = models.FileField(upload_to='uploads/', verbose_name='Arquivo de Importação')
    create_at = models.DateTimeField(verbose_name="Data de Criação", default=datetime.now())

    class Meta:
        verbose_name = 'Carregamento de Perfil de Usuário'
        verbose_name_plural = 'Carregamentos de Perfil de Usuário'

    def __str__(self):
        return self.get_filename()

    def save(self, *args, **kwargs):

        # Rename Import File
        self.import_file.name = create_filename(self.import_file.name.split('.')[1])

        super(UserProfileFile, self).save(*args, **kwargs)

        # Process Import File
        list_upfs = self.process_file(self.import_file.name)  # List of UserProfileFileSchema

        for upfs_obj in list_upfs:  # Create User and UserProfile
            sector = Sector.objects.get(initial__contains=upfs_obj.sector)
            user_profile = UserProfile(
                id_user=upfs_obj.username,
                name=upfs_obj.name,
                sector_id_id=sector.id,
                user_type=upfs_obj.user_type,
                birth_date=upfs_obj.birthdate,
                city=upfs_obj.city,
                state=upfs_obj.state
            )
            user_profile.save()

    def get_filename(self):
        return os.path.basename(self.import_file.name)

    def process_file(self, filename):

        list_rows = []

        # Get Import File
        xlsx_file = Path(filename)
        wb_obj = openpyxl.load_workbook(xlsx_file)
        sheet = wb_obj.active

        # Process
        for i, row in enumerate(sheet.iter_rows(values_only=True)):
            if i == 0:  # Skip title row
                continue
            else:
                list_rows.append(
                    UserProfileFileSchema(
                        username=row[0],
                        name=row[1],
                        user_type=row[2],
                        sector=row[3],
                        birthdate=row[4],
                        city=row[5],
                        state=row[6],
                    )
                )
        return list_rows


class UserPassword(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    password = models.CharField(max_length=200, verbose_name='Senha')

    class Meta:
        verbose_name = 'Senha de Usuário'
        verbose_name_plural = 'Senha de Usuários'

    def __str__(self):
        return self.user_id.first_name
