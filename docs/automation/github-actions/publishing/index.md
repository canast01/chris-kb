# GitHub Actions Publishing

## PyPI Publishing

Publish Python packages to PyPI using OIDC trusted publishing — no long-lived tokens required.

```yaml
# .github/workflows/publish-pypi.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  build:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install build && python -m build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  publish:
    needs: build
    runs-on: ubuntu-24.04
    environment: pypi
    permissions:
      id-token: write   # required for OIDC
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - uses: pypa/gh-action-pypi-publish@release/v1
```

## Docker Hub Publishing

```yaml
# .github/workflows/docker-publish.yml
name: Build and Push Docker Image

on:
  push:
    tags: ['v*.*.*']

jobs:
  docker:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: myorg/myapp
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## GitHub Packages (Container Registry)

```yaml
      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push to GHCR
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
```

## Release Workflows

Automate GitHub Release creation including changelog generation.

```yaml
name: Release

on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-24.04
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        id: changelog
        uses: orhun/git-cliff-action@v3
        with:
          config: cliff.toml
          args: --current --strip header

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body: ${{ steps.changelog.outputs.content }}
          files: dist/*
          draft: false
          prerelease: ${{ contains(github.ref, '-rc') || contains(github.ref, '-beta') }}
```

## Publishing Target Comparison

| Target | Auth method | Trigger | Key action |
|---|---|---|---|
| PyPI | OIDC trusted publishing | Release published | `pypa/gh-action-pypi-publish` |
| Docker Hub | Username + access token secret | Tag push | `docker/build-push-action` |
| GHCR | `GITHUB_TOKEN` (built-in) | Tag push | `docker/build-push-action` |
| GitHub Release | `GITHUB_TOKEN` with `contents: write` | Tag push | `softprops/action-gh-release` |
| npm | `NODE_AUTH_TOKEN` secret | Release published | `npm publish` in run step |
