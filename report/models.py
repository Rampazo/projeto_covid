import collections
import json

from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from health_condition.models import HealthCondition


def get_min_max_datetime_by_date(current_date):
    min_datetime = datetime(current_date.year, current_date.month, current_date.day, 00, 00, 00)
    max_datetime = datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59)

    return min_datetime, max_datetime


def get_percentage(total, part):
    return 0.00 if total == 0 or part == 0 else round(((part * 100) / total), 2)


class DailyQuantity(models.Model):

    initial_date = models.DateField(verbose_name='Data Inicial')
    end_date = models.DateField(verbose_name='Data Final')
    result_report = models.TextField(verbose_name='Resultado', null=True, blank=True)

    class Meta:
        verbose_name = 'Quantidade Diária'
        verbose_name_plural = 'Quantidades Diárias'

    def __str__(self):
        return f'{self.initial_date} - {self.end_date}'

    def set_result(self, x):
        self.result_report = json.dumps(x, indent=4, sort_keys=True)

    def get_result(self):
        return json.loads(self.result_report)

    def validate_date(self):
        return False if self.end_date < self.initial_date else True

    def clean(self):
        if not self.validate_date():
            raise ValidationError("Data Final deve ser maior ou igual a Data Inicial.")

    def save(self, *args, **kwargs):
        record_list = []
        current_date = self.initial_date

        while current_date <= self.end_date:

            min_datetime, max_datetime = get_min_max_datetime_by_date(current_date)

            dict_list = HealthCondition.objects.filter(create_at__range=[min_datetime, max_datetime]).values(
                'create_at', qty=models.Count('create_at'))

            data = {
                'data': str(current_date),
                'qtd': len(dict_list)
            }
            record_list.append(data)

            current_date = current_date + timedelta(days=1)

        self.set_result(record_list)
        super(DailyQuantity, self).save(*args, **kwargs)


class DailyQuantityBad(models.Model):

    initial_date = models.DateField(verbose_name='Data Inicial')
    end_date = models.DateField(verbose_name='Data Final')
    result_report = models.TextField(verbose_name='Resultado', null=True, blank=True)

    class Meta:
        verbose_name = 'Quantidade Diária "Não muito bem"'
        verbose_name_plural = 'Quantidades Diárias "Não muito bem"'

    def __str__(self):
        return f'{self.initial_date} - {self.end_date}'

    def set_result(self, x):
        self.result_report = json.dumps(x, indent=4, sort_keys=True)

    def get_result(self):
        return json.loads(self.result_report)

    def validate_date(self):
        return False if self.end_date < self.initial_date else True

    def clean(self):
        if not self.validate_date():
            raise ValidationError("Data Final deve ser maior ou igual a Data Inicial.")

    def save(self, *args, **kwargs):
        record_list = []
        current_date = self.initial_date

        while current_date <= self.end_date:
            min_datetime, max_datetime = get_min_max_datetime_by_date(current_date)

            dict_list = HealthCondition.objects.filter(create_at__range=[min_datetime, max_datetime]).values(
                'create_at', 'health_state', qty=models.Count('create_at'))

            bad_health_state = collections.Counter(e['health_state'] == 'NO' for e in dict_list).get(True)

            data = {
                'data': str(current_date),
                'qtd': 0 if not bad_health_state else bad_health_state,
                'porcentagem': get_percentage(len(dict_list), bad_health_state or 0)
            }
            record_list.append(data)

            current_date = current_date + timedelta(days=1)

        self.set_result(record_list)
        super(DailyQuantityBad, self).save(*args, **kwargs)


class DailyQuantityBySector(models.Model):

    initial_date = models.DateField(verbose_name='Data Inicial')
    end_date = models.DateField(verbose_name='Data Final')
    result_report = models.TextField(verbose_name='Resultado', null=True, blank=True)

    class Meta:
        verbose_name = 'Quantidade Diária por Setor'
        verbose_name_plural = 'Quantidades Diárias por Setor'

    def __str__(self):
        return f'{self.initial_date} - {self.end_date}'

    def set_result(self, x):
        self.result_report = json.dumps(x, indent=4, sort_keys=True)

    def get_result(self):
        return json.loads(self.result_report)

    def validate_date(self):
        return False if self.end_date < self.initial_date else True

    def clean(self):
        if not self.validate_date():
            raise ValidationError("Data Final deve ser maior ou igual a Data Inicial.")

    def save(self, *args, **kwargs):

        data = {}

        current_date = self.initial_date

        while current_date <= self.end_date:

            min_datetime, max_datetime = get_min_max_datetime_by_date(current_date)

            dict_list = HealthCondition.objects.filter(create_at__range=[min_datetime, max_datetime]).values(
                'user_id__sector_id__id', 'user_id__sector_id__initial', 'user_id__sector_id__name').annotate(
                qty=models.Count('user_id__sector_id__id'))

            for record in dict_list:
                sector_id = record.get('user_id__sector_id__id')
                if sector_id not in data:
                    data.update(
                        {
                            record.get('user_id__sector_id__id'):
                                {
                                    'nome': f"{record.get('user_id__sector_id__initial')} - {record.get('user_id__sector_id__name')}",
                                    'qtds': [
                                        {
                                            'data': str(current_date),
                                            'qtd': record.get('qty')
                                        }
                                    ]
                                }
                        }
                    )
                else:
                    data[sector_id]['qtds'].append({
                                            'data': str(current_date),
                                            'qtd': record.get('qty')
                                        })

            current_date = current_date + timedelta(days=1)

        self.set_result(data)
        super(DailyQuantityBySector, self).save(*args, **kwargs)


