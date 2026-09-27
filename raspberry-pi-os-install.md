# TechnoLichtPi — Install Manual

Raspberry Pi running LedFx with Waveshare UPS HAT, point-to-point Ethernet to a QuinLED-Dig-Octa.
Wi-Fi hotspot on the Pi for management; Ethernet for LED data.

OS: Raspberry Pi OS Lite (arm64, Trixie, 2026-04-21).

## Credentials & key addresses

⚠️ Keep this file private — passwords are in plain text.

| What | Value |
|---|---|
| Hostname | `TechnoLichtPi` (mDNS: `TechnoLichtPi.local`) |
| SSH login | `duser` / `powermorepower` |
| Wi-Fi hotspot SSID | `TechnoLichtPi-AP` |
| Wi-Fi hotspot password | `technolight123` |
| Hotspot subnet (Pi) | `192.168.50.1/24` |
| Eth P2P subnet (Pi) | `192.168.100.1/24` |
| QuinLED IP | `192.168.100.10` |
| LedFx web UI | `http://ledfx.lan` (on hotspot, see §11) · `http://192.168.50.1:8888` |
| WLED web UI | `http://wled.lan` (on hotspot, see §11) · `http://192.168.100.10` |

---

## 1. Flash the SD card

```bash
wget https://downloads.raspberrypi.com/raspios_lite_arm64/images/raspios_lite_arm64-2026-04-21/2026-04-21-raspios-trixie-arm64-lite.img.xz
lsblk                          # confirm the SD card device — assumed /dev/sdc below
xzcat 2026-04-21-raspios-trixie-arm64-lite.img.xz | sudo dd of=/dev/sdc bs=4M status=progress oflag=direct conv=fsync
```

⚠️ Wrong `of=` device will wipe that disk. Double-check with `lsblk`.

## 2. Preconfigure SSH and user on bootfs

```bash
sudo partprobe /dev/sdc
sudo mount /dev/sdc1 /mnt
sudo touch /mnt/ssh
echo "duser:$(openssl passwd -6 powermorepower)" | sudo tee /mnt/userconf.txt
sudo umount /mnt && sync
```

⚠️ Use **double quotes** around `"duser:$(...)"` so `openssl` runs. Single quotes write the literal `$(openssl …)`.

## 3. First boot + SSH

Insert SD, connect Ethernet (DHCP), power on. Wait ~60 s.

```bash
ssh duser@raspberrypi.local
```

## 4. Update and configure system

```bash
sudo apt update && sudo apt full-upgrade -y

sudo raspi-config nonint do_hostname TechnoLichtPi
sudo raspi-config nonint do_change_timezone Europe/Zurich
sudo raspi-config nonint do_change_locale en_US.UTF-8
sudo raspi-config nonint do_wifi_country CH
sudo raspi-config nonint do_ssh 0          # 0 = enable
sudo raspi-config nonint do_i2c 0          # for UPS HAT
sudo rfkill unblock wifi

sudo reboot
```

Reconnect: `ssh duser@TechnoLichtPi.local`.

## 5. Verify UPS HAT and install driver

```bash
sudo apt install -y i2c-tools p7zip-full python3-smbus
sudo i2cdetect -y 1            # expect device at 0x42 (INA219)

mkdir -p ~/ups-hat && cd ~/ups-hat
wget https://files.waveshare.com/upload/d/d9/UPS_HAT.7z
7zr x UPS_HAT.7z
cd UPS_HAT
python3 INA219.py              # prints voltage / current / power / SoC
```

⚠️ Power the system via the HAT's **8.4V barrel jack**, not the Pi's USB-C — otherwise the switchover to battery isn't seamless and SSH drops.

## 6. Wi-Fi hotspot for management (5 GHz)

⚠️ Keep home Ethernet plugged in until the hotspot is verified.

```bash
sudo nmcli device wifi hotspot \
  ifname wlan0 \
  ssid TechnoLichtPi-AP \
  password "technolight123"

# Force 5 GHz on a non-DFS channel (U-NII-1: 36/40/44/48)
sudo nmcli connection modify Hotspot 802-11-wireless.band a
sudo nmcli connection modify Hotspot 802-11-wireless.channel 36

# Custom subnet (default would be 10.42.0.1/24)
sudo nmcli connection modify Hotspot ipv4.addresses 192.168.50.1/24

# Persist across reboots
sudo nmcli connection modify Hotspot connection.autoconnect yes
sudo nmcli connection modify Hotspot connection.autoconnect-priority 100

sudo nmcli connection down Hotspot && sudo nmcli connection up Hotspot
```

**Disable Wi-Fi power-save** for lower-jitter management traffic:

```bash
sudo tee /etc/NetworkManager/conf.d/wifi-powersave-off.conf <<'EOF'
[connection]
wifi.powersave = 2
EOF
sudo systemctl restart NetworkManager
```

