#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
#
#COPY ./app/requirements.txt /app/requirements.txt
#
#RUN pip install -r /app/requirements.txt
#
#COPY ./app /app

FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code/app
#CMD ["uvicorn", "app.main:app", "--reload"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
