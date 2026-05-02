# QuinLED-Dig-Octa Reference

## Board Layout

| Section | Function |
|---------|----------|
| **Brainboard** | ESP32 + Ethernet, runs WLED |
| **Powerboard (7HC)** | 7 high-current outputs + power distribution |
| **Relay Output** | Channel 7 (or dedicated relay header) |
| **Resistor Switchers** | Per-channel 33Ω / 249Ω selector |

## Output Mapping

| Output | Assignment | LED Count | Notes |
|--------|-----------|-----------|-------|
| **0** | Strip 1 | 333 LEDs (10m) | Front / left side |
| **1** | Strip 2 | 333 LEDs (10m) | Front / right side |
| **2** | Strip 3 | 333 LEDs (10m) | Rear / left side |
| **3** | Strip 4 | 333 LEDs (10m) | Rear / right side |
| **4** | Unused | — | Available for expansion |
| **5** | Unused | — | Available for expansion |
| **6** | Unused | — | Available for expansion |
| **7** | SSR Strobe | — | Relay mode, not LED data |

Total: ~1,333 LEDs across 4 strips

## Resistor Switchers

Each channel has a physical switch/jumper for data output resistor:

- **249Ω** — Default. Use with separate data wire.
- **33Ω** — Use with bundled cable (data + GND together).

Switch is accessible on the board. No need to remove ESP32.

## Ethernet Configuration

| Parameter | Value |
|-----------|-------|
| IP Address | 192.168.100.100 |
| Subnet Mask | 255.255.255.0 |
| Gateway | 192.168.100.1 |
| Type | QuinLED-Dig-Octa |

Set in WLED: Settings → WiFi Setup → Ethernet Type

## Relay Output (Strobe)

| Parameter | Value |
|-----------|-------|
| Control | WLED channel 7 |
| Device | ZGT-25 DD SSR |
| Strobe Power | 12V via SSR |
| Trigger | WLED segment ON/OFF or preset |

**WLED Setup**:
1. Go to Segments
2. Create segment for output 7
3. Set segment length to 1 (dummy pixel)
4. Toggle segment ON to trigger SSR
5. Toggle segment OFF to release SSR

## WLED Presets

Presets are stored on the QuinLED ESP32. Back them up via:
- WLED UI: Config → Security & Updates → Backup configuration
- Or HTTP API: `http://192.168.100.100/json/cfg`

## Firmware Updates

If reflashing:
https://install.quinled.info/dig-octa/index.html

## Physical Connections

| Connector | To |
|-----------|----|
| 12V Input | WG8-36s1225 output |
| GND Input | WG8-36s1225 GND |
| Ethernet | RPi eth0 (192.168.100.10) |
| Out 0-3 | WS2815 strips (DI, 12V, GND) |
| Out 7 | ZGT-25 DD SSR control pins |

## Power Budget

| Load | Current (max white) | Notes |
|------|---------------------|-------|
| 333 LEDs @ 12V | ~8A | Per 10m strip |
| 4 strips | ~32A | Total LED load |
| QuinLED logic | ~0.5A | |
| SSR coil | ~0.02A | Negligible |
| **Total 12V** | **~32.5A** | WG8-36s1225 rated 25A — **use WLED brightness limit** |

**Critical**: Set WLED brightness limit to ~70% to stay within 25A. Or limit max white in presets.