The Pi is at `192.168.50.1`. Connect a laptop to `TechnoLichtPi-AP`, then:

```bash
ssh duser@192.168.50.1
```

## 7. Ethernet point-to-point to QuinLED-Dig-Octa

Move the Eth cable from the home router to the QuinLED. The Pi runs a tiny DHCP server on `eth0` (NetworkManager `shared` mode) so the QuinLED stays on its factory config — no per-device WLED setup needed.

**Pi side (eth0):**

```bash
# See the current ethernet profile name (default: "Wired connection 1")
nmcli connection show

# Replace it with a shared (DHCP server) profile
sudo nmcli connection delete "Wired connection 1"
sudo nmcli connection add type ethernet \
  con-name QuinLED \
  ifname eth0 \
  ipv4.method shared \
  ipv4.addresses 192.168.100.1/24 \
  ipv6.method disabled \
  connection.autoconnect yes
sudo nmcli connection up QuinLED
```

**QuinLED side:** flash WLED via <https://install.quinled.info/dig-octa/>. In WLED → Config → WiFi Setup, leave Static IP at `0.0.0.0` (DHCP). Config → Sync Interfaces → Ethernet Type: `QuinLED-Dig-Octa`.

**Find the QuinLED's MAC** (one ping/visit is enough to populate the ARP table):

```bash
ip neigh show dev eth0
```

**Reserve a predictable IP** by MAC so the QuinLED always lands at `192.168.100.10`:

```bash
sudo mkdir -p /etc/NetworkManager/dnsmasq-shared.d
sudo tee /etc/NetworkManager/dnsmasq-shared.d/quinled.conf <<'EOF'
dhcp-host=AA:BB:CC:DD:EE:FF,192.168.100.10,quinled
EOF
sudo nmcli connection down QuinLED && sudo nmcli connection up QuinLED
```

(Replace `AA:BB:CC:DD:EE:FF` with the MAC from the previous step.) Power-cycle the QuinLED to grab the reserved lease.

**Verify from the Pi:**

```bash
ping -c3 192.168.100.10
```

**Make hotspot clients reach the QuinLED.** NM's `shared` mode enables forwarding but auto-rejects cross-interface traffic, and hotspot clients don't know `192.168.100.0/24` exists. Two fixes:

1. **Push the route via DHCP option 121** so clients learn it automatically:

```bash
sudo tee /etc/NetworkManager/dnsmasq-shared.d/route-quinled.conf <<'EOF'
dhcp-option=121,192.168.100.0/24,192.168.50.1
EOF
sudo nmcli connection down Hotspot && sudo nmcli connection up Hotspot
```

2. **Allow forwarding between wlan0 and eth0** in NM's nftables tables:

```bash
sudo nft insert rule ip nm-shared-eth0  filter_forward iifname "wlan0" oifname "eth0" accept
sudo nft insert rule ip nm-shared-wlan0 filter_forward iifname "eth0"  oifname "wlan0" accept
```

Persist via NM dispatcher script (re-applies on every interface up):

```bash
sudo tee /etc/NetworkManager/dispatcher.d/99-forward-hotspot-to-quinled <<'EOF'
#!/bin/sh
IFACE="$1"; ACTION="$2"
[ "$ACTION" = "up" ] || exit 0
case "$IFACE" in wlan0|eth0) ;; *) exit 0 ;; esac
for tbl in nm-shared-eth0 nm-shared-wlan0; do
  nft list table ip "$tbl" >/dev/null 2>&1 || continue
  nft insert rule ip "$tbl" filter_forward iifname "wlan0" oifname "eth0" accept 2>/dev/null
  nft insert rule ip "$tbl" filter_forward iifname "eth0"  oifname "wlan0" accept 2>/dev/null
done
EOF
sudo chmod +x /etc/NetworkManager/dispatcher.d/99-forward-hotspot-to-quinled
```

**Verify from a laptop on `TechnoLichtPi-AP`:**

```bash
ping 192.168.100.10
curl http://192.168.100.10/
```

> 💡 **Need internet on the Pi later** (e.g. for `apt`)? Temporarily switch eth0 to DHCP and plug it into the home router:
> ```bash
> sudo nmcli connection modify QuinLED ipv4.method auto
> sudo nmcli connection down QuinLED && sudo nmcli connection up QuinLED
> # …apt install…
> sudo nmcli connection modify QuinLED ipv4.method shared ipv4.addresses 192.168.100.1/24
> sudo nmcli connection down QuinLED && sudo nmcli connection up QuinLED
> ```

## 8. USB Ethernet — home network + internet (home mode)

USB Eth adapter shows up as `eth1` and pulls DHCP from your home router → Pi has internet. The hotspot stays up untouched for field use.

