from django.urls import path
from .views.auth import RegisterStaffView
from .views.user import (
    user_dashboard,
    UserUpdateView,
    order_history,
    cancel_order,
    order_invoice,
)
from .views.admin import (
    AdminDashboard,
    StaffTableView, staff_activate, staff_delete, staff_schedule, staff_schedule_list,
    ServiceTableView, ServiceCreateView, edit_service, delete_service,
    ServiceOptionTableView, ServiceOptionCreateView, edit_service_option, delete_service_option,
    OrderUpdateForm, OrderItemUpdateForm, OrderListView, delete_order,
    order_accepted, order_completed, order_cancelled, order_preparing,
    # OrderUpdateFormSetView,
)
from .views.staff import (
    staff_dashboard,
    staff_form,
    AssignedTaskListView,
)
app_name = 'accounts'

urlpatterns = [

    ######################### FOR USER #########################
    path('user/account-dashboard/', user_dashboard, name='user_dashboard'),
    path('user/user-profile/<int:pk>/',
         UserUpdateView.as_view(), name='user_profile'),
    path('user/order-history/', order_history, name='order_history'),
    path(
        'user/cancel-order/<int:op_id>/', cancel_order, name='cancel_order'
    ),
    path(
        'user/order-invoice/<int:order_id>/download/', order_invoice, name='order_invoice'
    ),

    ######################### FOR STAFF #########################
    path('staff/register-staff/', RegisterStaffView.as_view(), name='register_staff'),
    path('staff/staff-dashboard/',  staff_dashboard, name='staff_dashboard'),
    path('staff/staff-form/<int:staff_id>/', staff_form, name='staff_form'),
    path('staff/task-list/', AssignedTaskListView.as_view(), name='task_list'),

    ######################### FOR ADMIN #########################
    path("admin/admin-dashboard/", AdminDashboard.as_view(), name='admin_dashboard'),
    path("admin/staff-list/", StaffTableView.as_view(), name='staff_table'),
    path(
        'admin/staff-delete/<int:staff_id>/', staff_delete, name='staff_delete'
    ),
    path(
        'admin/staff-activate/<int:staff_id>/', staff_activate, name='staff_activate'
    ),
    path(
        'admin/staff-schedule/<int:staff_id>/', staff_schedule, name='staff_schedule_single'
    ),
    path(
        'admin/staff-schedule/all/', staff_schedule_list, name='staff_schedule_list'
    ),
    path(
        'admin/service/list/', ServiceTableView.as_view(), name='service_table'
    ),
    path('admin/service/add/', ServiceCreateView.as_view(), name='create_service'),
    path(
        'admin/service/edit/<int:service_id>/', edit_service, name='edit_service'
    ),
    path(
        'admin/service/delete/<int:service_id>/', delete_service, name='delete_service'
    ),
    path(
        'admin/service-option/list/', ServiceOptionTableView.as_view(), name='service_option_table'
    ),
    path(
        'admin/service-option/add/', ServiceOptionCreateView.as_view(), name='create_service_option'
    ),
    path(
        'admin/service-option/edit/<int:service_option_id>/', edit_service_option, name='edit_service_option'
    ),
    path(
        'admin/service-option/delete/<int:service_option_id>/', delete_service_option, name='delete_service_option'
    ),
    path(
        'admin/order/list/', OrderListView.as_view(), name='order_list'
    ),
    path(
        'admin/order/edit/<int:pk>/', OrderUpdateForm.as_view(), name='edit_order'
    ),
    # path(
    #     'admin/order/<int:pk>/items/edit/', OrderUpdateFormSetView.as_view(), name='edit_order_formset'
    # ),
    path(
        'admin/order-item/edit/<int:pk>/', OrderItemUpdateForm.as_view(), name='edit_order_item'
    ),
    path(
        'admin/order/delete/<int:order_id>/', delete_order, name='delete_order'
    ),
    path(
        'admin/order/set-accepted/<int:pk>/', order_accepted, name='order_accepted'
    ),
    path(
        'admin/order/set-preparing/<int:pk>/', order_preparing, name='order_preparing'
    ),
    path(
        'admin/order/set-completed/<int:pk>/', order_completed, name='order_completed'
    ),
    path(
        'admin/order/set-cancelled/<int:pk>/', order_cancelled, name='order_cancelled'
    ),
]
