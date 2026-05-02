# 01 — Flash Raspberry Pi OS (Cloud-Init Method — Primary)

The recommended way to set up the TechnoLicht controller is to use **cloud-init**.  
You place two small text files on the boot partition before first power-on. The Pi configures itself automatically — no Imager GUI, no keyboard, no manual raspi-config.

---

## Prerequisites

- Raspberry Pi OS Lite (64-bit), Trixie or newer
- microSD card (16 GB+)
- Linux PC with `dd`, `wget`, `xzcat`, `mount`

---

## Step 1: Download the OS Image

```bash
cd ~/Downloads
wget https://downloads.raspberrypi.com/raspios_lite_arm64/images/raspios_lite_arm64-2026-04-21/2026-04-21-raspios-trixie-arm64-lite.img.xz
```

> Replace the URL with the latest release if needed.

---

## Step 2: Flash to SD Card

Identify your SD card device with `lsblk`. **Double-check — `/dev/sdc` in this example.**

```bash
lsblk
# Look for the 14–64 GB device with no partitions mounted
# In this guide: /dev/sdc
```

Write the image:

```bash
xzcat 2026-04-21-raspios-trixie-arm64-lite.img.xz | sudo dd of=/dev/sdc bs=4M status=progress conv=fsync
```

Wait for completion (~1–2 min).

---

## Step 3: Mount the Boot Partition

```bash
sudo mkdir -p /mnt/rpi-boot
sudo mount /dev/sdc1 /mnt/rpi-boot
```

---

## Step 4: Copy Cloud-Init Files

Copy the two files from this repository onto the boot partition:

```bash
# From the repo root
cp boot/user-data /mnt/rpi-boot/
cp boot/meta-data /mnt/rpi-boot/
```

These files tell the Pi how to configure itself on first boot:

| File | Purpose |
|------|---------|
| `user-data` | Full config: user, SSH, networking, packages, Docker, hotspot, audio, watchdog, zram |
| `meta-data` | Datasource metadata (instance-id, hostname) |

---

## Step 5: Eject and Boot

```bash
sync
sudo umount /mnt/rpi-boot
```

1. **Insert SD card** into the Raspberry Pi
2. **Connect ethernet cable** from Pi to the QuinLED brain (or to your router for first-boot internet if WiFi is unavailable)
3. **Connect USB audio interface** (if available — can be done later)
4. **Power on**

---

## Step 6: Wait for First-Boot Configuration

First boot takes **3–6 minutes** while cloud-init:
- Updates packages
- Installs Docker, `hostapd`, `dnsmasq`, `zram-tools`
- Configures static IPs on `eth0` and `wlan0`
- Sets up the WiFi AP
- Pulls the LedFx Docker image

The Pi has no display output — the green LED will blink during SD card activity, then go mostly solid when done.

---

## Step 7: Connect Your Laptop

1. Join the WiFi network: **SSID `TechnoLicht`** / Password `technolight123`
2. Open a browser and go to: **http://ledfx.local**  
   (or `http://192.168.50.1` if `.local` doesn't resolve)

> The Pi is now ready. QuinLED is reachable at `http://quinled.local` once configured.

---

## Step 8: SSH (Optional)

```bash
ssh pi@192.168.50.1
# Password: technolight123
```

---

## What's Configured Automatically

| Feature | Setting |
|---------|---------|
| User | `pi` / `technolight123` |
| Hostname | `technolight-pi` |
| `eth0` (QuinLED) | Static `192.168.100.10/24` |
| `wlan0` (AP) | Static `192.168.50.1/24`, SSID `TechnoLicht` |
| DNS aliases | `ledfx.local` → Pi, `quinled.local` → `192.168.100.100` |
| Hardware | `gpu_mem=16`, HDMI disabled, watchdog enabled |
| Audio | USB card as default ALSA device |
| Swap | zram (50% of RAM, `zstd`) |
| Docker | Installed, `pi` in `docker` group, LedFx image pulled |
| Journal | Capped at 100 MB |

---

## Troubleshooting First Boot

| Symptom | Fix |
|---------|-----|
| Can't see `TechnoLicht` WiFi | Wait longer (up to 5 min). Check `hostapd` status via serial console or re-flash. |
| `ledfx.local` doesn't resolve | Use IP `192.168.50.1`. Ensure your laptop accepted DHCP DNS server. |
| LedFx not running yet | Cloud-init pulled the image but did not start the container. See `05-docker.md` to compose up. |
| No internet on laptop via AP | **Expected** — this is an isolated network for show control, not a router to the internet. |

---

## Fallback Methods

If you prefer not to use cloud-init, see the archived methods below. They require manual post-boot configuration.

<details>
<summary><b>Method A: Raspberry Pi Imager (GUI)</b></summary>

1. Download Raspberry Pi Imager: https://www.raspberrypi.com/software/
2. Choose **Raspberry Pi OS Lite (64-bit)**
3. Click gear icon → set hostname `technolight-pi`, enable SSH, set username/password
4. Flash to SD card
5. Boot, then manually follow docs 02–09

</details>

<details>
<summary><b>Method B: Raw dd + Manual Config</b></summary>

Same as the primary method but without copying `user-data`/`meta-data`. After flashing:
1. Mount `/dev/sdc1`, `touch ssh`, create `userconf.txt` for password
2. Boot, then manually follow docs 02–09

</details>

---

## Done

Proceed to `05-docker.md` to start LedFx, or `09-verify.md` to run the full system check.
