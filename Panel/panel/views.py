from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView

from .forms import PanelUserCreationForm, PanelUserModifyForm, AccountToUserForm
from .mixins import TableMixin, MultipleDeletionMixin, AdminRequiredMixin
from .models import Server, Account


# Create your views here.
@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'base.html')


class UserList(LoginRequiredMixin, AdminRequiredMixin, TableMixin,
               MultipleDeletionMixin, ListView):
    login_url = reverse_lazy('login')
    permission_denied_url = reverse_lazy('dashboard')
    template_name = 'panel/user.html'
    model = get_user_model()
    fields = ['username', 'email', 'accounts']


class UserAdd(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    permission_denied_url = reverse_lazy('dashboard')
    form_class = PanelUserCreationForm
    template_name = 'common_form.html'
    success_url = reverse_lazy('user')


class UserEdit(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    permission_denied_url = reverse_lazy('dashboard')
    template_name = 'panel/user_detail.html'

    def get_object(self, pk: int) -> None:
        self.object = get_user_model().objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            self.get_object(pk)
            user_accounts = Account.objects.filter(user=self.object)
            context.update(
                dict(object=self.object,
                     user_accounts=user_accounts,
                     user_modify_form=PanelUserModifyForm(prefix='user'),
                     account_to_user_form=AccountToUserForm(prefix='account')))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.get_object(kwargs.get('pk'))

        # account 表单
        account_to_user_form = AccountToUserForm(request.POST, prefix='account')
        if account_to_user_form.is_valid():
            add_accounts = account_to_user_form.cleaned_data.get(
                'add_accounts')
            for account_id in add_accounts:
                print(account_id)
                account = Account.objects.get(pk=int(account_id))
                print(account)
                account.user = self.object
                account.save()
        return redirect(request.path)


class ServerList(LoginRequiredMixin, TableMixin, MultipleDeletionMixin,
                 ListView):
    login_url = reverse_lazy('login')
    template_name = 'panel/server.html'
    model = Server
    fields = ['host', 'ip', 'accounts']


class ServerAdd(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Server
    fields = ['host', 'ip', 'auth_user', 'auth_secret']
    template_name = 'common_form.html'
    success_url = reverse_lazy('server')


class AccountList(LoginRequiredMixin, TableMixin, MultipleDeletionMixin,
                  ListView):
    login_url = reverse_lazy('login')
    template_name = 'panel/account.html'
    model = Account
    fields = ['server', 'port', 'secret']


class AccountAdd(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Account
    fields = ['server', 'port', 'secret']
    template_name = 'common_form.html'
    success_url = reverse_lazy('account')


class Login(TemplateView):
    template_name = 'panel/login.html'
    redirect_url = reverse_lazy('dashboard')

    def get_redirect_url(self, request):
        return request.GET.get('next') if request.GET.get(
            'next') else self.redirect_url

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = get_user_model().objects.get(email=email).username
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect(self.get_redirect_url(request))
        else:
            self.extra_context = {'msg': "username or password is incorrect"}
            return self.get(request)


def logout_view(request):
    logout(request)
    return redirect('/')


class Register(CreateView):
    template_name = 'panel/register.html'
    model = get_user_model()
    form_class = PanelUserCreationForm
    success_url = reverse_lazy('login')
