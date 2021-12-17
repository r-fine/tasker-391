from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


from apps.accounts.forms import RegisterStaffForm
from apps.accounts.decorators import unauthenticated_user


@unauthenticated_user()
class RegisterStaffView(SuccessMessageMixin, CreateView):
    template_name = 'account/staff/register-staff.html'
    form_class = RegisterStaffForm
    success_url = reverse_lazy('account_login')
    success_message = "Profile Created"

    def form_valid(self, form):
        form.instance.username = form.instance.email.split('@')[0]

        return super().form_valid(form)
