"""Application logging module.
"""
import logging
from pyramid.events import ContextFound
from pyramid.events import subscriber


@subscriber(ContextFound)
def context_found(event):
    """Records incoming request without assets and health check.
    """
    request = event.request
    # quiet access to assets
    path = getattr(request, 'path', '')
    if not path.startswith('/assets') and not path == '/_ah/health':
        logger = logging.getLogger(__name__)
        route = getattr(request, 'matched_route', None)
        logger.info('%s %d %s %s %s %s',
                    request.method,
                    request.response.status_code,
                    request.path_qs,
                    route.name if route else '',
                    str(request.matchdict),
                    str(request.params))
