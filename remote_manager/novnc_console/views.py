from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import View
from django.conf import settings
from .models import VNCSession
from .forms import VNCSessionForm
from secrets import token_hex
from datetime import datetime

# Create your views here.
class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class VNCListView(LoginRequiredMixin, ListView):
    queryset = VNCSession.objects.all()
    template_name = 'novnc_console/vnc_list.html'


class VNCCreateView(LoginRequiredMixin, UserPassesTestMixin, PassRequestToFormViewMixin, CreateView):
    form_class = VNCSessionForm
    template_name = 'novnc_console/vnc_form.html'
    success_url = reverse_lazy('vnc_list')
    def test_func(self):
        return self.request.user.is_staff

class VNCUpdateView(LoginRequiredMixin, UserPassesTestMixin, PassRequestToFormViewMixin, UpdateView):
    model = VNCSession
    form_class = VNCSessionForm
    template_name = 'novnc_console/vnc_form.html'
    def get_success_url(self):
        return reverse_lazy('vnc_detail', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return self.request.user.is_staff


class VNCDetailView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VNCSession
    template_name = 'novnc_console/vnc_detail.html'
    success_url = reverse_lazy('vnc_list')
    def test_func(self):
        return self.request.user.is_staff


class VNCConsoleView(LoginRequiredMixin, UserPassesTestMixin, View):
    def set_token(self, token):
        f = open('token/token.conf', 'w')
        f.write(token)
        f.close()

    def logging_user(self):
        param =  (self.request.user.username, datetime.now(), self.vnc.name, self.vnc.ip4_addr, self.vnc.vnc_port)
        message ='user[%s] %s connecting to:%s[%s:%s]\n' % param
        logfile = open('log/user.log', 'a')
        logfile.write(message)

    def get(self, request, *args, **kwargs):
        token = token_hex(16)
        proxy_ip, proxy_port = settings.WEBSOCKIFY
        vnc_ip = self.vnc.ip4_addr
        vnc_port = self.vnc.vnc_port
        password = self.vnc.password
        context = {'proxy_ip': proxy_ip, 'proxy_port': proxy_port, 'token': token, 'password': password}
        self.set_token('%s: %s:%i' % (token, vnc_ip, vnc_port))
        self.logging_user()
        return render(request, 'novnc_console/vnc_console.html', context)

    def test_func(self):
        self.vnc = VNCSession.objects.get(id=self.kwargs['pk'])
        return self.request.user.is_staff or self.request.user.organization in self.vnc.organizations.all()
