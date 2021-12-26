from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
# from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.generic.list import ListView

from apps.accounts.models import Staff, LocalUser
from apps.accounts.forms import StaffEditForm, LocalUserForm
from apps.accounts.decorators import staff_only, staff_required
from apps.orders.models import OrderItem


@staff_only
def staff_form(request, staff_id):
    staff = Staff.objects.get(pk=staff_id)
    user = LocalUser.objects.get(pk=staff.user_id)

    if request.method == 'POST':
        form = StaffEditForm(request.POST, request.FILES, instance=staff)
        userForm = LocalUserForm(request.POST, instance=user)
        if form.is_valid():
            # staff = form.save(commit=False)
            # staff.is_active = True
            staff.save()
            user.save()
            messages.success(request, 'Profile Updated')
            if request.user.is_superuser:
                return redirect('accounts:staff_table')
            return redirect('accounts:staff_dashboard')
        else:
            return HttpResponse('failed to submit')
    else:
        form = StaffEditForm(instance=staff)
        userForm = LocalUserForm(instance=user)
        try:
            activated = Staff.objects.get(user=request.user, is_active=True)
        except Staff.DoesNotExist:
            activated = None

        context = {
            'form': form,
            'userForm': userForm,
            'activated': activated,
            'staff': staff,
        }

        if request.user.is_superuser or staff.user.id == request.user.id:
            return render(request, 'account/staff/staff-form.html', context)
        else:
            raise Http404()


@staff_only
def staff_dashboard(request):
    staff = Staff.objects.get(user=request.user)
    tasks = OrderItem.objects.filter(assigned_staff__user=request.user)
    upcoming = tasks.filter(status='Accepted').count()
    ongoing = tasks.filter(status='Preparing').count()
    completed = tasks.filter(status='Completed').count()
    context = {
        'staff': staff,
        'upcoming': upcoming,
        'ongoing': ongoing,
        'completed': completed,
    }
    if staff.is_active:
        return render(request, 'account/staff/staff-homepage.html', context)
    else:
        return redirect('accounts:staff_form', staff.id)


@staff_required()
class AssignedTaskListView(ListView):
    model = OrderItem
    template_name = "account/staff/task-list.html"
    context_object_name = 'tasks'

    def get_queryset(self):
        return OrderItem.objects.select_related('order', 'service').filter(assigned_staff__user=self.request.user)
