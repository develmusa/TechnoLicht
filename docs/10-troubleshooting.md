# 10 — Troubleshooting

## RPi Won't Boot

| Symptom | Fix |
|---------|-----|
| Red LED only, no green | Re-flash SD card |
| Kernel panic | Re-flash SD card |
| Boots but no SSH | Connect monitor/keyboard, check `raspi-config` |

## SD Card Corruption

```bash
# Check filesystem
sudo fsck -f /dev/mmcblk0p2

# Backup config
tar -czf ledfx-backup-$(date +%Y%m%d).tar.gz ~/ledfx-config

# Re-flash and restore
```

Keep a second flashed SD card as spare.

## No Audio in LedFx

```bash
# Check ALSA
cat /proc/asound/cards
arecord -l

# Test capture
arecord -d 5 -f cd test.wav

# Restart LedFx
cd ~/TechnoLicht/docker && docker compose restart
```

## QuinLED Not Responding

```bash
ping 192.168.100.100
```

If no response:
- Check Ethernet cable
- Check QuinLED power LED
- Reboot QuinLED (power cycle)
- Verify WLED static IP config

## LEDs Not Lighting

- Check 12V rail voltage under load
- Check WLED LED settings (output type = WS2815, color order = RGB)
- Check data wire continuity
- Test with WLED built-in effects (no LedFx)

## LedFx Laggy / High Latency

- Reduce pixel count in LedFx segments
- Disable complex effects, use simpler ones (Energy, Spectrum)
- Check RPi CPU usage: `htop`
- Try running LedFx natively (not Docker) if latency persists:
  ```bash
  pip3 install ledfx
  ledfx --open-ui
  ```

## Docker Issues

```bash
# View logs
docker logs ledfx

# Restart
sudo systemctl restart ledfx

# Or manually via docker compose (path exists on the Pi, written by cloud-init)
cd ~/TechnoLicht/docker && docker compose restart

# Rebuild
cd ~/TechnoLicht/docker && docker compose down && docker compose up -d
```

## UPS HAT Not Detected

```bash
sudo i2cdetect -y 1
```

If no `42`:
- Check HAT seated firmly on GPIO
- Check I2C enabled: `sudo raspi-config nonint do_i2c 0`
- Reboot

## Battery Swelling / Heat

**Stop immediately.** Disconnect power. Replace 18650 cells. Do not use damaged Li-ion batteries.

## Emergency Shutdown

If system is unresponsive:
```bash
sudo shutdown -h now
```

Or hold RPi power button (if connected) for 5 seconds.

## Still Stuck?

Check logs:
```bash
sudo dmesg | tail -50
sudo journalctl -xe
```
