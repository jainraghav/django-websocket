import os
from django.http import JsonResponse
import logging
from .metrics import active_connections, last_shutdown

logger = logging.getLogger(__name__)

def healthz(request):
    logger.info('health check')
    return JsonResponse({
        "status": "ok",
        "color": os.environ.get("COLOR")
    })