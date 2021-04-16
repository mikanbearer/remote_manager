from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import CustomUser, Organization
from .forms import CustomUserCreationForm, OrganizationForm
import re


# Create your views here.
class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class MainLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'main/login.html'


class MainLogoutView(LogoutView, LoginRequiredMixin):
    pass


class PasswordUpdateView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    model = CustomUser
    form_class = PasswordChangeForm
    template_name = 'main/password.html'
    success_message = 'Success!'

    def get_success_url(self):
        return reverse_lazy('profile')


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        # read websockify log
        logfile = open('log/websockify.log', 'r')
        log = logfile.readlines()
        logfile.close()
        if len(log) >= 30:
            log = log[-30:]
        conn_log = []
        for line in log:
            conn = re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4})\n', line)
            if conn:
                conn_log += [conn.group(1)]

        # read app novnc_console log
        user_logfile = open('log/user.log', 'r')
        user_log = user_logfile.readlines()
        user_logfile.close()

        user_list = []
        host_list = []

        for line in user_log:
            a = re.match(r'user\[(.+)\] .+connecting to:.+\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):\d+\]\n', line)
            user_list += [a.group(1)]
            host_list += [a.group(2)]

        user_count = []
        for user in set(user_list):
            user_count += [[user, user_list.count(user)]]

        host_count = []
        for host in set(host_list):
            host_count += [[host, host_list.count(host)]]

        if len(user_log) > 10:
            user_log = user_log[-10:]

        context = {'conn_log': conn_log, 'user_log': user_log, 'host_count': host_count, 'user_count': user_count}
        return render(request, 'main/dashboard.html', context)


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    queryset = CustomUser.objects.filter(is_superuser=False)
    template_name = 'main/user_list.html'

    def test_func(self):
        return self.request.user.is_staff


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, PassRequestToFormViewMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'main/user_form.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.is_staff


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, PassRequestToFormViewMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'main/user_form.html'

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return self.request.user.is_staff


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'main/user_detail.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.is_staff


class OrgListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Organization
    template_name = 'main/org_list.html'

    def test_func(self):
        return self.request.user.is_staff


class OrgCreateView(LoginRequiredMixin, UserPassesTestMixin, PassRequestToFormViewMixin, CreateView):
    form_class = OrganizationForm
    template_name = 'main/org_form.html'
    success_url = reverse_lazy('org_list')

    def test_func(self):
        return self.request.user.is_staff


class OrgUpdateView(LoginRequiredMixin, UserPassesTestMixin, PassRequestToFormViewMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'main/org_form.html'

    def get_success_url(self):
        return reverse_lazy('org_detail', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return self.request.user.is_staff


class OrgDetailView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Organization
    template_name = 'main/org_detail.html'
    success_url = reverse_lazy('org_list')

    def test_func(self):
        return self.request.user.is_staff