### 8a. Rename the auto-created profile

```bash
sudo nmcli connection modify "Wired connection 1" connection.id HomeNet
sudo nmcli connection modify HomeNet connection.autoconnect yes
```

### 8b. Extend the dispatcher to cover eth1 ↔ eth0

Replaces the wlan0-only version from step 7:

```bash
sudo tee /etc/NetworkManager/dispatcher.d/99-forward-hotspot-to-quinled <<'EOF'
#!/bin/sh
[ "$2" = "up" ] || exit 0
case "$1" in wlan0|eth0|eth1) ;; *) exit 0 ;; esac
nft list table ip nm-shared-eth0 >/dev/null 2>&1 || exit 0
for if_in in wlan0 eth1; do
  nft insert rule ip nm-shared-eth0 filter_forward iifname "$if_in" oifname "eth0" accept 2>/dev/null
  nft insert rule ip nm-shared-eth0 filter_forward iifname "eth0"  oifname "$if_in" accept 2>/dev/null
done
EOF
sudo chmod +x /etc/NetworkManager/dispatcher.d/99-forward-hotspot-to-quinled

# Apply now without waiting for the next interface-up event
sudo /etc/NetworkManager/dispatcher.d/99-forward-hotspot-to-quinled eth1 up
```

### 8c. Reserve Pi's home IP + static route on router

In your home router admin UI:

1. **Reserve a fixed DHCP lease** for the Pi's `eth1` MAC (find it with `ip link show eth1`). Note that IP — call it `<PI_HOME>` below.
2. **Add a static route**: destination `192.168.100.0/24`, gateway `<PI_HOME>`. Any device on the home LAN can then reach the QuinLED at `192.168.100.10`.

If your router doesn't support static routes, do it per-laptop instead:

```bash
sudo ip route add 192.168.100.0/24 via <PI_HOME>
```

### 8d. Verify from a home laptop

```bash
ping <PI_HOME>                  # Pi reachable on home LAN
ping 192.168.100.10             # QuinLED through Pi
curl http://192.168.100.10/     # WLED config
ssh duser@TechnoLichtPi.local   # mDNS works on home LAN too
```

### Mode summary

| Mode | USB Eth | Hotspot | LedFx control from | QuinLED reachable from |
|---|---|---|---|---|
| Home | plugged in | up (idle) | home LAN | home LAN (via static route) |
| Field | unplugged | up (active) | `TechnoLichtPi-AP` | hotspot clients (step 7 routing) |

## 9. Install LedFx + autostart service

LedFx is a Python app that pushes effects to networked LED controllers (WLED / QuinLED). On Trixie, install it isolated via `pipx`.

### 9a. Install dependencies + LedFx

`uv` (from Astral) is a fast modern Python toolchain — `uv tool install` is the equivalent of `pipx install` but resolves and installs in seconds.

```bash
# Build deps for PyAudio (LedFx pulls portaudio bindings)
sudo apt install -y portaudio19-dev python3-dev gcc

# Install uv (single static binary, drops itself into ~/.local/bin)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reload PATH for this shell
export PATH="$HOME/.local/bin:$PATH"

# Install LedFx as a uv tool (creates its own isolated venv)
uv tool install ledfx
```

`uv tool install` puts the `ledfx` binary at `~/.local/bin/ledfx`, ready for the systemd service in 9c. To upgrade later: `uv tool upgrade ledfx`.

### 9b. First run + connect the QuinLED

```bash
~/.local/bin/ledfx --open-ui
```

Then from a laptop, browse:

```
http://TechnoLichtPi.local:8888
```

In the UI: **Settings → Devices → Add → WLED**, IP/Host `192.168.100.10`. LedFx auto-detects the pixel count from WLED's API.

`Ctrl-C` to stop, then continue.

### 9c. systemd service for autostart

```bash
sudo tee /etc/systemd/system/ledfx.service <<'EOF'
[Unit]
Description=LedFx
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=duser
ExecStart=/home/duser/.local/bin/ledfx
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now ledfx
sudo systemctl status ledfx --no-pager
```

LedFx now starts at boot, restarts on crash, and the web UI is always at `http://TechnoLichtPi.local:8888`.

## 10. Audio input — USB-C sound card line-in

### 10a. Verify the card is detected

```bash
arecord -l        # ALSA capture devices — note the card,device numbers
lsusb             # confirm the USB audio is enumerated
```

Look for an entry like `card 1: ICUSBAUDIO7D, device 0: USB Audio`. Substitute those numbers below.

### 10b. Test capture

```bash
arecord -D plughw:1,0 -d 5 -f cd /tmp/test.wav
ls -lh /tmp/test.wav     # ~880 KB for 5 s of CD-quality audio = capturing
```

