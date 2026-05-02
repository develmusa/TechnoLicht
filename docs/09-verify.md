# 09 — Verification

Run all checks before first ride.

## Network

```bash
ping -c 3 192.168.100.100
```

QuinLED must respond.

## Audio

```bash
arecord -l
```

USB sound card must be listed.

Test capture:
```bash
arecord -d 3 -f cd /dev/null
```

No errors.

## Docker

```bash
docker ps
```

LedFx container running.

## LedFx Web UI

```bash
curl -s http://localhost:8888 | head
```

Should return HTML.

Open in browser: `http://ledfx.local:8888`

## LEDs

In LedFx web UI:
1. Select your WLED device
2. Choose an audio-reactive effect (e.g., "Energy", "Spectrum")
3. Play music through your amp
4. LEDs should react to the beat

## UPS HAT

```bash
sudo systemctl status ups-monitor
```

Service active.

```bash
sudo journalctl -u ups-monitor --no-pager -n 10
```

Recent battery readings visible.

## Strobe

Test via WLED web UI (`192.168.100.100`):
1. Go to Segments
2. Select relay output (output 7)
3. Toggle ON/OFF
4. SSR should click, strobe should fire

## Power

Measure rails with multimeter:
- 12V rail: 11.8-12.2V under LED load
- 5V rail: 4.9-5.1V
- 8.4V at UPS HAT jack: 8.2-8.5V when charging

## Done

System is ready. See `10-troubleshooting.md` if anything fails.
