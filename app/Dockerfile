# Multi-platform Dockerfile for downstream application
# Supports: linux/amd64, linux/arm64
FROM ghcr.io/prefix-dev/pixi:latest

# Set working directory
WORKDIR /app

# Copy pixi configuration first for better Docker layer caching
COPY pixi.toml ./

# Install dependencies from prefix.dev using pixi
# This demonstrates consuming published packages, not local builds
RUN pixi install && \
    rm -rf ~/.cache/rattler

# Copy application source code
COPY src/ /app/src/

# Set up Python path to include src directory
ENV PYTHONPATH=/app/src:${PYTHONPATH}

# Verify packages are installed correctly
RUN pixi run python -c "import foopack_core, foopack_extras, foopack_ui; print('✓ All packages installed')"

# Expose port for Panel dashboard
EXPOSE 5006

# Run the dashboard (accessible from outside container)
CMD ["pixi", "run", "panel", "serve", "src/myapp/dashboard.py", "--address", "0.0.0.0", "--port", "5006", "--allow-websocket-origin", "*"]
