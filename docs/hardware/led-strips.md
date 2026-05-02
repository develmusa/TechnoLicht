# WS2815 LED Strip Wiring

## Strip Specs

- **Type**: WS2815 RGBIC, 12V
- **Pitch**: 3cm
- **Total Length**: 40m
- **Distribution**: 4 outputs × 10m (QuinLED outputs 0-3)
- **Wire**: Black, 3-pin + BI backup line

## The BI (Backup Input) Line

WS2815 strips have **4 pads** at each cut point:
- **12V / V+** — Power
- **GND** — Ground
- **DI** — Data In
- **BI** — Backup Input

**You only need to connect 3 wires** from the controller to the strip:
- 12V → V+
- GND → GND
- DI → Data output

### Grounding BI

At the **start of each strip** (the first LED), tie **BI to GND**:
- Use a small wire jumper between BI and GND pads
- Or put a solder blob connecting BI to GND on the first LED

**Why**: The first LED generates the backup signal internally. If one LED dies, the next LED switches to the backup line automatically. You do not run BI back to the controller.

## Data Resistor Selection

QuinLED-Dig-Octa has a **selectable resistor** per channel (33Ω or 249Ω). Switch location is on the board, accessible without removing the ESP32.

| Resistor | Use When | Typical Cable |
|----------|----------|---------------|
| **249Ω** (default) | Data wire runs **separate** from power/GND | Thick 2-wire power + thin data-only wire |
| **33Ω** | Data and GND run **together** in same bundle | 2-wire, 3-wire, or 4-wire bundled cable, twisted pair |

### Rule of Thumb

- **Under 3m / 10ft**: Either resistor works. Leave at 249Ω default.
- **Over 3m with bundled cable**: Switch to **33Ω**.
- **Separate data wire any length**: Use **249Ω**.

Each of the 8 channels can be set independently.

## Physical Wiring per Strip

```
QuinLED Output          First LED              Rest of Strip
┌─────────┐            ┌─────────┐            ┌─────────┐
│ 12V     ├────────────┤ 12V     ├────────────┤ 12V     │
│ GND     ├────────────┤ GND     ├────────────┤ GND     │
│ DATA    ├────────────┤ DI      ├────────────┤ DI      │
│         │     ┌──────┤ BI      │            │ BI      │
│         │     │      └─────────┘            └─────────┘
│         │     │       ↑ Jumper/solder blob at first LED
└─────────┘     └───────┘ BI tied to GND
```

## Power Injection

Inject **12V + GND** every **5 meters** on each 10m strip:
- Start of strip: power from QuinLED output
- 5m midpoint: power injection from 12V rail
- End of strip: power injection from 12V rail (optional, recommended for 10m)

**Wire gauge for injection**: 16 AWG minimum

## Connections Summary

| From | To | Wire | Gauge | Notes |
|------|----|------|-------|-------|
| QuinLED Out 0-3 | Strip Start | 3-wire | 18 AWG | 12V, GND, DI |
| Strip Start BI | Strip Start GND | Jumper | — | Solder blob or short wire |
| 12V Rail | Strip 5m point | 2-wire | 16 AWG | Power injection |
| 12V Rail | Strip 10m end | 2-wire | 16 AWG | Power injection |

## Setting Resistor on Dig-Octa

1. Power off QuinLED
2. Locate the resistor switcher for the channel (labeled per output)
3. Move jumper/switch to **33R** or **249R** position
4. Power on and test

**Channels 0-3**: Set based on your cable type (likely 33Ω if using bundled cable)
**Channel 7**: SSR strobe — resistor setting irrelevant for relay output
