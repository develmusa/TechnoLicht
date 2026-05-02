# Wiring Diagrams

All diagrams are generated from YAML source using WireViz.

## Generate Diagrams

```bash
cd ~/TechnoLicht/wireviz
make diagrams
```

Outputs:
- `output/power-distribution.svg` — Full power tree
- `output/quinled-outputs.svg` — LED strip data wiring
- `output/quinled-relay.svg` — SSR strobe control
- `output/rpi-network.svg` — Ethernet, USB, GPIO
- `output/power-injection.svg` — LED power injection points

## Install WireViz

```bash
pip install wireviz
```

## Physical Build Notes

WireViz shows logical connections. Physical routing:
- Keep power and data cables separated where possible
- Use twisted pair for data lines if running near power
- All GNDs tie to common ground plane
- BI (Backup Input) tied to GND at first LED of each strip

## Updating Diagrams

Edit the `.yml` files, then rerun `make diagrams`.
