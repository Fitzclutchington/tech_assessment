FROM python:3.10-slim

WORKDIR /vehicle-query

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "vehicle-query.app:app", "--host", "0.0.0.0", "--port", "8000"]
