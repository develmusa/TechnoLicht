# 04 — Audio Setup

Goal: USB 6-in-1 sound card as default ALSA capture device, tuned for the amp line-in.

> `asound.conf` was already written by cloud-init. This doc covers detection, volume tuning, and verification.

---

## Step 1: Plug In Sound Card

Connect USB sound card to any RPi USB port.

Connect line-out from your 4-channel amp to the sound card's line-in (3.5mm).

## Step 2: Verify Detection

```bash
arecord -l
```

Expected output (example):
```
card 1: Device [USB Audio Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

Note your card number (e.g., `card 1`).

> `asound.conf` already sets `card 1` as default. If your card number differs, skip to **Troubleshooting**.

## Step 3: Set Capture Volume

```bash
alsamixer
```

- Press `F4` for Capture
- Set volume to ~70-80% (avoid clipping)
- Press `Esc` to exit

Save levels:
```bash
sudo alsactl store
```

## Step 4: Test Capture

```bash
arecord -d 5 -f cd test.wav
aplay test.wav
```

You should hear audio from your amp. If not, check connections and volume.

## Step 5: Clean Up

```bash
rm test.wav
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| No sound card in `arecord -l` | Re-plug USB, try different port |
| Card number is not `1` | Edit `/etc/asound.conf` to match your card number, then `sudo alsactl store` |
| Static/noise | Check ground loop; try different USB port |
| Clipping/distortion | Lower capture volume in `alsamixer` |

## Done

Proceed to `06-ledfx.md`.
