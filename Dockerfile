FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV HTTP_PORT=8085

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y iputils-ping git
RUN pip install --no-cache-dir -r requirements.txt

# Add logic to configure "safe.directory" exceptions for Git repositories
RUN find /repos/ -type d -name .git | while read repo; do \
  dir=$(dirname "$repo"); \
  git config --global --add safe.directory "$dir"; \
done

EXPOSE 8085

CMD ["python", "main.py"]
