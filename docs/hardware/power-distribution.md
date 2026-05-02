# Power Distribution

## Architecture

```
14.4V Battery (4S Li-ion, max 16.8V)
│
└──→ WG8-36s1225 Buck Converter (12V 25A)
     │
     ├──→ QuinLED-Dig-Octa Powerboard
     │    ├──→ LED Output 0: Strip 1 (10m WS2815)
     │    ├──→ LED Output 1: Strip 2 (10m WS2815)
     │    ├──→ LED Output 2: Strip 3 (10m WS2815)
     │    ├──→ LED Output 3: Strip 4 (10m WS2815)
     │    └──→ LED Output 7: ZGT-25 DD SSR → 12V Strobe
     │
     ├──→ 12V Power Injection Points
     │    ├──→ Strip 1: 5m, 10m
     │    ├──→ Strip 2: 5m, 10m
     │    ├──→ Strip 3: 5m, 10m
     │    └──→ Strip 4: 5m, 10m
     │
     └──→ 12V→5V 50W Buck Converter
          │
          ├──→ RPi4B (USB-C or GPIO 5V pins)
          ├──→ USB 6-in-1 Sound Card
          └──→ USB 5V→8.4V Converter Cable
               └──→ Waveshare UPS HAT Charging Jack (8.4V)
                    └──→ UPS HAT on RPi GPIO (I2C, 5V backup)
```

## Rails

| Rail | Voltage | Source | Loads |
|------|---------|--------|-------|
| **Main** | 14.4V | Battery | WG8-36s1225 input |
| **12V** | 12V | WG8-36s1225 | QuinLED, LED strips, SSR, 12V→5V converter |
| **5V** | 5V | 12V→5V 50W | RPi, USB sound card, UPS charger |
| **8.4V** | 8.4V | USB 5V→8.4V | UPS HAT charging jack |

## Converters

| Converter | Input | Output | Max | Purpose |
|-----------|-------|--------|-----|---------|
| WG8-36s1225 | 8-36V | 12V | 25A | Main LED + QuinLED rail |
| 12V→5V 50W | 12V/24V | 5V | 10A | RPi + peripherals + UPS charge |
| USB 5V→8.4V | 5V | 8.4V | ~1A | UPS HAT battery charging |

## Fusing

Fuses are handled by the **QuinLED Power 7HC board**.

Per-output fusing (verify on your board):
- Each LED output has its own fuse or polyfuse
- Total input has main fuse

**Add external fusing if your board lacks it**:
- Main 12V input: 30A fuse
- Per 10m strip: 10A fuse
- 5V rail: 15A fuse

## Wire Gauges

| Run | Gauge | Reason |
|-----|-------|--------|
| Battery → 12V buck | 10 AWG | Up to 30A peak |
| 12V buck → QuinLED | 10-12 AWG | Up to 25A |
| 12V injection points | 16 AWG | ~8A per injection |
| QuinLED → strip start | 18 AWG | Data + power, short run |
| 12V → 5V buck | 14 AWG | Up to 10A |
| 5V → RPi/USB | 18-20 AWG | ~3-5A |

## UPS HAT Behavior

| State | Current | Meaning |
|-------|---------|---------|
| Positive | Charging | External power present, cells charging |
| Negative | Discharging | Running on battery |
| ~0 | Idle | Fully charged, trickle/float |

The UPS HAT provides **5V backup power** to the RPi when the main 14.4V battery is disconnected (e.g., during a battery swap). It does **not** power the LEDs or sound card.

## Critical Notes

- **Brightness limit**: Set WLED to ~70% max to keep 12V load under 25A
- **Peak load**: All-white at 100% on 40m WS2815 = ~60A — **will blow fuse/buck converter**
- **Thermal**: Mount buck converters with airflow; they will get warm under load
- **Grounding**: All GNDs must be common — QuinLED GND, LED strip GND, RPi GND, audio GND
