# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**This is a test/demo project** designed to validate end-to-end automated deployment workflows using Pixi, Docker, and GitHub Actions. While implemented as a single repository, it simulates a multi-repository deployment pipeline.

### Project Goal
Test the complete lifecycle from version bump to production deployment:
1. Version increase triggers builds
2. Conda packages published to prefix.dev
3. Docker images automatically built and pushed to ghcr.io
4. Downstream applications consume packages and deploy to VMs

### Package Structure
Foopack is a Python monorepo consisting of three packages managed with Pixi:
- `foopack-core`: Core utilities (dependencies: numpy, xarray)
- `foopack-extras`: Extensions built on core (dependencies: foopack-core, pandas)
- `foopack-ui`: UI helpers (dependencies: foopack-core, panel, bokeh)

All packages use `pixi-build-python` backend with `hatchling` for building. Packages are configured as `noarch` (pure Python).

## Architecture & Responsibilities

**IMPORTANT**: This project follows a **separation of concerns** pattern where package building and application deployment are independent responsibilities.

### foopack Repository Responsibilities
This repository is responsible for:
- ✅ Building conda packages (foopack-core, foopack-extras, foopack-ui)
- ✅ Publishing packages to prefix.dev with semantic versioning
- ✅ Testing packages work correctly
- ✅ Maintaining package compatibility and dependencies
- ❌ **NOT** responsible for building application Docker images
- ❌ **NOT** responsible for deploying applications to VMs

### Downstream Application Responsibilities
Applications consuming foopack packages (like `app/` in this repo) are responsible for:
- ✅ Declaring dependencies on specific foopack versions via `pixi.toml`
- ✅ Building Docker images that include:
  - Installed foopack packages from prefix.dev
  - Application code (dashboard, services, etc.)
- ✅ Pushing Docker images to ghcr.io
- ✅ Deploying containers to VMs
- ❌ **NOT** responsible for building foopack packages

### Why This Separation?

**Reusability**: Foopack packages are designed to be reused across multiple projects, not just this dashboard. Each downstream project can:
- Pin to specific versions (e.g., `foopack-core==0.2.0`)
- Upgrade independently
- Use only needed packages (not all three)

**Clean CI/CD Pipeline**:
```
foopack CI:  code changes → tests → build packages → prefix.dev
                                                         ↓
App CI:                                    install packages → add app code → Docker → ghcr.io → VM
```

**Deployment Target**: Docker containers deployed to VMs. Applications run as containers that pull from ghcr.io.

**Version Management**: Downstream apps control which foopack version to use, enabling:
- Gradual rollouts of new package versions
- Independent testing of package updates
- Rollback capability per application

### Testing Strategy

**Before Publishing to prefix.dev**:
- Run tests locally: `pixi run test-all`
- Build packages locally: `pixi run build-all` → `./output/`
- Test packages work in isolation

**After Publishing to prefix.dev**:
- Downstream apps update `pixi.toml` to new version
- Build Docker images: packages installed from prefix.dev
- Deploy to staging VMs, then production

## Package Management & Build System

This project uses **Pixi** (not pip/conda directly) for all package management and task execution. The monorepo workspace is defined in the root `pixi.toml`.

### Key Pixi concepts:
- Each package has both `pyproject.toml` (Python metadata) and `pixi.toml` (Pixi build config)
- Root workspace declares all three packages as path dependencies
- Two environments: `dev` (includes test deps) and `prod` (runtime only)
- All commands must be run via `pixi run <task>` or within a pixi shell

## Development Commands

### Testing
```bash
# Test individual packages (parallel with coverage)
pixi run test-core
pixi run test-extras
pixi run test-ui

# Test all packages
pixi run test-all
```

Tests use pytest with pytest-xdist for parallelization (`-n auto`) and pytest-cov for coverage reporting.

### Building
```bash
# Build individual packages to ./output
pixi run build-core
pixi run build-extras
pixi run build-ui

# Build all packages
pixi run build-all
```

Builds use `pixi build -vv` and output conda packages to `./output/` directory.

### Version Check
```bash
# Quick smoke test - imports all packages and prints versions
pixi run versions
```

## Architecture

### Repository Structure
```
packages/          # Foopack package monorepo
├── core/          # Foundation package (numpy, xarray)
├── extras/        # Depends on core + pandas
└── ui/            # Depends on core + panel/bokeh

app/               # Downstream application (simulates separate repo)
├── src/myapp/     # Application source using src layout
├── pixi.toml      # Consumes foopack packages from prefix.dev
└── Dockerfile     # Multi-platform image build

containers/
└── runtime/       # Alternative runtime container example
```

### Dependency Graph
- `foopack-core` has no internal dependencies
- `foopack-extras` depends on `foopack-core==0.1.0`
- `foopack-ui` depends on `foopack-core==0.1.0`
- All inter-package deps use exact version pinning (`==0.1.0`)

### Build System Details
- Uses Pixi's preview feature `pixi-build` for building conda packages
- Host dependencies (build-time): hatchling, uv
- Run dependencies defined in both `pyproject.toml` and `pixi.toml`
- Channels: `pixi-build-backends` and `conda-forge` via prefix.dev
- Platforms: linux-64, linux-aarch64, osx-arm64, osx-64

## CI/CD

The automation pipeline demonstrates version-triggered deployments: a version tag triggers package publishing to prefix.dev, which enables Docker images to consume the packages from the public conda channel.

