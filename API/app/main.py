import asyncio
import os

from fastapi import FastAPI, Request
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import prometheus_client
from time import time
from starlette.responses import HTMLResponse

import uvicorn
from custom_exception import CustomException
from prometheus_metrics import EXCEPTION_COUNT, REQUEST_COUNT, REQUEST_IN_PROGRESS, REQUEST_RESPOND_TIME


sentry_sdk.init(dsn="https://04af687c23f14f05a43b45bfea40fa7e@o1067007.ingest.sentry.io/6060283")

app = FastAPI()

asgi_app = SentryAsgiMiddleware(app)

prometheus_client.start_http_server(9001)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    """
    Custom handler allowing Prometheus metrics
    """
    EXCEPTION_COUNT.labels(exc.app_name, exc.endpoint).inc()
    return HTMLResponse(content="Custom Exception")


@app.get("/")
async def index():
    REQUEST_COUNT.labels('FastAPI', "root").inc()
    return {"message": "Hello, Numberly!"}


@REQUEST_IN_PROGRESS.track_inprogress()
@app.get("/expensive")
async def expensive_request():
    """
    Slow request simulating expensive computation
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
    Raises exception for testing Prometheus monitoring
    """
    raise CustomException(app_name="API", endpoint="exception endpoint")


@app.get("/crash")
async def crash():
    """
    Induces app crash for testing Sentry monitoring
    """
    return undefined_var


if __name__ == "__main__":
    port = os.getenv("PORT")
    uvicorn.run(app, host="0.0.0.0", port=port or 8000)