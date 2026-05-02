# 06 — LedFx Setup

Goal: Deploy LedFx in Docker, connected to QuinLED via Ethernet.

> `ledfx-config.yaml`, `docker-compose.yml`, and the systemd service were all written by cloud-init. This doc covers starting the container and configuring WLED in the web UI.

---

## Step 1: Start Container

```bash
sudo systemctl start ledfx
```

Or manually:

```bash
cd ~/TechnoLicht/docker
docker compose up -d
```

## Step 2: Verify Running

```bash
docker ps
```

Expected: `ledfx` container running.

Or via systemd:

```bash
sudo systemctl status ledfx
```

## Step 3: Access Web UI

From the DJ laptop connected to `TechnoLicht` WiFi:

```
http://ledfx.local
```

Or from the RPi itself:

```
http://localhost:8888
```

## Step 4: Initial Config (Web UI)

1. **Audio**: Settings → Audio → Select your USB sound card
2. **Device**: Settings → Devices → Add WLED Device
   - Name: `QuinLED`
   - IP Address: `192.168.100.100`
   - Port: `21324`
3. **Segments**: Define your 4 LED segments (10m each on outputs 0-3)
4. **Effects**: Choose and tune audio-reactive effects

Save configuration in the UI. It persists in `/home/pi/ledfx-config/` via Docker volume.

## Step 5: Auto-Start on Boot

Already enabled by cloud-init. Verify:

```bash
sudo systemctl is-enabled ledfx
```

Expected: `enabled`

---

## Where Are the Config Files?

Since everything was baked into `user-data`, these were written automatically:

| File | Location | What It Does |
|------|----------|--------------|
| LedFx config | `/home/pi/ledfx-config/config.yaml` | Pixel mapping, segments, WLED IP |
| Docker Compose | `/home/pi/TechnoLicht/docker/docker-compose.yml` | Container definition |
| Systemd service | `/etc/systemd/system/ledfx.service` | Auto-start on boot |

**To edit pixel counts or LED layout later:**
1. Edit `/home/pi/ledfx-config/config.yaml`
2. Restart: `sudo systemctl restart ledfx`

---

## Done

Proceed to `07-ups-hat.md`.
