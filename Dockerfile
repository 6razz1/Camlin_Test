FROM python:3.12
WORKDIR /code/app
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

RUN cd /code/app

EXPOSE 8000
CMD ["fastapi", "run", "main.py", "--host" , "0.0.0.0", "--port", "8080"]
