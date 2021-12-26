from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.text import slugify
from django.conf import settings
from django.core.mail import send_mail

from django_tables2 import SingleTableView

from apps.accounts.filters import StaffFilter
from apps.accounts.models import *
from apps.accounts.tables import *
from apps.accounts.decorators import admin_required, admin_only, staff_only
from apps.services.forms import ServiceCreationForm, ServiceOptionCreationForm
from apps.services.models import Service, ServiceOption
from apps.orders.models import Order, OrderItem
from apps.orders.forms import AdminOrderForm, AdminOrderItemForm
# from apps.orders.forms import OrderUpdateFormSet

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
    table_data = Staff.objects.prefetch_related('user', 'department').all()
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


@admin_only
def staff_schedule(request, staff_id):
    staff = Staff.objects.get(pk=staff_id)
    booked = StaffBookedDateTime.objects.filter(staff=staff)
    context = {
        'staff': staff,
        'booked': booked,
    }

    return render(request, 'account/admin/staff-schedule-single.html', context)


@admin_only
def staff_schedule_list(request):
    staffs = Staff.objects.select_related('user', 'department').prefetch_related(
        'booked_on__order_item', 'booked_on__order',
    ).all().order_by('department')
    myFilter = StaffFilter(request.GET, queryset=staffs)
    staffs = myFilter.qs
    context = {
        'staffs': staffs,
        'myFilter': myFilter,
    }

    return render(request, 'account/admin/staff-schedule-all.html', context)


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
    table_data = ServiceOption.objects.select_related('service').all()
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
    queryset = Order.objects.select_related('user').prefetch_related(
        'user', 'order_item', 'order_item__service', 'order_item__assigned_staff',
        'order_item__assigned_staff__department', 'order_item__assigned_staff__user',
    ).all().order_by('-created_at')
    paginate_by = 10


@admin_required()
class OrderUpdateForm(SuccessMessageMixin, UpdateView):
    model = Order
    form_class = AdminOrderForm
    template_name = "account/admin/order-edit.html"
    success_message = 'Order has been updated.'

    def get_success_url(self):
        return reverse('accounts:edit_order', args=[self.object.pk])

    def form_valid(self, form):
        obj = StaffBookedDateTime.objects.filter(order=self.object)
        for o in obj:
            o.date = form.instance.date
            o.time = form.instance.time
            o.save()

        return super().form_valid(form)


# @admin_required()
# class OrderUpdateFormSetView(SuccessMessageMixin, SingleObjectMixin, FormView):
#     model = Order
#     template_name = "account/admin/order-edit-formset.html"
#     success_message = "Changes were saved"

#     # def get_form_kwargs(self):
#     #     form_kwargs = super(OrderUpdateFormSetView, self).get_form_kwargs()
#     #     if 'pk' in self.kwargs:
#     #         form_kwargs['instance'] = Order.objects.get(
#     #             pk=int(self.kwargs['pk'])
#     #         )
#     #     return form_kwargs

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object(
#             queryset=Order.objects.filter(pk=self.kwargs['pk']))
#         return super().get(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object(
#             queryset=Order.objects.filter(pk=self.kwargs['pk']))
#         return super().post(request, *args, **kwargs)

#     def get_form(self):
#         formset = OrderUpdateFormSet(
#             queryset=OrderItem.objects.select_related('service').all(),
#             **self.get_form_kwargs(), instance=self.object
#         )
#         for form in formset:
#             form['user'].initial = self.object.user
#         return formset

#     def form_valid(self, form):
#         formset = self.get_form()

#         for form in formset:
#             form.save()
#             self.object.order_item.add(form.instance)

#         return HttpResponseRedirect(self.get_success_url())

#     def get_success_url(self):
#         return reverse('accounts:edit_order_formset', args=[self.object.pk])


@admin_required()
class OrderItemUpdateForm(SuccessMessageMixin, UpdateView):
    model = OrderItem
    # form_class = AdminOrderItemForm
    template_name = "account/admin/order-item-edit.html"
    success_message = 'Order has been updated.'

    def get_form(self, form_class=AdminOrderItemForm):
        form = form_class(**self.get_form_kwargs())
        form.fields['assigned_staff'].queryset = Staff.objects.filter(
            department=self.object.service.service
        )
        return form

    def get_success_url(self):
        return reverse_lazy('accounts:edit_order_item', args=[self.object.pk])

    def form_valid(self, form):
        if form.instance.status == 'Completed':
            form.instance.is_reviewable = True
        else:
            form.instance.is_reviewable = False

        form.save()

        booked = StaffBookedDateTime(
            order=form.instance.order,
            order_item=form.instance,
            staff=form.instance.assigned_staff,
            date=form.instance.order.date,
            time=form.instance.order.time
        )
        booked.save(force_insert=True)

        previous_books = StaffBookedDateTime.objects.filter(
            order=form.instance.order, order_item=form.instance
        ).exclude(staff=form.instance.assigned_staff)

        for obj in previous_books:
            obj.delete()

        form.instance.assigned_staff.booked_on.add(booked)

        return super().form_valid(form)


@ admin_only
def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()

    return redirect('accounts:order_list')


@ admin_only
def order_accepted(request, pk):
    order = OrderItem.objects.get(pk=pk)
    order.status = 'Accepted'
    order.is_reviewable = False
    order.save()

    return redirect('accounts:order_list')


@ staff_only
def order_preparing(request, pk):
    order = OrderItem.objects.get(pk=pk)
    order.status = 'Preparing'
    order.is_reviewable = False
    order.save()

    if request.user.is_superuser:
        return redirect('accounts:order_list')
    else:
        return redirect('accounts:task_list')


@ staff_only
def order_completed(request, pk):
    order = OrderItem.objects.get(pk=pk)
    order.status = 'Completed'
    order.is_reviewable = True
    order.save()

    email_to = order.user.email
    subject = "Order #{0} update".format(order.order.order_number)
    message = "Your task {0} has been completed".format(order)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email_to, ])

    if request.user.is_superuser:
        return redirect('accounts:order_list')
    else:
        return redirect('accounts:task_list')


@ admin_only
def order_cancelled(request, pk):
    order = OrderItem.objects.get(pk=pk)
    order.status = 'Cancelled'
    order.is_reviewable = False
    order.save()

    return redirect('accounts:order_list')
