from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.text import slugify

from django_tables2 import SingleTableView

from apps.accounts.models import LocalUser, Staff
# from apps.accounts.tables import StaffTable, ServiceTable, ServiceOptionTable, OrderTable
from apps.accounts.tables import *
from apps.accounts.decorators import admin_required, admin_only, staff_only
from apps.services.forms import ServiceCreationForm, ServiceOptionCreationForm
from apps.services.models import Service, ServiceOption
from apps.orders.models import Order, OrderItem
from apps.orders.forms import AdminOrderForm, AdminOrderItemForm

# class AdminRequiredMixin(UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.is_superuser


@admin_required()
class AdminDashboard(TemplateView):
    template_name = 'account/admin/admin-homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = OrderItem.objects.all()
        staffs = Staff.objects.all()
        context.update({
            'total_orders': orders.count(),
            'completed': orders.filter(status='Completed').count(),
            'pending': orders.filter(status='Pending', is_ordered=True).count(),
            'total_staffs': staffs.filter(is_active=True).count(),
            'staffs_approval_pending': staffs.filter(is_active=False).count(),
            'total_services': Service.objects.filter(level=1).count(),
        })
        return context


@admin_required()
class StaffTableView(SingleTableView):
    model = Staff
    table_class = StaffTable
    template_name = "account/admin/staff-list.html"
    # table_data = Staff.objects.all()
    # paginator_class = LazyPaginator
    table_pagination = {
        "per_page": 10
    }


@admin_only
def staff_delete(request, staff_id):
    staff = Staff.objects.get(pk=staff_id)
    user = LocalUser.objects.get(pk=staff.user_id)
    user.delete()

    return redirect('accounts:staff_table')


@admin_only
def staff_activate(request, staff_id):
    staff = Staff.objects.get(pk=staff_id)
    if staff.is_active:
        staff.is_active = False
    else:
        staff.is_active = True
    staff.save()

    return redirect('accounts:staff_table')


@admin_required()
class ServiceTableView(SingleTableView):
    model = Service
    table_class = ServiceTable
    template_name = "account/admin/service-list.html"
    table_pagination = {
        "per_page": 10
    }


@admin_required()
class ServiceCreateView(SuccessMessageMixin, CreateView):
    template_name = 'account/admin/create-service.html'
    form_class = ServiceCreationForm
    success_url = reverse_lazy('accounts:create_service')
    success_message = "A new service has been added"

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.name)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Add new Service"
        return context


@admin_only
def edit_service(request, service_id):
    service = Service.objects.get(pk=service_id)

    if request.method == 'POST':
        form = ServiceCreationForm(
            request.POST, request.FILES, instance=service)
        if form.is_valid():
            service.save()
            return redirect('accounts:service_table')
        else:
            return HttpResponse('failed to submit')
    else:
        form = ServiceCreationForm(instance=service)
        context = {
            'form': form,
            'form_name': 'Edit Service'
        }

        return render(request, 'account/admin/create-service.html', context)


@admin_only
def delete_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    service.delete()

    return redirect('accounts:service_table')


@admin_required()
class ServiceOptionTableView(SingleTableView):
    model = ServiceOption
    table_class = ServiceOptionTable
    template_name = "account/admin/service-option-list.html"
    table_pagination = {
        "per_page": 10
    }


@admin_required()
class ServiceOptionCreateView(SuccessMessageMixin, CreateView):
    template_name = 'account/admin/create-service-option.html'
    form_class = ServiceOptionCreationForm
    success_url = reverse_lazy('accounts:create_service_option')
    success_message = "A new service option has been added"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Add new Service Option"
        return context


@admin_only
def edit_service_option(request, service_option_id):
    service_option = ServiceOption.objects.get(pk=service_option_id)

    if request.method == 'POST':
        form = ServiceOptionCreationForm(
            request.POST, request.FILES, instance=service_option)
        if form.is_valid():
            service_option.save()
            return redirect('accounts:service_option_table')
        else:
            return HttpResponse('failed to submit')
    else:
        form = ServiceOptionCreationForm(instance=service_option)
        context = {
            'form': form,
            'form_name': 'Edit Sevice Option'
        }

        return render(request, 'account/admin/create-service-option.html', context)


@admin_only
def delete_service_option(request, service_option_id):
    service_option = ServiceOption.objects.get(pk=service_option_id)
    service_option.delete()

    return redirect('accounts:service_option_table')


@admin_required()
class OrderListView(ListView):
    model = Order
    template_name = 'account/admin/order-list.html'
    context_object_name = 'orders'
    queryset = Order.objects.prefetch_related(
        'order_item').all().order_by('-created_at')
    paginate_by = 10


@admin_required()
class OrderUpdateForm(SuccessMessageMixin, UpdateView):
    model = Order
    form_class = AdminOrderForm
    template_name = "account/admin/order-edit.html"
    success_url = reverse_lazy('accounts:order_list')
    success_message = 'Order has been updated.'


@admin_required()
class OrderItemUpdateForm(SuccessMessageMixin, UpdateView):
    model = OrderItem
    form_class = AdminOrderItemForm
    template_name = "account/admin/order-item-edit.html"
    success_url = reverse_lazy('accounts:order_list')
    success_message = 'Order has been updated.'

    def form_valid(self, form):
        if form.instance.status == 'Completed':
            form.instance.is_reviewable = True
        else:
            form.instance.is_reviewable = False

        return super().form_valid(form)


@admin_only
def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()

    return redirect('accounts:order_list')


@admin_only
def order_accepted(request, pk):
    order = OrderItem.objects.get(pk=pk)
    order.status = 'Accepted'
    order.is_reviewable = False
    order.save()

    return redirect('accounts:order_list')


@staff_only
def order_preparing(request, pk):
    order = OrderItem.objects.get(pk=pk)
    order.status = 'Preparing'
    order.is_reviewable = False
    order.save()

    if request.user.is_superuser:
        return redirect('accounts:order_list')
    else:
        return redirect('accounts:task_list')


@staff_only
def order_completed(request, pk):
    order = OrderItem.objects.get(pk=pk)
    order.status = 'Completed'
    order.is_reviewable = True
    order.save()

    if request.user.is_superuser:
        return redirect('accounts:order_list')
    else:
        return redirect('accounts:task_list')


@admin_only
def order_cancelled(request, pk):
    order = OrderItem.objects.get(pk=pk)
    order.status = 'Cancelled'
    order.is_reviewable = False
    order.save()

    return redirect('accounts:order_list')
