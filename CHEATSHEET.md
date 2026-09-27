# TechnoLicht — Operation Cheat Sheet

⚠️ Contains passwords — keep private. Setup details: `raspberry-pi-os-install.md`.

## Connect (phone or laptop)

1. WiFi **`TechnoLichtPi-AP`** · password **`technolight123`**
2. "No internet" prompt → **Stay connected** / **Use without internet**
3. **Turn off mobile data** — otherwise pages load forever

| Open | URL | Fallback |
|---|---|---|
| LedFx (effects, audio) | **http://ledfx.lan** | http://192.168.50.1:8888 |
| WLED (QuinLED, LEDs, brightness) | **http://wled.lan** | http://192.168.100.10 |

Names don't work? Phone Settings → Private DNS → *Automatic* or *Off*. Or use the fallback IPs.

## Power

| Step | Action |
|---|---|
| On | Pi via UPS HAT **8.4V barrel jack** (not USB-C) · 12V LED supply on · wait ~1 min |
| Off | `sudo poweroff` over SSH → wait for the green LED to stop → cut power |

Pulling power without shutting down can corrupt the SD card.

## SSH

```bash
ssh duser@192.168.50.1          # password: powermorepower
```

From a phone: any SSH app (e.g. Termius), same host/user.

## Everyday commands (on the Pi)

| What | Command |
|---|---|
| LedFx status / restart | `systemctl status ledfx` · `sudo systemctl restart ledfx` |
| LedFx log | `journalctl -u ledfx -f` |
| nginx (names) restart | `sudo systemctl restart nginx` |
| QuinLED reachable? | `ping -c3 192.168.100.10` |
| Battery (UPS HAT) | `python3 ~/ups-hat/UPS_HAT/INA219.py` |
| Audio level check | `sudo systemctl stop ledfx` → `arecord -D plughw:1,0 -f cd -V mono /dev/null` → Ctrl-C → `sudo systemctl start ledfx` |
| Input gain | `amixer -c 1 sset 'Line' 30% cap && sudo alsactl store` |
| Reboot | `sudo reboot` |

Audio target: VU peaks at **70–80%**, never `MAX`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Page loads forever | Mobile data off; check you're on `TechnoLichtPi-AP` |
| `ledfx.lan` not found | Use http://192.168.50.1:8888; check phone Private DNS |
| LedFx opens, LEDs dark | Open WLED — Power on? Brightness > 0? Then `ping -c3 192.168.100.10` on the Pi |
| WLED unreachable | Check Ethernet cable Pi ↔ QuinLED (link LEDs lit); power-cycle QuinLED |
| LEDs don't react to music | LedFx → Settings → Audio Device = USB sound card; `sudo systemctl restart ledfx`; check audio level |
| Wrong colours | WLED → Config → LED Preferences → Color order (GRB) |
| LEDs flicker / brown out | Lower brightness; check brightness limiter in WLED |
| Nothing works | `sudo reboot`, wait 1 min, reconnect WiFi |

## Addresses

| Device | IP |
|---|---|
| Pi (hotspot) | `192.168.50.1` |
| Pi (Ethernet to QuinLED) | `192.168.100.1` |
| QuinLED | `192.168.100.10` |
| Phone / laptop | `192.168.50.x` (DHCP) |
