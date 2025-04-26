FROM python:3.11-slim
WORKDIR /app
COPY ./app /app
COPY ./uploads /app/uploads  
COPY .env /app/.env
COPY requirements.txt /app/requirements.txt
ENV FLASK_CONFIG=/app/.env
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD python /app/create_db.py && python /app/main.py