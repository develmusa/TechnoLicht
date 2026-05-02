# 04 — Audio Setup

Goal: USB 6-in-1 sound card as default ALSA capture device.

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

## Step 3: Apply ALSA Config

```bash
sudo cp ~/TechnoLicht/config/asound.conf /etc/asound.conf
```

This sets the USB sound card as default capture.

## Step 4: Set Capture Volume

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

## Step 5: Test Capture

```bash
arecord -d 5 -f cd test.wav
aplay test.wav
```

You should hear audio from your amp. If not, check connections and volume.

## Step 6: Clean Up

```bash
rm test.wav
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| No sound card in `arecord -l` | Re-plug USB, try different port |
| Static/noise | Check ground loop; try different USB port |
| Clipping/distortion | Lower capture volume in `alsamixer` |

## Done

Proceed to `05-docker.md`.
