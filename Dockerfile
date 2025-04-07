FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy application files
COPY app.py ./
COPY entrypoint.sh /app/entrypoint.sh

# Install necessary tools
RUN apk add --no-cache mariadb-client postgresql-client

# Create a non-root user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Change ownership of the working directory
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set entrypoint and command
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
