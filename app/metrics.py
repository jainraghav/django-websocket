from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import CollectorRegistry
from django.http import HttpResponse
from django.views import View

registry = CollectorRegistry()

total_messages = Counter(
    'chat_total_messages',
    'Total number of chat messages received',
    registry=registry
)
active_connections = Gauge(
    'chat_active_connections',
    'Current number of active websocket connections',
    registry=registry
)
error_count = Counter(
    'chat_error_count',
    'Total number of errors in ChatConsumer',
    registry=registry
)
last_shutdown = Gauge(
    'chat_last_shutdown_timestamp',
    'timestamp of last websocket disconnect',
    registry=registry
)


class MetricsView(View):
    def get(self, request, *args, **kwargs):
        data = generate_latest(registry)
        return HttpResponse(data, content_type=CONTENT_TYPE_LATEST)
