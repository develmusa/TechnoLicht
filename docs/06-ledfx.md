# 06 — LedFx Setup

Goal: Deploy LedFx in Docker, connected to QuinLED via Ethernet.

## Step 1: Copy Config

```bash
mkdir -p ~/ledfx-config
cp ~/TechnoLicht/config/ledfx-config.yaml ~/ledfx-config/config.yaml
```

## Step 2: Start Container

```bash
cd ~/TechnoLicht/docker
docker compose up -d
```

## Step 3: Verify Running

```bash
docker ps
```

Expected: `ledfx` container running.

## Step 4: Access Web UI

From a device on the same network:
```
http://192.168.100.10:8888
```

Or from the RPi itself:
```
http://localhost:8888
```

## Step 5: Initial Config (Web UI)

1. **Audio**: Settings → Audio → Select your USB sound card
2. **Device**: Settings → Devices → Add WLED Device
   - Name: `QuinLED`
   - IP Address: `192.168.100.100`
   - Port: `21324`
3. **Segments**: Define your 4 LED segments (10m each on outputs 0-3)
4. **Effects**: Choose and tune audio-reactive effects

Save configuration in the UI. It persists in the Docker volume.

## Step 6: Auto-Start on Boot

```bash
sudo cp ~/TechnoLicht/config/ledfx.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ledfx.service
sudo systemctl start ledfx.service
```

Verify:
```bash
sudo systemctl status ledfx
```

## Done

Proceed to `07-ups-hat.md`.
