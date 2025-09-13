import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

logger = logging.getLogger('api')
performance_logger = logging.getLogger('cache')


class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """Middleware for monitoring API performance and logging requests."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.api_logger = logging.getLogger('api')
        self.performance_logger = logging.getLogger('cache')

    def __call__(self, request):
        # Start timing
        start_time = time.time()

        # Log incoming request
        if self._is_api_request(request):
            self.api_logger.info(
                f"API Request: {request.method} {request.path} "
                f"from {self._get_client_ip(request)}"
            )

        # Process request
        response = self.get_response(request)

        # Calculate response time
        duration = time.time() - start_time

        # Log performance metrics
        if self._is_api_request(request):
            self._log_api_performance(request, response, duration)
        elif duration > 1.0:  # Log slow requests (> 1 second)
            self.performance_logger.warning(
                f"Slow request: {request.method} {request.path} "
                f"took {duration:.2f}s"
            )

        return response

    def _is_api_request(self, request):
        """Check if the request is to an API endpoint."""
        return (
            request.path.startswith('/api/') or
            'application/json' in request.META.get('HTTP_ACCEPT', '') or
            request.META.get('CONTENT_TYPE', '').startswith('application/json')
        )

    def _get_client_ip(self, request):
        """Get the client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def _log_api_performance(self, request, response, duration):
        """Log API performance metrics."""
        status_code = response.status_code
        method = request.method
        path = request.path
        user = getattr(request, 'user', None)
        user_id = user.id if user and user.is_authenticated else 'anonymous'

        # Determine log level based on response status
        if status_code >= 500:
            log_level = 'error'
            log_method = self.api_logger.error
        elif status_code >= 400:
            log_level = 'warning'
            log_method = self.api_logger.warning
        else:
            log_level = 'info'
            log_method = self.api_logger.info

        log_method(
            f"API Response: {method} {path} {status_code} "
            f"({duration:.3f}s) User: {user_id}"
        )

        # Log additional details for errors
        if status_code >= 400:
            self.api_logger.warning(
                f"Request details: {dict(request.GET)} {dict(request.POST) if request.POST else ''}"
            )


class CacheMonitoringMiddleware(MiddlewareMixin):
    """Middleware for monitoring cache performance."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.cache_logger = logging.getLogger('cache')

    def __call__(self, request):
        # Track cache hits/misses if available
        response = self.get_response(request)

        # Log cache headers if present
        cache_control = response.get('Cache-Control', '')
        if cache_control:
            self.cache_logger.debug(
                f"Cache-Control: {cache_control} for {request.path}"
            )

        return response


class SecurityMonitoringMiddleware(MiddlewareMixin):
    """Middleware for monitoring security-related events."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.security_logger = logging.getLogger('django.security')

    def __call__(self, request):
        # Monitor suspicious activities
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if self._is_suspicious_user_agent(user_agent):
            self.security_logger.warning(
                f"Suspicious User-Agent: {user_agent} from {self._get_client_ip(request)}"
            )

        # Monitor failed authentication attempts
        if hasattr(request, 'user') and not request.user.is_authenticated:
            if request.path in ['/accounts/login/', '/api/orders/']:
                self.security_logger.info(
                    f"Unauthenticated access attempt: {request.method} {request.path}"
                )

        response = self.get_response(request)
        return response

    def _is_suspicious_user_agent(self, user_agent):
        """Check for suspicious user agents."""
        suspicious_patterns = [
            'sqlmap',
            'nmap',
            'masscan',
            'dirbuster',
            'gobuster',
            'nikto',
            'acunetix',
            'openvas'
        ]
        return any(pattern.lower() in user_agent.lower() for pattern in suspicious_patterns)

    def _get_client_ip(self, request):
        """Get the client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RequestLoggingMiddleware(MiddlewareMixin):
    """Enhanced request logging middleware."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.request_logger = logging.getLogger('django.request')

    def __call__(self, request):
        # Log detailed request information
        self.request_logger.debug(
            f"Request: {request.method} {request.path} "
            f"User: {getattr(request, 'user', 'anonymous')} "
            f"IP: {self._get_client_ip(request)}"
        )

        response = self.get_response(request)

        # Log response information
        self.request_logger.debug(
            f"Response: {response.status_code} for {request.path}"
        )

        return response

    def _get_client_ip(self, request):
        """Get the client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip