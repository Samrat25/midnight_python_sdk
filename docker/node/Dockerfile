FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir aiohttp

# Copy server script
COPY server.py .

# Expose port
EXPOSE 9944

# Health check
HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:9944/health')"

# Run server
CMD ["python", "server.py"]
