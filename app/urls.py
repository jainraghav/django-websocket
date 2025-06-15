from django.urls import path, include
from .views import healthz
from .metrics import MetricsView

urlpatterns = [
    path('healthz/', healthz, name='healthz'),
    path('metrics/', MetricsView.as_view(), name='metrics'),
    path('chat/', include('app.chat.routing')),
]