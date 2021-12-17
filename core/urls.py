from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

import debug_toolbar

from apps.services.views import HomeView

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', HomeView.as_view()),
    path('auth/', include('allauth.urls')),
    path('account/', include('apps.accounts.urls', namespace='accounts')),
    path('service/', include('apps.services.urls', namespace='services')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('__debug__/', include(debug_toolbar.urls)),
    # path(r'^media/(?P<path>.*)$', serve,
    #      {'document_root': settings.MEDIA_ROOT}),
    # path(r'^static/(?P<path>.*)$', serve,
    #      {'document_root': settings.STATIC_ROOT}),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
