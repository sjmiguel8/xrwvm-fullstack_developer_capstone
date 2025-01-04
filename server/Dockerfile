FROM python:3.12.0-slim-bookworm

ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1

ENV APP=/app

WORKDIR $APP

# Install requirements
COPY requirements.txt $APP
RUN pip3 install -r requirements.txt

# Create directories first
RUN mkdir -p $APP/frontend/static
RUN mkdir -p $APP/djangoapp/templates

# Copy files
COPY . $APP

# Verify index.html exists after copy
RUN ls -la $APP/frontend/static/index.html

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"] 