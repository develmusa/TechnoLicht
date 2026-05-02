# 02 — First Boot Setup

> **Already done by cloud-init.** If you used the primary flashing method in `01-flash-os.md`, first boot happened automatically. Use this doc to verify the initial state.

---

## What Was Configured Automatically

- [x] System updated (`apt update && apt full-upgrade`)
- [x] Essentials installed: `git`, `i2c-tools`, `python3-pip`, `alsa-utils`, `vim`, `htop`
- [x] I2C enabled for UPS HAT
- [x] Hostname set to `technolight-pi`
- [x] User `pi` created with password `technolight123`
- [x] SSH enabled with password authentication
- [x] Docker installed and `pi` added to `docker` group
- [x] LedFx Docker image pre-pulled

---

## Verification Steps

### 1. SSH In

Join WiFi `TechnoLicht` / `technolight123` on your laptop, then:

```bash
ssh pi@192.168.50.1
# or
ssh pi@ledfx.local
# Password: technolight123
```

### 2. Check I2C (UPS HAT)

```bash
sudo i2cdetect -y 1
```

Expected: `42` in the output grid (UPS HAT address).

### 3. Check Docker

```bash
docker --version
docker compose version
docker images | grep ledfx
```

Expected: Docker installed, LedFx image present.

### 4. Check Audio Device

```bash
arecord -l
```

Expected: USB sound card listed (e.g., `card 1: Device [USB Audio Device]`).

> **Note:** `asound.conf` is already written, but ALSA capture volume is not set. You must run `alsamixer` (step 4 in `04-audio.md`) to set the capture volume to ~70–80%.

### 5. Reboot (Recommended)

```bash
sudo reboot
```

This ensures all first-boot services start cleanly on a subsequent boot.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Can't SSH | Wait longer — first boot can take 5 min. If still nothing, check serial console or re-flash. |
| `i2cdetect` not found | `sudo apt install i2c-tools` (should already be installed by cloud-init) |
| Docker not found | Cloud-init may not have finished. Check `sudo systemctl status cloud-init` |
| No USB sound card | Plug it in and re-run `arecord -l`. Try a different USB port. |

---

## Done

Proceed to `03-network.md` (verify), `04-audio.md` (set volume), or `06-ledfx.md` (start container).
