FROM python:3.11.3
WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt --no-cache-dir
COPY . /code/

# ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "main:fastapi_app", "--host", "0.0.0.0", "--port", "80"]