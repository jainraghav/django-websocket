import os
from django.http import JsonResponse
import logging
logger = logging.getLogger(__name__)

def healthz(request):
    logger.info('health check')
    return JsonResponse({
        "status": "ok",
        "color": os.environ.get("COLOR")
    })