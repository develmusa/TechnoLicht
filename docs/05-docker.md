# 05 — Docker Setup

> **Already done by cloud-init.** Docker is installed, the `pi` user is in the `docker` group, and the LedFx image is pre-pulled.

Use this doc to verify.

---

## Step 1: Verify Docker

```bash
docker --version
docker compose version
```

Expected:
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

## Step 2: Verify Docker Group

```bash
groups | grep docker
```

Expected: `docker` in the output.

> If no `docker`, log out and back in (or `newgrp docker`).

## Step 3: Verify LedFx Image

```bash
docker images | grep ledfx
```

Expected: `ledfx/ledfx` listed.

## Step 4: Test Docker

```bash
docker run hello-world
```

---

## Done

Proceed to `06-ledfx.md`.
