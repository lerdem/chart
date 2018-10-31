from django.http import JsonResponse
from django.views.generic.list import BaseListView

from .models import RandomData


class GetDataList(BaseListView):
    queryset = RandomData.objects.all()[:1000]

    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        res = []
        for item in qs:
            res.append({
                'date': item.date,
                'value1': item.value1,
                'value2': item.value2,
            })
        return JsonResponse({'results': res})
