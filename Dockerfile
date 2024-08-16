FROM python:3.10-alpine

# Install system dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

WORKDIR /app

COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python3 manage.py collectstatic --noinput

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "windam_backend.asgi:application"]
