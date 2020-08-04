from django.urls import path

from .views import Login, Register, logout_view, dashboard, UserList, UserAdd,UserEdit, ServerList, ServerAdd, AccountList, \
    AccountAdd

urlpatterns = [
    path('', Login.as_view()),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('user/', UserList.as_view(), name='user'),
    path('user/add/', UserAdd.as_view()),
    path('user/update/<slug:pk>/', UserEdit.as_view()),
    path('account/', AccountList.as_view(), name='account'),
    path('account/add/', AccountAdd.as_view()),
    path('server/', ServerList.as_view(), name='server'),
    path('server/add/', ServerAdd.as_view()),
]
