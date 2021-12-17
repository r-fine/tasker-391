from django.urls import path
from .views import (
    HomeView,
    ServiceListView,
    service_list,
    ServiceSingleView,
    # submit_review,
)

app_name = 'services'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('all-service/', ServiceListView.as_view(), name='all_service'),
    path('<slug:slug>/', ServiceSingleView.as_view(), name='service_detail'),
    path(
        'services/<slug:service_slug>/', service_list, name='service_list'
    ),
    # path('submit_review/<int:service_id>/',
    #      submit_review, name='submit_review'),

]
