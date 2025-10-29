# Downstream Application

This is a test application that demonstrates consuming the foopack packages (`foopack-core`, `foopack-extras`, `foopack-ui`) as dependencies.

## Purpose

In a real-world scenario, this would be a separate repository that:
- Depends on published foopack packages from prefix.dev
- Builds multi-platform Docker images for deployment
- Deploys to production VMs or container orchestration platforms

This directory simulates that downstream application within the same repository for testing the end-to-end deployment pipeline.

## Local Development

### Prerequisites
- [Pixi](https://pixi.sh) installed

### Running the application

```bash
# Verify packages are installed
pixi run check

# Run the CLI application
pixi run run

# Start the diagnostics dashboard (opens in browser)
pixi run dashboard
```

The diagnostics dashboard provides:
- 📊 Package version information (foopack packages and dependencies)
- 💻 System information (Python version, platform details)
- ✅ Import tests (verify all packages work correctly)

The dashboard runs on `http://localhost:5006` by default and auto-reloads on code changes.

## Docker Deployment

### Build multi-platform image locally

Build for both linux/amd64 (Linux VMs) and linux/arm64 (macOS ARM64):

```bash
# Using pixi task
pixi run docker-build

# Or directly with docker
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ghcr.io/matusgasparik/foopack-app:latest \
  .
```

### Push to GitHub Container Registry

Build and push the multi-platform image to ghcr.io:

```bash
# First, authenticate with GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u MatusGasparik --password-stdin

# Build and push using pixi task
pixi run docker-push

# Or directly with docker
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ghcr.io/matusgasparik/foopack-app:latest \
  --push \
  .
```

### Run the container

Run the dashboard locally (accessible at http://localhost:5006):

```bash
docker run --rm -p 5006:5006 ghcr.io/matusgasparik/foopack-app:latest
```

## How it works

1. **pixi.toml** declares dependencies on foopack packages with exact version pins and configures prefix.dev channels
2. **Dockerfile** uses the official pixi Docker image (`ghcr.io/prefix-dev/pixi:latest`)
3. **pixi install** automatically installs packages from prefix.dev during Docker build (not local builds)
4. **src/myapp/** contains the application code that imports and uses foopack packages
5. The application runs via `pixi run` to ensure proper environment activation

**Key advantage**: Using the pixi Docker image means no manual lock file conversion is needed—pixi.toml and pixi.lock are understood natively.

This demonstrates the full deployment scenario: packages are published to prefix.dev, consumed by a downstream application via pixi, and deployed as a multi-platform container.
