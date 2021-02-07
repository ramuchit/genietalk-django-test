from django.urls import path
from .views import DateConverter, AutoComplete
from .stream_view import StreamView

urlpatterns = [
    path(r'dateconvertor/', DateConverter.as_view()),
    path(r'autocomplete/', AutoComplete.as_view()),
    path(r'stream/', StreamView.as_view())
]