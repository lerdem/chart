from collections import defaultdict
from datetime import datetime

from django.core.exceptions import ValidationError
from django.http import JsonResponse, Http404
from django.db import models
from django.views.generic.list import BaseListView

from .models import RandomData


STRPTIME_YMD = '%Y-%m-%d'
DEFAULT_MONTH_DIFFERENCE = 1
DEFAULT_TO_DATE = datetime.now()
DEFAULT_FROM_DATE = DEFAULT_TO_DATE.replace(month=DEFAULT_TO_DATE.month - DEFAULT_MONTH_DIFFERENCE)


class GetDataList(BaseListView):

    def _get_clean_or_default_date(self, val):
        if isinstance(val, datetime):
            return val
        if isinstance(val, str):
            try:
                val = datetime.strptime(val, STRPTIME_YMD)
            except ValueError:
                raise Http404('invalid date')
            return val

    def validate_date(self, query_params: dict):
        get_fields = {'from-date', 'to-date'}
        get_keys = {*query_params.keys()}

        if len(get_fields.intersection(get_keys)) == 1:
            raise Http404('has to be 2 or 0 keys')
        from_date_str_or_default = query_params.get('from-date', DEFAULT_FROM_DATE)
        to_date_str_or_default = query_params.get('to-date', DEFAULT_TO_DATE)

        from_date = self._get_clean_or_default_date(from_date_str_or_default)
        to_date = self._get_clean_or_default_date(to_date_str_or_default)

        if from_date > to_date:
            raise Http404('from-date has to be less than to-date ')

        return from_date, to_date

    def get_queryset(self):
        from_date, to_date = self.validate_date(self.request.GET)
        self._date_range = from_date, to_date
        return RandomData.objects.filter(created__range=(from_date, to_date))\
                                 .values('created__day')\
                                 .annotate(
                                     models.Avg('value1', output_field=models.IntegerField()),
                                     models.Avg('value2', output_field=models.IntegerField())
                                 )

    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        res = defaultdict(list)
        for item in qs:
            res['value1'].append(item['value1__avg'])
            res['value2'].append(item['value2__avg'])
            res['date'].append(item['created__day'])
        res['date_range'] = [date.strftime(STRPTIME_YMD) for date in self._date_range]

        return JsonResponse(res)
