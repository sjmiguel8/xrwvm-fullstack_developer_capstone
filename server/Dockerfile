FROM python:3.12.0-slim-bookworm

ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1
<<<<<<< HEAD
=======

>>>>>>> 5640e36cdccbbac143706c3b2726d6031e25c264
ENV APP=/app

WORKDIR $APP

<<<<<<< HEAD
# Install AWS CLI and dependencies
RUN apt-get update && apt-get install -y \
    awscli \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install AWS Amplify CLI
RUN curl -sL https://aws-amplify.github.io/amplify-cli/install | bash

=======
>>>>>>> 5640e36cdccbbac143706c3b2726d6031e25c264
# Install requirements
COPY requirements.txt $APP
RUN pip3 install -r requirements.txt

# Create directories first
RUN mkdir -p $APP/frontend/static
RUN mkdir -p $APP/djangoapp/templates

# Copy files
COPY . $APP

<<<<<<< HEAD
=======
# Verify index.html exists after copy
RUN ls -la $APP/frontend/static/index.html

>>>>>>> 5640e36cdccbbac143706c3b2726d6031e25c264
# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]
<<<<<<< HEAD
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"] 
=======
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"] 

# Create necessary directories
RUN mkdir -p $APP/frontend/static
RUN mkdir -p $APP/staticfiles

# Copy all files
COPY . $APP/

# Set permissions
RUN chmod +x /app/entrypoint.sh
RUN chown -R www-data:www-data $APP

# Collect static files during build
RUN python manage.py collectstatic --noinput 
>>>>>>> 5640e36cdccbbac143706c3b2726d6031e25c264
