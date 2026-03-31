FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir aiohttp websockets

# Copy server script
COPY server.py .

# Expose port
EXPOSE 8088

# Health check
HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8088/health')"

# Run server
CMD ["python", "server.py"]
