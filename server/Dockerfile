FROM python:3.12.0-slim-bookworm

ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1
ENV APP=/app

WORKDIR $APP

# Install AWS CLI and dependencies
RUN apt-get update && apt-get install -y \
    awscli \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install AWS Amplify CLI
RUN curl -sL https://aws-amplify.github.io/amplify-cli/install | bash

# Install requirements
COPY requirements.txt $APP
RUN pip3 install -r requirements.txt

# Create directories first
RUN mkdir -p $APP/frontend/static
RUN mkdir -p $APP/djangoapp/templates

# Copy files
COPY . $APP

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"] 