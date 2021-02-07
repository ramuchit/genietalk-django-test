import calendar
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from .documents import ArticleDocument
from .serializers import ArticleDocumentSerializer


class DateConverter(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        now = datetime.now()
        if request.query_params.get('day'):
            weekday = {
                'MONDAY': calendar.MONDAY,
                'TUESDAY': calendar.TUESDAY,
                'WEDNESDAY': calendar.WEDNESDAY,
                'THURSDAY': calendar.THURSDAY,
                'FRIDAY': calendar.FRIDAY,
                'SATURDAY': calendar.SATURDAY,
                'SUNDAY': calendar.SUNDAY,
            }
            days = weekday.get(request.query_params.get('day').upper())
            if days > now.weekday():
                days = days
            else:
                days = now.weekday() - days
            output_date = now - timedelta(days=days)
            return Response({'day':output_date.strftime("%d/%m/%Y")}, status=200)
        else:
            return Response(now.strftime("%d/%m/%Y"), status=200)


class AutoComplete(APIView):
    @staticmethod
    def get(request):
        if request.query_params.get('q'):
            article_query = ArticleDocument.search().query("match", title=request.query_params.get('q'))[:5]
            query_set = article_query.to_queryset()
            return Response(ArticleDocumentSerializer(query_set, many=True).data, status=200)
        return Response([], status=200)


