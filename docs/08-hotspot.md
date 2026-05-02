# 08 — WiFi Hotspot (Verify)

> **Already set up by cloud-init.** If you flashed using the primary method in `01-flash-os.md`, everything below is already running. Use this doc to verify.

---

## What Was Configured Automatically

- **SSID**: `TechnoLicht`
- **Password**: `technolight123`
- **Channel**: 7 (2.4 GHz)
- **Pi IP**: `192.168.50.1` (AP default gateway)
- **Client DHCP pool**: `192.168.50.10 – 192.168.50.200`
- **DNS aliases**: `ledfx.local`, `quinled.local`

---

## Verification Steps

### 1. Check hostapd status

```bash
sudo systemctl status hostapd
```

Expected: `active (running)`

### 2. Check the AP is visible

```shell
# On any device:
iwlist wlan0 scan | grep -i technolight
```

Or just look for `TechnoLicht` in your WiFi network list.

### 3. Check dnsmasq is handing out IPs

```bash
sudo cat /var/log/dnsmasq.log | tail -20
```

Expected: DHCPACK lines with `192.168.50.x` assignments.

### 4. Test DNS aliases from the laptop

Connect your laptop to `TechnoLicht`, then:

```bash
nslookup ledfx.local
# Expected: 192.168.50.1

nslookup quinled.local
# Expected: 192.168.100.100
```

---

## Disable Hotspot

If you need to shut it down temporarily (e.g., RF interference at an event):

```bash
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
```

To re-enable:

```bash
sudo systemctl start hostapd
sudo systemctl start dnsmasq
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Hotspot not visible | Check `sudo systemctl status hostapd`. Reboot if hostapd fails on first boot (race condition with wlan0 bring-up). |
| No internet for clients | **Expected** — this is an isolated network for show control, not a gateway to the internet. |
| RF interference at events | Stop hostapd/dnsmasq and use Ethernet for the laptop. Or move to 5 GHz if your Pi supports it. |

---

## Done

Proceed to `09-verify.md`.
