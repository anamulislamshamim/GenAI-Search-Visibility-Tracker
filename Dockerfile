# Stage 1: Builder
FROM python:3.12-slim AS builder

# Prevent python from writing pyc files and force stdout/err to appear immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build tools for compiling dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Install dependencies into /install (a clean folder)
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Final Lightweight Image
FROM python:3.12-slim

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]