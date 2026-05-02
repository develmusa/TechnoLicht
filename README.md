# TechnoLicht

Sound-reactive LED light system for a three-wheel bicycle.

**Controller**: QuinLED-Dig-Octa (WLED)  
**Brain**: Raspberry Pi 4B + Waveshare UPS HAT  
**Software**: LedFx (Docker)  
**LEDs**: 40m WS2815 12V RGBIC, 3cm pitch  
**Audio**: USB 6-in-1 sound card (line-in from 4-channel amp)  
**Strobe**: ZGT-25 DD SSR via QuinLED relay output  

## Quickstart

### Recommended: Cloud-init (Zero Manual Steps)

1. Flash Raspberry Pi OS Lite (64-bit) to SD card: `xzcat ... | sudo dd of=/dev/sdX`
2. Copy `boot/user-data` and `boot/meta-data` to the boot partition
3. Boot the Pi — everything (network, Docker, hotspot, audio) configures automatically
4. Join WiFi `TechnoLicht` / `technolight123` and open [http://ledfx.local](http://ledfx.local)

Full steps: `docs/01-flash-os.md`

### Fallback: Manual Setup

1. Flash Raspberry Pi OS Lite (64-bit) using Raspberry Pi Imager
2. Copy `config/` to `/home/pi/TechnoLicht/` on the Pi
3. Follow `docs/01-flash-os.md` through `docs/09-verify.md`

## Network

```
[Laptop] ~~~~ WiFi ~~~~> [Pi wlan0: 192.168.50.1]
                              |
                              | IP forwarding + NAT
                              |
[QuinLED] <---- Eth ----> [Pi eth0: 192.168.100.10]
(192.168.100.100)
```

| Device | Interface | IP | Friendly Name |
|--------|-----------|-----|---------------|
| Pi | `eth0` | `192.168.100.10` | — |
| Pi | `wlan0` (AP) | `192.168.50.1` | `ledfx.local` |
| QuinLED | `eth0` | `192.168.100.100` | `quinled.local` |

- **WiFi clients** get DHCP IPs `192.168.50.10–200`
- **DNS aliases** (`ledfx.local`, `quinled.local`) work automatically for connected laptops

## Docs

| Step | Topic |
|------|-------|
| 00 | Prerequisites |
| 01 | Flash OS |
| 02 | First Boot |
| 03 | Network |
| 04 | Audio |
| 05 | Docker |
| 06 | LedFx |
| 07 | UPS HAT |
| 08 | Hotspot (optional) |
| 09 | Verify |
| 10 | Troubleshooting |

## Wiring Diagrams

```bash
cd wireviz
make diagrams
```

Outputs SVGs to `wireviz/output/`.

## Repo Structure

```
TechnoLicht/
├── README.md
├── audio-system-diagram.html
├── docs/           # Setup instructions (markdown + commands)
├── config/         # Ready-to-use config files
├── wireviz/        # Wiring diagrams as code
├── docker/         # Docker Compose for LedFx
└── scripts/        # Python helpers
```
