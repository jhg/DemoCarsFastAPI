FROM python:3.14.2-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

USER nobody

CMD ["fastapi", "run", "app/main.py", "--proxy-headers"]
