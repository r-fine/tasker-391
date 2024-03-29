from django.http import HttpResponse, FileResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator
from django .views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from allauth.account.decorators import verified_email_required

from apps.orders.models import Order, OrderItem
from apps.accounts.models import LocalUser
from apps.accounts.forms import LocalUserForm
# from apps.accounts.decorators import allowed_users

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

import io
import datetime


def user_dashboard(request):

    return render(request, 'account/user/user-dashboard.html')


class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = LocalUser
    form_class = LocalUserForm
    template_name = "account/user/user-profile-form.html"
    success_message = 'Profile updated successfully'

    def get_queryset(self):
        qs = super(UserUpdateView, self).get_queryset()
        if self.request.user.is_superuser:
            return qs.all()
        return qs.filter(pk=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy('accounts:user_profile', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = LocalUser.objects.get(pk=self.request.user.id)
        return context


@verified_email_required
def order_history(request):
    order_list = Order.objects.prefetch_related('order_item__service').filter(
        user=request.user).order_by('-created_at')

    page_obj = request.GET.get('page', 1)

    paginator = Paginator(order_list, 3)

    try:
        orders = paginator.page(page_obj)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = {
        'orders': orders,
    }
    return render(request, 'order/order-history.html', context)


def cancel_order(request, op_id):
    op = OrderItem.objects.get(user=request.user, id=op_id)
    if op.status == 'Preparing':
        messages.error(request, mark_safe(
            'This order is already on progress. Please <a href="mailto:info@example.com">contact us<a> to cancel your order.'))
    else:
        op.status = 'Cancelled'
    op.save()

    return redirect('accounts:order_history')


def order_invoice(request, order_id):
    buffer = io.BytesIO()
    cnvs = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    text_object = cnvs.beginText()
    text_object.setTextOrigin(inch, inch)
    text_object.setFont('Helvetica', 14)

    order = None
    if request.user.is_staff:
        order = Order.objects.get(pk=order_id)
    else:
        order = Order.objects.get(user=request.user, pk=order_id)
    order_items = OrderItem.objects.filter(order=order)

    lines = [
        'Order No.#'+order.order_number,
        ' ',
        'Name: '+order.full_name,
        'Address: '+order.full_address,
        'Phone no. '+order.phone,
        'E-mail address: '+order.email,
        ' ', ' ',
        '             Services                                     Quantity                    Price',
        ' ',
    ]

    for i, item in enumerate(order_items):
        lines.append(str(i+1)+'. '+item.service.name)

    lines.append(
        '--------------------------------------------------------------------------------------------------------'
    )
    lines.append(
        '                                                                                 Total Bill:')
    lines.append(' ')
    lines.append(' ')
    lines.append(' ')
    lines.append('____________________')
    lines.append(
        'Date & Signature' + '                                                        Delivered on: ' +
        datetime.date.today().strftime('%b %d, %Y')
    )

    for line in lines:
        text_object.textLine(line)

    cnvs.drawText(text_object)
    cnvs.showPage()
    cnvs.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="Invoice_%s.pdf" % (order.order_number))
