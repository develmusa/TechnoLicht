# 05 — Docker Setup

Goal: Install Docker CE and Docker Compose plugin.

## Step 1: Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh
```

## Step 2: Add User to Docker Group

```bash
sudo usermod -aG docker pi
```

Log out and back in (or `newgrp docker`) for this to take effect.

## Step 3: Verify

```bash
docker --version
docker compose version
```

Expected:
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

## Step 4: Test

```bash
docker run hello-world
```

## Done

Proceed to `06-ledfx.md`.
