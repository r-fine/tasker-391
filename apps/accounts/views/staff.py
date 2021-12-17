from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
# from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.generic.list import ListView
from apps.accounts.models import Staff
from apps.accounts.forms import StaffEditForm
from apps.accounts.decorators import staff_only, staff_required
from apps.orders.models import OrderItem


@staff_only
def staff_form(request, staff_id):
    staff = Staff.objects.get(pk=staff_id)

    if request.method == 'POST':
        form = StaffEditForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            # staff = form.save(commit=False)
            # staff.is_active = True
            staff.save()
            messages.success(request, 'Saved')
            if request.user.is_superuser:
                return redirect('accounts:staff_table')
            return redirect('accounts:staff_dashboard')
        else:
            return HttpResponse('failed to submit')
    else:
        form = StaffEditForm(instance=staff)
        try:
            activated = Staff.objects.get(user=request.user, is_active=True)
        except Staff.DoesNotExist:
            activated = None
        context = {'form': form, 'activated': activated}

        if request.user.is_superuser or staff.user.id == request.user.id:
            return render(request, 'account/staff/staff-form.html', context)
        else:
            raise Http404()


@staff_only
def staff_dashboard(request):
    staff = Staff.objects.get(user=request.user)
    upcoming = OrderItem.objects.filter(
        assigned_staff__user=request.user, status='Accepted'
    ).count()
    ongoing = OrderItem.objects.filter(
        assigned_staff__user=request.user, status='Preparing'
    ).count()
    completed = OrderItem.objects.filter(
        assigned_staff__user=request.user, status='Completed'
    ).count()
    context = {
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
        return OrderItem.objects.filter(assigned_staff__user=self.request.user)
