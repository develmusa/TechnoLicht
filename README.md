# TechnoLicht

Sound-reactive LED light system for a three-wheel bicycle.

**Controller**: QuinLED-Dig-Octa (WLED)  
**Brain**: Raspberry Pi 4B + Waveshare UPS HAT  
**Software**: LedFx (Docker)  
**LEDs**: 40m WS2815 12V RGBIC, 3cm pitch  
**Audio**: USB 6-in-1 sound card (line-in from 4-channel amp)  
**Strobe**: ZGT-25 DD SSR via QuinLED relay output  

## Quickstart

1. Flash Raspberry Pi OS Lite (64-bit) to SD card: `xzcat ... | sudo dd of=/dev/sdX`
2. Copy `boot/user-data` and `boot/meta-data` to the boot partition
3. Boot the Pi — everything (network, Docker, hotspot, audio, LedFx, UPS monitor) configures automatically
4. Join WiFi `TechnoLicht` / `technolight123` and open [http://ledfx.local](http://ledfx.local)

Full steps: `docs/01-flash-os.md`

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
| 08 | Hotspot (verify) |
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
├── boot/             # Cloud-init NoCloud files (user-data + meta-data)
├── docs/             # Setup instructions (markdown + commands)
│   └── hardware/     # Wiring, power, LED strip reference
├── scripts/          # Python helpers (UPS monitor, strobe trigger)
└── wireviz/          # Wiring diagrams as code
```

*Note: All config files previously in `config/` and `docker/` are now baked into `boot/user-data` and written to the Pi on first boot.*
