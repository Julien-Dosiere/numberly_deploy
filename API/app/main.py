import asyncio
import os
from models import Post
from db_client import DB_Client
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




@app.on_event("startup")
async def startup():
    global db_client
    db_client = await DB_Client.get_instance()


@app.on_event("shutdown")
async def shutdown():
    await db_client.disconnect()


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException) -> HTMLResponse:
    """
    Custom handler allowing Prometheus metrics
    """
    EXCEPTION_COUNT.labels(exc.app_name, exc.endpoint).inc()
    return HTMLResponse(content="Custom Exception")


@app.get("/")
async def index(request: Request) -> dict:
    REQUEST_COUNT.labels('FastAPI', "root").inc()
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


@app.get("/posts/")
async def get_all_posts() -> list[Post]:
    return await db_client.get_all_posts()


@app.get("/posts/{post_id}")
async def get_one_post(post_id: int) -> Post:
    return await db_client.get_one_post(post_id)


@app.post("/posts/")
async def create_post(post: Post) -> Post:
    return await db_client.create_post(post)


@app.delete("/posts/{post_id}")
async def create_post(post_id: int) -> dict:
    is_deleted = await db_client.delete_post(post_id)
    message = f"Deletion successful" if is_deleted else "post not found"
    return {"message": message}


@REQUEST_IN_PROGRESS.track_inprogress()
@app.get("/expensive")
async def expensive_request() -> dict:
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
