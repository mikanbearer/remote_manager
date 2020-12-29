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
import os
from threading import Timer

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


class VNCPlaybackView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        name = VNCSession.objects.get(pk=pk).name
        record_root = 'media/record/' + pk
        record_by_user = {}
        for root, dirs, files in os.walk(record_root):
            for d in dirs:
                record_by_user[d] = []
        for user in record_by_user.keys():
            for root, dirs, files in os.walk(record_root + '/' + user):
                record_by_user[user] = files
        context = {'pk': pk, 'name': name, 'record_by_user': record_by_user}
        return render(request, 'novnc_console/vnc_playback.html', context)

    def test_func(self):
        return self.request.user.is_staff


class VNCConsoleView(LoginRequiredMixin, UserPassesTestMixin, View):
    def set_token(self, token):
        f = open('token/token.conf', 'a')
        f.write(token)
        f.close()

    def unset_token(self, token):
        f = open('token/token.conf', 'r')
        token_new = ''
        for line in f:
            if line != line:
                token += line
        f = open('token/token.conf', 'w')
        f.write(token_new)


    def logging_user(self):
        param = (self.request.user.username, datetime.now(), self.vnc.name, self.vnc.ip4_addr, self.vnc.vnc_display)
        message ='user[%s] %s connecting to:%s[%s:%s]\n' % param
        logfile = open('log/user.log', 'a')
        logfile.write(message)

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        token = token_hex(16)
        proxy_ip, proxy_port = settings.WEBSOCKIFY
        vnc_ip = self.vnc.ip4_addr
        vnc_port = 5900 + int(self.vnc.vnc_display)
        password = self.vnc.password
        context = {'pk': pk, 'proxy_ip': proxy_ip, 'proxy_port': proxy_port, 'token': token, 'password': password}
        token = '%s: %s:%i\n' % (token, vnc_ip, vnc_port)
        self.set_token(token)
        self.logging_user()
        Timer(10, self.unset_token, [token]).start()
        return render(request, 'novnc_console/vnc_console.html', context)

    def test_func(self):
        self.vnc = VNCSession.objects.get(id=self.kwargs['pk'])
        return self.request.user.is_staff or self.request.user.organization in self.vnc.organizations.all()


