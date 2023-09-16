FROM python:slim


COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--reload", "--port=5000", "--host=0.0.0.0"]