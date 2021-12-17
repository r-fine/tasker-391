from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormView
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import *
from .forms import ReviewRatingForm

from apps.orders.models import Order, OrderItem


class HomeView(ListView):
    model = Service
    template_name = 'service/home.html'
    context_object_name = 'subservices'
    paginate_by = 4
    queryset = Service.objects.filter(level=1)


class ServiceListView(ListView):
    model = Service
    template_name = "service/service-list.html"


def service_list(request, service_slug=None):
    service = get_object_or_404(Service, slug=service_slug)
    subservices = Service.objects.filter(parent=service)
    return render(request, 'service/service_list.html', {'service': service, 'subservices': subservices})


class ServiceDetailView(DetailView):
    model = Service
    template_name = "service/service-detail.html"
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'service_options': ServiceOption.objects.filter(service=self.object),
            'ordered': OrderItem.objects.filter(user=self.request.user, service__in=ServiceOption.objects.filter(service=self.object), is_ordered=True, is_reviewable=True)
            if self.request.user.is_authenticated else None,
            'reviews': ReviewRating.objects.filter(
                service_id=self.object.id,
                status=True
            ),
            'is_reviewed': ReviewRating.objects.get(user=self.request.user, service=self.object)
            if (self.request.user.is_authenticated and ReviewRating.objects.filter(service_id=self.object.id, status=True).exists()) else None,
            'form': ReviewRatingForm(),
        })
        return context


class ReviewRatingFormView(LoginRequiredMixin, SuccessMessageMixin, SingleObjectMixin, FormView):
    template_name = "service/service-detail.html"
    model = Service
    success_message = 'Thank you! Your review has been submitted.'

    def get_form(self):
        try:
            reviews = ReviewRating.objects.get(
                user=self.request.user, service=self.object
            )
            return ReviewRatingForm(self.request.POST, instance=reviews)
        except ReviewRating.DoesNotExist:
            return ReviewRatingForm(self.request.POST)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('services:service_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.service = self.object
        form.instance = form.save()

        return super().form_valid(form)


class ServiceSingleView(View):

    def get(self, request, *args, **kwargs):
        view = ServiceDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ReviewRatingFormView.as_view()
        return view(request, *args, **kwargs)