class DailyQuantityBadBySector(models.Model):

    initial_date = models.DateField(verbose_name='Data Inicial')
    end_date = models.DateField(verbose_name='Data Final')
    result_report = models.TextField(verbose_name='Resultado', null=True, blank=True)

    class Meta:
        verbose_name = 'Quantidade Diária "Não muito bem" por Setor'
        verbose_name_plural = 'Quantidades Diárias "Não muito bem" por Setor'

    def __str__(self):
        return f'{self.initial_date} - {self.end_date}'

    def set_result(self, x):
        self.result_report = json.dumps(x, indent=4, sort_keys=True)

    def get_result(self):
        return json.loads(self.result_report)

    def validate_date(self):
        return False if self.end_date < self.initial_date else True

    def clean(self):
        if not self.validate_date():
            raise ValidationError("Data Final deve ser maior ou igual a Data Inicial.")

    def save(self, *args, **kwargs):

        sector_id_list = []
        data = {}

        current_date = self.initial_date

        while current_date <= self.end_date:

            min_datetime, max_datetime = get_min_max_datetime_by_date(current_date)

            dict_list = HealthCondition.objects.filter(create_at__range=[min_datetime, max_datetime]).values(
                'user_id__sector_id__id', 'user_id__sector_id__initial', 'user_id__sector_id__name',
                'health_state').annotate(qty=models.Count('user_id__sector_id__id'))

            print(dict_list)

        #     for record in dict_list:
        #         sector_id = record.get('user_id__sector_id__id')
        #         if sector_id not in data:
        #             data.update(
        #                 {
        #                     record.get('user_id__sector_id__id'):
        #                         {
        #                             'nome': f"{record.get('user_id__sector_id__initial')} - {record.get('user_id__sector_id__name')}",
        #                             'qtds': [
        #                                 {
        #                                     'data': str(current_date),
        #                                     'qtd': record.get('qty')
        #                                 }
        #                             ]
        #                         }
        #                 }
        #             )
        #         else:
        #             data[sector_id]['qtds'].append({
        #                                     'data': str(current_date),
        #                                     'qtd': record.get('qty')
        #                                 })
        #
            current_date = current_date + timedelta(days=1)
        #
        # self.set_result(data)
        # super(DailyQuantityBadBySector, self).save(*args, **kwargs)


class PeopleQuantityBadLastFiveDays(models.Model):

    date_reference = models.DateField(verbose_name='Data Referência', default=now)
    result_report = models.TextField(verbose_name='Resultado', null=True, blank=True)

    class Meta:
        verbose_name = 'Quantidade de Pessoas "Não muito bem" nos Últimos 5 Dias'
        verbose_name_plural = 'Quantidades de Pessoas "Não muito bem" nos Últimos 5 Dias'

    def __str__(self):
        return str(self.date_reference)

    def set_result(self, x):
        self.result_report = json.dumps(x, indent=4, sort_keys=True)

    def get_result(self):
        return json.loads(self.result_report)

    def save(self, *args, **kwargs):

        current_date = self.date_reference - timedelta(days=6)

        min_datetime_current, max_datetime_current = get_min_max_datetime_by_date(current_date)
        min_datetime_reference, max_datetime_reference = get_min_max_datetime_by_date(self.date_reference)

        dict_list = HealthCondition.objects.filter(create_at__range=[min_datetime_current, max_datetime_reference],
                                                   health_state='NO').values('user_id').annotate(
            qty=models.Count('user_id'))

        self.set_result({'qtd': len(dict_list)})
        super(PeopleQuantityBadLastFiveDays, self).save(*args, **kwargs)
