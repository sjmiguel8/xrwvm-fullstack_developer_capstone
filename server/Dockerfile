FROM python:3.12.0-slim-bookworm

ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1
ENV APP=/app

WORKDIR $APP

# Install required packages and dependencies
RUN apt-get update && apt-get install -y \
    awscli \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install AWS Amplify CLI using npm
RUN npm install -g @aws-amplify/cli

# Install Python requirements
COPY requirements.txt $APP
RUN pip3 install -r requirements.txt

# Create directories first
RUN mkdir -p $APP/frontend/static
RUN mkdir -p $APP/djangoapp/templates
RUN mkdir -p $APP/staticfiles

# Copy all files
COPY . $APP/

# Set permissions
RUN chmod +x /app/entrypoint.sh
RUN chown -R www-data:www-data $APP

# Collect static files during build
RUN python manage.py collectstatic --noinput

ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
