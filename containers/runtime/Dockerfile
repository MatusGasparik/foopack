# Multi-platform runtime container for foopack packages
# Supports: linux/amd64, linux/arm64
FROM ghcr.io/prefix-dev/pixi:latest

# Set working directory
WORKDIR /app

# Copy pixi configuration
COPY pixi.toml ./

# Install foopack packages from prefix.dev using pixi
RUN pixi install && \
    rm -rf ~/.cache/rattler

# Run the demo task defined in pixi.toml
CMD ["pixi", "run", "demo"]
