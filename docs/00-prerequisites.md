# 00 — Prerequisites

## Hardware

| Item | Spec | Qty |
|------|------|-----|
| Raspberry Pi 4B | 4GB RAM | 1 |
| MicroSD Card | 32GB+, Class 10 | 1 |
| Waveshare UPS HAT | 2x 18650 Li-ion | 1 |
| QuinLED-Dig-Octa | 8 outputs, WLED pre-flashed | 1 |
| QuinLED-Dig-Octa Power 7HC | Power distribution board | 1 |
| WS2815 LED Strip | 12V, RGBIC, 3cm pitch | 40m |
| USB 6-in-1 Sound Card | 48kHz, optical + analog | 1 |
| ZGT-25 DD SSR | Solid state relay | 1 |
| 12V Strobe | LED strobe light | 1+ |
| Ethernet Cable | Cat5e, any length | 1 |

## Power

| Item | Input | Output | Notes |
|------|-------|--------|-------|
| Main Battery | 14.4V (4S Li-ion) | — | Max charge ~16.8V |
| WG8-36s1225 Buck | 8-36V | 12V 25A | LED + QuinLED rail |
| DC-DC 50W Buck | 12V/24V | 5V 10A | RPi + USB + UPS charge |
| USB 5V→8.4V Cable | 5V | 8.4V | Charges UPS HAT via jack |

## Tools

- Computer with Raspberry Pi Imager
- MicroSD card reader
- SSH client (Linux/Mac terminal, PuTTY, or Windows Terminal)
- Small Phillips screwdriver
- Wire strippers + crimper

## Before You Start

- Know your QuinLED's current WLED IP (check router or serial monitor)
- Verify WLED is responsive via web UI before connecting RPi
- Have your 14.4V battery charged and ready
