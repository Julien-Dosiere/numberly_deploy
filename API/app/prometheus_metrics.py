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

SLOW_REQUEST_RESPOND_TIME = Summary('slow_request_latency_seconds', 'Slow request latency in seconds')
DB_READ_REQUEST_RESPOND_TIME = Summary('db_read_request_latency_seconds', 'db read request latency in seconds')
DB_WRITE_REQUEST_RESPOND_TIME = Summary('db_write_request_latency_seconds', 'db write request latency in seconds')
