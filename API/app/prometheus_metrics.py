from prometheus_client import Counter, Gauge, Summary


REQUEST_COUNT = Counter(
    'app_requests_count',
    'Http root request count',
    ['app_name', 'endpoint']
)

EXCEPTION_COUNT = Counter(
    'app_exception_count',
    'Http root request count',
    ['app_name', 'endpoint'],
)

REQUEST_IN_PROGRESS = Gauge(
    'expensive_requests_in_progress',
    'number of expensive requests in progress',
)

REQUEST_RESPOND_TIME = Summary('app_response_latency_seconds', 'Response latency in seconds')