If it errors with permission denied, make sure `duser` is in the `audio` group:

```bash
groups duser
sudo usermod -aG audio duser  # if missing — then reboot
```

### 10c. Select Line as the capture source

⚠️ **Gotcha**: the CM106 chip defaults `PCM Capture Source` to `Mic`. Switch it to `Line` or your line-jack signal won't be captured:

```bash
amixer -c 1 sset 'PCM Capture Source' 'Line'
amixer -c 1 sget 'PCM Capture Source'    # confirm: Item0: 'Line'
sudo alsactl store                       # persist across reboots
```

Available items on this card: `'Mic'`, `'Line'`, `'IEC958 In'`, `'Mixer'`.

### 10d. Point LedFx at the input

In the LedFx web UI (`http://TechnoLichtPi.local:8888`):

1. **Settings → Audio Settings → Audio Device** dropdown.
2. Pick the USB sound card (`ICUSBAUDIO7D` / `USB Audio Device`).
3. Save.

If the dropdown doesn't show the card, LedFx enumerated audio before it was plugged in — restart:

```bash
sudo systemctl restart ledfx
```

### 10e. Calibrate input level (run whenever you plug in a different source)

Goal: VU meter peaks at **70–80%** on loud moments, drops noticeably in quieter parts. Clipping (`MAX`) flattens dynamics and kills LedFx's responsiveness.

```bash
sudo systemctl stop ledfx
arecord -D plughw:1,0 -f cd -V mono /dev/null   # live VU meter, Ctrl-C to quit
sudo systemctl start ledfx
```

Adjust the analog input gain on the Pi until the bars look right:

```bash
amixer -c 1 sset 'Line' 30% cap     # tweak the percentage to taste
sudo alsactl store                  # persist
```

⚠️ Use `'Line'`, **not** `'PCM'` — `PCM` is a post-source digital scaler and can't help with clipping at the ADC.

### Note: ALSA mixer over Ghostty terminal

`alsamixer` chokes on Ghostty's terminfo:

```bash
TERM=xterm alsamixer -c 1     # workaround
```

Or use `amixer` non-interactively (commands above).

## 11. Friendly names — `ledfx.lan` / `wled.lan`

Hotspot clients (phone, laptop) open the UIs by name, without IPs or ports:

| URL | Goes to |
|---|---|
| `http://ledfx.lan` | LedFx (`127.0.0.1:8888` on the Pi) |
| `http://wled.lan` | WLED on the QuinLED (`192.168.100.10`) |

How it works: the hotspot's dnsmasq resolves both names to the Pi (`192.168.50.1`); nginx on port 80 proxies by hostname. The phone only ever talks to the Pi, so WLED works even without the step 7 routing.

`.lan` rather than `.local`: `.local` is mDNS, which many Android phones don't resolve. Bare names (`http://ledfx`) get treated as searches by browsers.

### 11a. DNS names on the hotspot

```bash
sudo tee /etc/NetworkManager/dnsmasq-shared.d/names.conf <<'EOF'
address=/ledfx.lan/192.168.50.1
address=/wled.lan/192.168.50.1
EOF
sudo nmcli connection up Hotspot     # re-activates the hotspot; clients drop for a few seconds
```

Verify from the phone: `http://ledfx.lan:8888` opens LedFx.

### 11b. nginx reverse proxy

Needs internet (home mode, §8). IPv6 on the home LAN may not route — force IPv4:

```bash
sudo apt -o Acquire::ForceIPv4=true update
sudo apt -o Acquire::ForceIPv4=true install -y nginx
```

```bash
sudo tee /etc/nginx/sites-available/technolicht <<'EOF'
map $http_upgrade $connection_upgrade { default upgrade; '' close; }

# LedFx: http://ledfx.lan (also the default for http://192.168.50.1)
server {
    listen 80 default_server;
    server_name ledfx.lan;
    location / {
        proxy_pass http://127.0.0.1:8888;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_read_timeout 1d;
    }
}

# WLED on the QuinLED: http://wled.lan
server {
    listen 80;
    server_name wled.lan;
    location / {
        proxy_pass http://192.168.100.10;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_read_timeout 1d;
    }
}
EOF
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/technolicht /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

The `Upgrade`/`Connection` headers pass WebSockets through — both LedFx and WLED use them for live updates.

**Verify from the phone** (on `TechnoLichtPi-AP`): `http://ledfx.lan` and `http://wled.lan` both open.

### Using a phone on the road

⚠️ **Turn off mobile data.** The hotspot has no internet, so the phone sends traffic over mobile data instead — pages then load forever. With mobile data off (and "Stay connected" / "Use without internet" when prompted), everything works.

If names don't resolve: phone Settings → Private DNS → set to *Automatic* or *Off*. A fixed Private DNS provider bypasses the Pi's DNS.
