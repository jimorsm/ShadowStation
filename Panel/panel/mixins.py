import json

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect
from django.views.generic.edit import DeletionMixin
from django import forms


class TableMixin:
    '''表格Mixin，
    fields：列表，元素为模型名（字符串），模型要显示的字段
    配合table.html模板使用
    '''
    fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('search'):
            query = Q()
            query.connector = 'OR'
            for key in self.fields:
                value = self.request.GET.get(key)
                if value:
                    query.children.append((key, value))
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        context['fields'] = self.fields
        context['table_titles'] = []
        for item in list(map(lambda x: self.model._meta.get_field(x), self.fields)):
            context['table_titles'].append(item.verbose_name) if hasattr(item, 'verbose_name') else context[
                'table_titles'].append(item.name)
        return context


class MultipleDeletionMixin(DeletionMixin):
    '''多个项目删除'''

    def delete(self, request, *args, **kwargs):
        item = request.POST.get('item')
        items = request.POST.get('items')
        if item:
            self.model.objects.get(pk=item).delete()
        if items:
            items = json.loads(items)
            for item in items:
                self.model.objects.get(pk=item).delete()
        return HttpResponseRedirect(self.success_url)


class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    permission_denied_url = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            if self.permission_denied_url:
                return HttpResponseRedirect(self.redirect_url)
            else:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)



