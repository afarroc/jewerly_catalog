"""
Metrics and monitoring utilities for the jewelry catalog application.
"""
import time
import logging
from functools import wraps
from django.core.cache import cache
from django.conf import settings
from django.db import connection
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger('api')
performance_logger = logging.getLogger('cache')


class MetricsCollector:
    """Collect and track application metrics."""

    def __init__(self):
        self.metrics_cache_key = 'app_metrics'
        self.alerts_cache_key = 'alerts_log'

    def record_api_call(self, endpoint, method, status_code, duration, user_id=None):
        """Record API call metrics."""
        metrics = self._get_metrics()

        # Update counters
        metrics['api_calls']['total'] += 1
        metrics['api_calls']['by_endpoint'][endpoint] = metrics['api_calls']['by_endpoint'].get(endpoint, 0) + 1
        metrics['api_calls']['by_method'][method] = metrics['api_calls']['by_method'].get(method, 0) + 1
        metrics['api_calls']['by_status'][status_code] = metrics['api_calls']['by_status'].get(status_code, 0) + 1

        # Update response times
        if endpoint not in metrics['response_times']:
            metrics['response_times'][endpoint] = []
        metrics['response_times'][endpoint].append(duration)

        # Keep only last 100 response times per endpoint
        if len(metrics['response_times'][endpoint]) > 100:
            metrics['response_times'][endpoint] = metrics['response_times'][endpoint][-100:]

        # Update user activity
        if user_id and user_id != 'anonymous':
            metrics['active_users'][user_id] = timezone.now().isoformat()

        self._save_metrics(metrics)

        # Check for alerts
        self._check_alerts(metrics, endpoint, status_code, duration)

    def record_cache_hit(self, cache_key):
        """Record cache hit."""
        metrics = self._get_metrics()
        metrics['cache']['hits'] += 1
        self._save_metrics(metrics)

    def record_cache_miss(self, cache_key):
        """Record cache miss."""
        metrics = self._get_metrics()
        metrics['cache']['misses'] += 1
        self._save_metrics(metrics)

    def record_database_query(self, query_type, table, duration):
        """Record database query metrics."""
        metrics = self._get_metrics()

        if query_type not in metrics['database']['queries']:
            metrics['database']['queries'][query_type] = {}

        metrics['database']['queries'][query_type][table] = (
            metrics['database']['queries'][query_type].get(table, 0) + 1
        )

        if duration > 0.1:  # Log slow queries
            performance_logger.warning(
                f"Slow database query: {query_type} on {table} took {duration:.3f}s"
            )

        self._save_metrics(metrics)

    def get_metrics_summary(self):
        """Get a summary of current metrics."""
        metrics = self._get_metrics()

        summary = {
            'total_api_calls': metrics['api_calls']['total'],
            'cache_hit_rate': self._calculate_cache_hit_rate(metrics),
            'avg_response_time': self._calculate_avg_response_time(metrics),
            'active_users': len(metrics['active_users']),
            'error_rate': self._calculate_error_rate(metrics),
            'top_endpoints': self._get_top_endpoints(metrics),
        }

        return summary

    def _get_metrics(self):
        """Get current metrics from cache."""
        metrics = cache.get(self.metrics_cache_key)
        if metrics is None:
            metrics = self._initialize_metrics()
        return metrics

    def _save_metrics(self, metrics):
        """Save metrics to cache."""
        cache.set(self.metrics_cache_key, metrics, 3600)  # Cache for 1 hour

    def _initialize_metrics(self):
        """Initialize empty metrics structure."""
        return {
            'api_calls': {
                'total': 0,
                'by_endpoint': {},
                'by_method': {},
                'by_status': {},
            },
            'response_times': {},
            'cache': {
                'hits': 0,
                'misses': 0,
            },
            'database': {
                'queries': {},
            },
            'active_users': {},
            'alerts': [],
        }

    def _calculate_cache_hit_rate(self, metrics):
        """Calculate cache hit rate."""
        total = metrics['cache']['hits'] + metrics['cache']['misses']
        if total == 0:
            return 0.0
        return (metrics['cache']['hits'] / total) * 100

    def _calculate_avg_response_time(self, metrics):
        """Calculate average response time across all endpoints."""
        all_times = []
        for times in metrics['response_times'].values():
            all_times.extend(times)

        if not all_times:
            return 0.0

        return sum(all_times) / len(all_times)

    def _calculate_error_rate(self, metrics):
        """Calculate API error rate."""
        total_calls = metrics['api_calls']['total']
        if total_calls == 0:
            return 0.0

        error_calls = sum(
            count for status, count in metrics['api_calls']['by_status'].items()
            if status >= 400
        )

        return (error_calls / total_calls) * 100

    def _get_top_endpoints(self, metrics, limit=5):
        """Get top accessed endpoints."""
        endpoints = metrics['api_calls']['by_endpoint']
        return sorted(endpoints.items(), key=lambda x: x[1], reverse=True)[:limit]

    def _check_alerts(self, metrics, endpoint, status_code, duration):
        """Check for alert conditions."""
        alerts = []

        # High error rate alert
        error_rate = self._calculate_error_rate(metrics)
        if error_rate > 10:  # More than 10% errors
            alerts.append({
                'type': 'high_error_rate',
                'message': f'High error rate: {error_rate:.1f}%',
                'severity': 'high',
                'timestamp': timezone.now().isoformat(),
            })

        # Slow response alert
        if duration > 5.0:  # Response took more than 5 seconds
            alerts.append({
                'type': 'slow_response',
                'message': f'Slow response on {endpoint}: {duration:.2f}s',
                'severity': 'medium',
                'timestamp': timezone.now().isoformat(),
            })

        # Low cache hit rate alert
        cache_hit_rate = self._calculate_cache_hit_rate(metrics)
        if cache_hit_rate < 50 and metrics['cache']['hits'] + metrics['cache']['misses'] > 100:
            alerts.append({
                'type': 'low_cache_hit_rate',
                'message': f'Low cache hit rate: {cache_hit_rate:.1f}%',
                'severity': 'medium',
                'timestamp': timezone.now().isoformat(),
            })

        # Log alerts
        for alert in alerts:
            logger.warning(f"ALERT: {alert['type']} - {alert['message']}")

        # Store alerts in cache
        if alerts:
            existing_alerts = cache.get(self.alerts_cache_key, [])
            existing_alerts.extend(alerts)
            # Keep only last 100 alerts
            if len(existing_alerts) > 100:
                existing_alerts = existing_alerts[-100:]
            cache.set(self.alerts_cache_key, existing_alerts, 86400)  # 24 hours


