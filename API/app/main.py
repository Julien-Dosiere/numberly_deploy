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
from custom_exceptions import RequestError, DBError
from prometheus_metrics import *

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


@app.exception_handler(RequestError)
async def custom_exception_handler(request: Request, exc: RequestError) -> HTMLResponse:
    """
    Custom handler allowing Prometheus metrics export
    """
    EXCEPTION_COUNT.labels(exc.app_name, exc.endpoint).inc()
    return HTMLResponse(content="This request returns only exceptions")



@app.exception_handler(DBError)
async def custom_exception_handler(request: Request, exc: DBError) -> HTMLResponse:
    """
    Custom handler dor DB connection errors
    """

    return HTMLResponse(content="Problems with database, check that DB is running and accessible")



@app.get("/")
async def index(request: Request) -> dict:
    REQUEST_COUNT.labels('FastAPI', "root").inc()
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


@app.get("/posts")
async def get_all_posts() -> list[Post]:
    """
    Returns all posts
    """
    start_time = time()
    data = await db_client.get_all_posts()
    time_taken = time() - start_time
    DB_WRITE_REQUEST_RESPOND_TIME.observe(time_taken)
    return data



@app.get("/posts/{post_id}")
async def get_one_post(post_id: int) -> Post:
    """
    Returns specified Id post
    """
    return await db_client.get_one_post(post_id)


@app.post("/posts")
async def create_post(post: Post) -> Post:
    """
    Creates new post sent in body and returned it with Id
    """
    start_time = time()
    created_post = await db_client.create_post(post)
    time_taken = time() - start_time
    DB_WRITE_REQUEST_RESPOND_TIME.observe(time_taken)
    return created_post


@app.delete("/posts/{post_id}")
async def create_post(post_id: int) -> dict:
    """
    Deletes specified Id Post and returns message
    """
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
    SLOW_REQUEST_RESPOND_TIME.observe(time_taken)
    return {"message": "expensive calculation completed"}


@app.get("/exception")
async def raise_exception():
    """
    Raises exception for testing Prometheus monitoring
    """
    raise RequestError(app_name="API", endpoint="exception endpoint")


@app.get("/crash")
async def crash():
    """
    Induces app crash for testing Sentry monitoring
    """
    return undefined_var


if __name__ == "__main__":
    port = os.getenv("PORT")
    uvicorn.run(app, host="0.0.0.0", port=port or 8000)
