BEGIN;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";


DROP TABLE IF EXISTS posts, tags, users;


CREATE TABLE users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

INSERT INTO users (name, email, password) VALUES
('Michel','michel@michel', crypt('password1', gen_salt('md5')));


CREATE TABLE tags (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL);


INSERT INTO tags (name) VALUES ('frontend'), ('backend'), ('devops');

CREATE TABLE posts (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author_id INT REFERENCES users(id) ON DELETE NO ACTION
);


INSERT INTO posts (title, content, author_id) VALUES
('Async IO in Python', 'Concurrency and parallelism are expansive subjects that are not easy to wade into. While this article focuses on async IO and its implementation in Python, it’s worth taking a minute to compare async IO to its counterparts in order to have context about how async IO fits into the larger, sometimes dizzying puzzle.', 1),
('Nginx', 'Nginx [engine x] is an HTTP and reverse proxy server, a mail proxy server, and a generic TCP/UDP proxy server, originally written by Igor Sysoev. For a long time, it has been running on many heavily loaded Russian sites including Yandex, Mail.Ru, VK, and Rambler. According to Netcraft, nginx served or proxied 22.50% busiest sites in October 2021. Here are some of the success stories: Dropbox, Netflix, Wordpress.com, FastMail.FM. ', 1);




CREATE TABLE posts_tags (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INT REFERENCES tags(id) ON DELETE CASCADE
);

INSERT INTO posts_tags (post_id, tag_id) VALUES
(1, 2),
(2, 3);


COMMIT;