import asyncio
from fastapi import FastAPI, Request
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from prometheus_client import start_http_server, Counter, Gauge, Summary
from time import time
from starlette.responses import HTMLResponse



sentry_sdk.init(dsn="https://04af687c23f14f05a43b45bfea40fa7e@o1067007.ingest.sentry.io/6060283")

app = FastAPI()

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


asgi_app = SentryAsgiMiddleware(app)

start_http_server(9001)


class CustomException(Exception):
    def __init__(self, app: str, endpoint: str, ):
        self.endpoint = endpoint
        self.app = app


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    EXCEPTION_COUNT.labels(exc.app, exc.endpoint).inc()
    return HTMLResponse(content="Custom Exception")


@app.get("/")
async def index():
    REQUEST_COUNT.labels('FastAPI', "root").inc()
    return {"message": "Hello, Numberly!"}


@REQUEST_IN_PROGRESS.track_inprogress()
@app.get("/expensive")
async def expensive_request():
    """
    Slow request that can be tracked in Prometheus
    """
    start_time = time()
    print("expensive calculation running....")
    await asyncio.sleep(6)
    print("expensive calculation finished")
    time_taken = time() - start_time
    REQUEST_RESPOND_TIME.observe(time_taken)
    return {"message": "expensive calculation completed"}



@app.get("/exception")
async def raise_exception():
    """
    Raises exception for testing purposes
    """
    raise CustomException(app="API", endpoint="exception endpoint")


@app.get("/crash")
async def crash():
    """
    Induces app crash for testing purposes
    """
    return undefined_var