# TechnoLicht — TODO

## Audio Device Configuration (Blocked — Hardware Not Yet Available)

- [ ] USB 6-in-1 sound card not yet available
- [ ] Once connected, run `arecord -l` on the Pi to find card number
- [ ] Update `boot/user-data` → `ledfx-config/config.yaml` → `audio.device_index`
- [ ] Run `alsamixer` to set capture volume to ~70–80%
- [ ] Verify audio capture works: `arecord -d 5 -f cd test.wav && aplay test.wav`

## WLED Configuration (Manual — By Design)

- [ ] Configure QuinLED outputs 0–3 (10m WS2815 each, ~333 LEDs)
- [ ] Set WLED brightness limit to ~70% (safety — 25A buck converter limit)
- [ ] Configure output 7 as relay for SSR strobe
- [ ] Save WLED presets and back up config

## Post-First-Boot Verification

- [ ] Verify `hostapd` and `dnsmasq` are running
- [ ] Verify QuinLED reachable at `192.168.100.100`
- [ ] Verify LedFx web UI at `http://ledfx.local`
- [ ] Add WLED device in LedFx UI (or run auto-discover)
- [ ] Configure segments and effects manually in LedFx
