# TechnoLicht Project Plan

## Project Context
TechnoLicht is a light control system for a three-wheel bicycle with a sound system.

### Hardware
- QuinLED-Dig-Octa (WLED firmware) controlling WS2815 12V LED strips (40m total)
- Raspberry Pi 4B with Waveshare UPS HAT (2x NCR18650B) running LedFx for sound-reactive effects
- USB 6-in-1 sound card for audio input (line-in from a 4-channel amp)
- Optional: WiFi hotspot for Rekordbox streaming from a DJ laptop
- ZGT-25 DD solid-state relay for 12V strobe control via QuinLED relay output
- Power: 14.4V battery -> WG8-36s1225 buck converter (12V rail) -> QuinLED, LED strips, 12V->5V 50W converter -> RPi, USB sound card, USB 5V->8.4V converter -> Waveshare UPS HAT charging jack
- Networking: RPi <-> QuinLED via Ethernet static IPs (192.168.100.10 / .100)
- LED distribution: 4 outputs x 10m WS2815 (outputs 0-3), output 7 for SSR strobe
- Power injection: 12V/GND every 5m on 10m strips

### Software / IaC
- Cloud-init NoCloud on Raspberry Pi OS Lite 64-bit
- WireViz (YAML-defined) for wiring diagrams
- Docker Compose for LedFx deployment

### Key Design Decisions
- Cloud-init for IaC (rejected Ansible, NixOS and Pulumi after analysis)
- Docker Compose for LedFx deployment
- USB sound card as default audio input, Rekordbox over WiFi as optional
- Static Ethernet IPs: RPi 192.168.100.10, QuinLED 192.168.100.100
- WiFi hotspot SSID "TechnoLicht" / password "technolight123"
- 4x10m LED strips on QuinLED outputs 0-3, output 7 for SSR strobe
- Power injection every 5m
- Waveshare UPS HAT charged via USB 5V->8.4V converter from 5V rail
- UPS HAT: telemetry only, NO auto-shutdown (battery bridges main battery swaps)
- WLED and LedFx LED configuration done manually via web UI for simplicity

## Proposed Repository Structure

```
TechnoLicht/
├── README.md
├── audio-system-diagram.html
├── ansible/
│   ├── ansible.cfg
│   ├── inventory.ini
│   ├── playbook.yml
│   ├── group_vars/all.yml
│   └── roles/
│       ├── common/
│       ├── network/
│       ├── audio/
│       ├── ups_hat/
│       ├── docker/
│       └── ledfx/
├── wireviz/
│   ├── power-distribution.yml
│   ├── quinled-outputs.yml
│   ├── quinled-relay.yml
│   ├── rpi-network.yml
│   ├── power-injection.yml
│   └── Makefile
├── config/
│   ├── network/
│   └── wled/
├── docker/
│   └── docker-compose.yml
├── scripts/
│   ├── power-monitor.py
│   └── strobe-trigger.py
└── docs/
    ├── hardware/
    └── software/
```
