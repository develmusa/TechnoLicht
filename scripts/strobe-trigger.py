#!/usr/bin/env python3
"""
Strobe Trigger Placeholder

Future implementation: Control ZGT-25 DD SSR strobe via QuinLED relay output.

The SSR is connected to QuinLED output 7 (relay mode).
Trigger via WLED HTTP API:
  curl -X POST http://192.168.100.100/json/state \
    -d '{"seg":[{"id":7,"on":true}]}'

Or manually toggle via WLED web UI.
"""

import requests
import time

QUINLED_IP = "192.168.100.100"


def strobe_on():
    url = f"http://{QUINLED_IP}/json/state"
    payload = {"seg": [{"id": 7, "on": True}]}
    requests.post(url, json=payload)


def strobe_off():
    url = f"http://{QUINLED_IP}/json/state"
    payload = {"seg": [{"id": 7, "on": False}]}
    requests.post(url, json=payload)


def main():
    print("Strobe trigger script - placeholder")
    print("Use WLED web UI or HTTP API to control relay output 7")


if __name__ == "__main__":
    main()