### CI Workflow (.github/workflows/ci.yml)
Runs QA tasks `qa-core`, `qa-extras`, `qa-ui` on every PR and push to main. These tasks are referenced but not defined in the visible pixi.toml (likely defined per-package).

### Release Workflow (.github/workflows/release.yml)
**Core automation workflow** that publishes packages to prefix.dev:

**Triggers:**
- Git tags matching `v*` pattern (e.g., `v0.1.0`, `v0.2.0`)
- Manual workflow dispatch

**Process:**
1. Builds all three packages using `pixi build -vv` to `./output/`
2. Uploads `.conda` artifacts to prefix.dev using `rattler-build upload`
3. Uses OIDC authentication via GitHub Actions Trusted Publishers (no secrets required)

**Authentication:**
This repository is configured as a Trusted Publisher on prefix.dev for the "foopack" channel. The workflow uses OpenID Connect (OIDC) to authenticate automatically via GitHub's `id-token: write` permission. No API keys need to be configured in repository secrets.

**Workflow:** Create a version tag → push tag → packages automatically published to prefix.dev → downstream Docker builds can consume them.

### Publish Workflow (.github/workflows/publish.yml)
Builds multi-arch Docker runtime image (amd64, arm64) on main branch changes to `containers/runtime/`. Publishes to GitHub Container Registry at `ghcr.io`.

**Important:** The Docker image installs packages from prefix.dev, so ensure packages are published there first via the Release workflow.

### Publish App Workflow (.github/workflows/publish-app.yml)
Builds multi-arch Docker image for the downstream application (amd64, arm64) on main branch changes to `app/`. Publishes to GitHub Container Registry at `ghcr.io`.

**Triggers:**
- Push to main with changes in `app/` directory
- Manual workflow dispatch

**Important:** This workflow demonstrates building a downstream application that consumes foopack packages from prefix.dev. Ensure packages are published there first.

### Container Images
Both Docker containers (`app/` and `containers/runtime/`) use the official pixi Docker image (`ghcr.io/prefix-dev/pixi:latest`) as the base.

**Key advantages of using pixi in Docker:**
- Native support for pixi.toml and pixi.lock files (no lock file conversion needed)
- Automatic dependency resolution from configured channels
- Consistent tooling between local development and production
- Multi-platform builds supported natively

**Dockerfile pattern:**
1. Copy `pixi.toml` for dependency declaration
2. Run `pixi install` to create environment from prefix.dev
3. Copy application source code
4. Execute using `pixi run` commands

This demonstrates how downstream applications consume published packages from prefix.dev in production.

## Deployment Simulation

This repository simulates what would typically be a multi-repository workflow within a single codebase to validate the end-to-end deployment process.

### Real-World Scenario (Multi-Repo)
In production, this would span multiple repositories:
1. **Package repo** (this project): Develops and publishes packages to prefix.dev
2. **Application repo**: Consumes packages as dependencies
3. **Infrastructure repo**: Deploys applications to VMs/cloud infrastructure

### Simulation in This Repo
The `app/` directory represents a downstream application that:
- Consumes foopack packages as dependencies via pixi.toml
- Uses src layout with a proper Python application structure
- Installs packages from prefix.dev (not local builds) in production
- Includes a multi-platform Dockerfile for deployment testing

**Local development with the downstream app:**
```bash
cd app
pixi run check      # Verify all foopack packages are installed
pixi run run        # Run the CLI application
pixi run dashboard  # Start the diagnostics dashboard (web UI)
```

The diagnostics dashboard (`app/src/myapp/dashboard.py`) provides a Panel-based web interface showing:
- Package versions for all foopack packages and dependencies
- System information (Python version, platform details)
- Import tests to verify packages work correctly
- Real-time refresh capability

**Testing multi-platform Docker builds:**
```bash
# Build for current platform
docker build -t myapp:latest app/

# Build for multiple platforms (requires buildx)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myapp:latest \
  app/

# Run the container
docker run --rm myapp:latest
```

**Testing the full pipeline:**
1. Bump versions in package files
2. Create and push a version tag (e.g., `git tag v0.2.0 && git push origin v0.2.0`)
3. Release workflow publishes to prefix.dev
4. Update app/pixi.toml to use new version
5. Docker build consumes published packages from prefix.dev
6. Multi-platform image can be pushed to ghcr.io and deployed to VMs

This single-repo setup allows rapid iteration on the deployment automation without managing multiple repositories during development.

## Version Management

All packages are currently at version `0.1.0`. When bumping versions:
1. Update version in package's `pyproject.toml`
2. Update version in package's `pixi.toml`
3. Update exact version pins in dependent packages (`foopack-extras` and `foopack-ui` both pin `foopack-core==0.1.0`)
4. Create and push a git tag matching the version (e.g., `git tag v0.2.0 && git push origin v0.2.0`)
5. The Release workflow will automatically build and publish packages to prefix.dev

**Note:** Version bumps trigger the entire deployment pipeline, so coordinate changes across all three packages when publishing new releases.
- use `ruff` and the "lint" and "fmt" `pixi` tasks with some sane defaults. Store in `.ruff.toml` or whatever is typically used
- I create a public channel at prefix.dev and added the remote repo to "Trusted Publishes". The channel is called "foopack". In the `pixi.toml` of the donwstream app the channel URL should be "https://repo.prefix.dev/foopack"