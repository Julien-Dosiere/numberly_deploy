from __future__ import annotations

import os

import sqlalchemy
from pydantic.tools import parse_obj_as
import databases
from databases import Database
from models import *



class DB_Client:
    instance: Database = None
    DATABASE_URL = f"postgresql+psycopg2://postgres:postgres@{os.getenv('PSQL_ADDRESS')}:5432/postgres"
    # DATABASE_URL = "postgresql+psycopg2://numberly:numberly@localhost:5732/numberly"

    @staticmethod
    async def get_instance() -> DB_Client:
        if DB_Client.instance is None:
            try:
                database: Database = databases.Database(DB_Client.DATABASE_URL)
                await database.connect()
                DB_Client.instance = DB_Client(database)
            except Exception:
                print("connection to db failed")

        return DB_Client.instance

    def __init__(self, database: Database):
        self.database = database

        self.posts = sqlalchemy.Table(
            "posts",
            sqlalchemy.MetaData(),
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("title", sqlalchemy.String),
            sqlalchemy.Column("content", sqlalchemy.String),
            sqlalchemy.Column("author_id", sqlalchemy.Integer),
        )

    async def disconnect(self) -> None:
        await self.database.disconnect()

    async def get_all_posts(self) -> list[Post]:
        query = self.posts.select()
        data = await self.database.fetch_all(query=query)
        return parse_obj_as(list[Post], data)

    async def get_one_post(self, post_id: int) -> Post:
        query = self.posts.select().where(self.posts.c.id == post_id)
        data = await self.database.fetch_all(query=query)
        post = parse_obj_as(list[Post], data)[0]
        return post

    async def create_post(self, post: Post) -> Post:
        query = self.posts.insert(post.dict(exclude={'tags', 'id'})).returning(*self.posts.c)
        post.id = await self.database.execute(query)
        return post

    async def delete_post(self, post_id: int) -> bool:
        query = self.posts.delete().where(self.posts.c.id == post_id).returning(*self.posts.c)
        return await self.database.execute(query) is not None





