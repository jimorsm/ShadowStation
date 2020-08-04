from django.urls import path, include
from .views import AccountList, AccountDetail, UserList, UserDetail
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from rest_framework.permissions import AllowAny
schema_view = get_schema_view()

urlpatterns = [
    path('schema/', schema_view),
    path('accounts/', AccountList.as_view()),
    path('accounts/<int:pk>/', AccountDetail.as_view()),
    path('auth/', include('rest_framework.urls'))
    # path('users/', UserList.as_view()),
    # path('users/<int:pk>/', UserDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)