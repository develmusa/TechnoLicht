# 03 — Network Setup

Goal: The Raspberry Pi bridges two isolated networks so the DJ laptop can control both the Pi (LedFx) and the QuinLED brain via friendly names.

```
[Laptop] ~~~~ (WiFi AP) ~~~~> [Pi wlan0: 192.168.50.1]
                                  |
                                  | IP forwarding + NAT
                                  |
[QuinLED] <---- (Eth) ----> [Pi eth0: 192.168.100.10]
(192.168.100.100)
```

| Interface | Role | IP | Subnet |
|-----------|------|-----|--------|
| `eth0` | Direct link to QuinLED | `192.168.100.10/24` | `192.168.100.0/24` |
| `wlan0` | WiFi AP for DJ laptop | `192.168.50.1/24` | `192.168.50.0/24` |

---

## What Cloud-Init Already Did

If you used the cloud-init method in `01-flash-os.md`, the following are already configured. Use this doc to **understand** or **verify** the setup.

---

## Manual Verification Steps

### 1. Check eth0 (QuinLED link)

```bash
ip addr show eth0
```

Expected:
```
inet 192.168.100.10/24 brd 192.168.100.255 scope global eth0
```

### 2. Check wlan0 (WiFi AP)

```bash
ip addr show wlan0
```

Expected:
```
inet 192.168.50.1/24 brd 192.168.50.255 scope global wlan0
```

### 3. Check IP forwarding is enabled

```bash
sysctl net.ipv4.ip_forward
```

Expected: `net.ipv4.ip_forward = 1`

### 4. Check hostapd is running

```bash
sudo systemctl status hostapd
```

Expected: `active (running)`

### 5. Check dnsmasq is running

```bash
sudo systemctl status dnsmasq
```

Expected: `active (running)`

---

## Configure QuinLED Brain

Set the QuinLED to static IP via its WLED web UI:

1. **WLED Settings → WiFi Setup**
   - Disable WiFi
2. **WLED Settings → Ethernet Type**
   - Select `QuinLED-Dig-Octa`
3. **Static IP settings:**
   - IP: `192.168.100.100`
   - Gateway: `192.168.100.10` ← **The Pi**, not `192.168.100.1`
   - Subnet: `255.255.255.0`
4. Save and reboot QuinLED.

### Verify Reachability

From the Pi:
```bash
ping 192.168.100.100
```

Or from the DJ laptop (connected to `TechnoLicht` WiFi):
```bash
ping quinled.local
```

---

## DNS Aliases for Convenience

The Pi's `dnsmasq` already advertises these names to WiFi clients:

| Friendly Name | Resolves To | What It Opens |
|---------------|-------------|---------------|
| `http://ledfx.local` | `192.168.50.1` | LedFx web UI |
| `http://quinled.local` | `192.168.100.100` | QuinLED WLED settings |

No `/etc/hosts` editing needed on the laptop.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Laptop can't reach QuinLED | Check IP forwarding (`sysctl net.ipv4.ip_forward`). Verify iptables rules (`sudo iptables -t nat -L`). |
| `ledfx.local` doesn't resolve | Ensure laptop accepted the Pi (`192.168.50.1`) as its DNS server via DHCP. Try `nslookup ledfx.local 192.168.50.1`. |
| No gateway on eth0 | **Correct** — `eth0` is a direct link, not a routed network. The Pi is the only "gateway" QuinLED needs to talk to the laptop. |

---

## Done

Proceed to `04-audio.md`.
