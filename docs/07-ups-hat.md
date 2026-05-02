# 07 — UPS HAT Setup

Goal: Monitor battery voltage, current, and percentage via I2C.

> `ups-monitor.service` was already installed and enabled by cloud-init. This doc covers verification and battery reading.

---

## Step 1: Verify I2C Detection

```bash
sudo i2cdetect -y 1
```

You should see `42` in the output.

If nothing appears:
- Check the HAT is firmly seated on the GPIO header
- Reboot: `sudo reboot`

## Step 2: Install Python Dependencies

```bash
pip3 install smbus2
```

## Step 3: Test Monitor Script

```bash
cd ~/TechnoLicht/scripts
python3 power-monitor.py
```

Expected output:
```
Voltage: 8.35 V
Current: -450 mA
Power: 3.76 W
Percentage: 87%
```

Negative current = battery discharging (normal when not charging).

## Step 4: Verify Systemd Service

Already enabled by cloud-init. Check status:

```bash
sudo systemctl status ups-monitor
```

If not running:

```bash
sudo systemctl start ups-monitor
```

## Step 5: View Logs

```bash
sudo journalctl -u ups-monitor -f
```

## Note on Charging

The UPS HAT charges via its 8.4V jack. Power source:
```
5V Rail → USB 5V→8.4V converter cable → UPS HAT 8.4V input
```

When the main 14.4V battery is connected, the 5V rail is active, and the UPS HAT charges.

When main battery is disconnected (swap), the UPS HAT powers the RPi from its 18650 cells.

---

## Done

Proceed to `08-hotspot.md` (verify) or `09-verify.md`.
