"""
System monitoring and health check views.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_page
from .metrics import get_system_health, metrics_collector
import logging

logger = logging.getLogger('api')


@require_GET
@cache_page(60)  # Cache for 1 minute
def health_check(request):
    """
    Health check endpoint for monitoring system status.

    Returns system health information including:
    - Database connectivity
    - Cache status
    - API metrics summary
    - Overall system status
    """
    try:
        health_data = get_system_health()

        # Return appropriate HTTP status based on health
        status_code = 200 if health_data['status'] == 'healthy' else 503

        logger.info(f"Health check requested from {request.META.get('REMOTE_ADDR')} - Status: {health_data['status']}")

        return JsonResponse(health_data, status=status_code)

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'timestamp': health_data.get('timestamp') if 'health_data' in locals() else None
        }, status=500)


@require_GET
def metrics(request):
    """
    Detailed metrics endpoint for monitoring.

    Returns comprehensive metrics about:
    - API usage statistics
    - Cache performance
    - Database query metrics
    - User activity
    """
    try:
        # Check if user is staff/admin (basic security)
        if not (request.user.is_authenticated and request.user.is_staff):
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        metrics_summary = metrics_collector.get_metrics_summary()

        # Add additional system information
        metrics_summary.update({
            'server_info': {
                'django_version': '5.2.3',
                'python_version': '3.13',
                'debug_mode': getattr(request, '_get_raw_host', lambda: 'unknown')().startswith('localhost'),
            },
            'timestamp': metrics_summary.get('timestamp', None),
        })

        logger.info(f"Metrics requested by {request.user.username}")

        return JsonResponse(metrics_summary)

    except Exception as e:
        logger.error(f"Metrics endpoint failed: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@require_GET
def alerts(request):
    """
    Recent alerts endpoint.

    Returns recent system alerts and warnings.
    """
    try:
        # Check if user is staff/admin
        if not (request.user.is_authenticated and request.user.is_staff):
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        from django.core.cache import cache
        alerts = cache.get('alerts_log', [])

        # Return last 50 alerts
        recent_alerts = alerts[-50:] if len(alerts) > 50 else alerts

        logger.info(f"Alerts requested by {request.user.username} - {len(recent_alerts)} alerts returned")

        return JsonResponse({
            'alerts': recent_alerts,
            'total': len(alerts),
            'timestamp': recent_alerts[-1]['timestamp'] if recent_alerts else None
        })

    except Exception as e:
        logger.error(f"Alerts endpoint failed: {e}")
        return JsonResponse({'error': str(e)}, status=500)