from django.urls import path
from .views import (
    HomeView,
    ServiceListView,
    service_list,
    ServiceSingleView,
    search,
    delete_review,
)

app_name = 'services'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', search, name='search'),
    path('all-service/', ServiceListView.as_view(), name='all_service'),
    path('<slug:slug>/', ServiceSingleView.as_view(), name='service_detail'),
    path(
        '<slug:service_slug>/all', service_list, name='service_list'
    ),
    path('delete-review/<int:review_id>/', delete_review, name='delete_review')

]