# Global metrics collector instance
metrics_collector = MetricsCollector()


def monitor_api_call(view_func=None, endpoint_name=None):
    """Decorator to monitor API calls."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()

            # Get request object
            request = None
            for arg in args:
                if hasattr(arg, 'method'):
                    request = arg
                    break

            try:
                result = func(*args, **kwargs)

                # Calculate duration
                duration = time.time() - start_time

                # Record metrics
                if request:
                    user_id = getattr(request.user, 'id', None) if hasattr(request, 'user') else None
                    endpoint = endpoint_name or request.path
                    method = request.method

                    # Get status code from response
                    status_code = 200
                    if hasattr(result, 'status_code'):
                        status_code = result.status_code

                    metrics_collector.record_api_call(
                        endpoint, method, status_code, duration, user_id
                    )

                return result

            except Exception as e:
                duration = time.time() - start_time
                if request:
                    metrics_collector.record_api_call(
                        request.path, request.method, 500, duration
                    )
                raise

        return wrapper

    if view_func:
        return decorator(view_func)
    return decorator


def monitor_database_queries():
    """Context manager to monitor database queries."""
    class QueryMonitor:
        def __enter__(self):
            self.start_queries = len(connection.queries)
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            end_queries = len(connection.queries)
            new_queries = connection.queries[self.start_queries:]

            for query in new_queries:
                # Extract table name and query type
                sql = query['sql'].upper()
                if 'SELECT' in sql:
                    query_type = 'SELECT'
                elif 'INSERT' in sql:
                    query_type = 'INSERT'
                elif 'UPDATE' in sql:
                    query_type = 'UPDATE'
                elif 'DELETE' in sql:
                    query_type = 'DELETE'
                else:
                    query_type = 'OTHER'

                # Extract table name (simplified)
                table = 'unknown'
                if 'FROM' in sql:
                    from_part = sql.split('FROM')[1].split()[0].strip('`"')
                    table = from_part.split('.')[0] if '.' in from_part else from_part

                duration = float(query.get('time', 0))
                metrics_collector.record_database_query(query_type, table, duration)

    return QueryMonitor()


def get_system_health():
    """Get system health status."""
    try:
        # Check database connectivity
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        db_status = "healthy"

        # Check cache connectivity
        cache.set('health_check', 'ok', 10)
        cache_status = "healthy" if cache.get('health_check') == 'ok' else "unhealthy"

        # Get metrics summary
        metrics = metrics_collector.get_metrics_summary()

        return {
            'status': 'healthy',
            'database': db_status,
            'cache': cache_status,
            'metrics': metrics,
            'timestamp': timezone.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': timezone.now().isoformat(),
        }