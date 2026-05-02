# 07 — UPS HAT Setup

Goal: Monitor battery voltage, current, and percentage via I2C.

## Step 1: Verify I2C Detection

```bash
sudo i2cdetect -y 1
```

You should see `42` in the output.

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

## Step 4: Install Systemd Service

```bash
sudo cp ~/TechnoLicht/config/ups-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ups-monitor.service
sudo systemctl start ups-monitor.service
```

## Step 5: Verify Service

```bash
sudo systemctl status ups-monitor
```

## Step 6: View Logs

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

## Done

Proceed to `08-hotspot.md` (optional) or `09-verify.md`.
