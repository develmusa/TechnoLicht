#!/usr/bin/env python3
"""
Waveshare UPS HAT Battery Monitor
Reads voltage, current, power, and percentage via I2C (INA219).
Address: 0x42
"""

import time
import smbus2
from smbus2 import SMBus

# INA219 Registers
REG_CONFIG = 0x00
REG_SHUNT_VOLTAGE = 0x01
REG_BUS_VOLTAGE = 0x02
REG_POWER = 0x03
REG_CURRENT = 0x04
REG_CALIBRATION = 0x05

# I2C Configuration
I2C_BUS = 1
I2C_ADDR = 0x42

# Calibration for 0.1 ohm shunt, 3.2A max
CALIBRATION_VALUE = 0x2000


def ina219_init(bus):
    """Initialize INA219."""
    bus.write_word_data(I2C_ADDR, REG_CALIBRATION, CALIBRATION_VALUE)
    # Config: 32V, 1.1A, 12-bit, 1 sample, continuous
    config = 0x399F
    bus.write_word_data(I2C_ADDR, REG_CONFIG, config)


def read_voltage(bus):
    """Read bus voltage in volts."""
    raw = bus.read_word_data(I2C_ADDR, REG_BUS_VOLTAGE)
    # Swap bytes (INA219 is big-endian)
    raw = ((raw & 0xFF) << 8) | (raw >> 8)
    voltage = (raw >> 3) * 0.004
    return voltage


def read_current(bus):
    """Read current in milliamps."""
    raw = bus.read_word_data(I2C_ADDR, REG_CURRENT)
    raw = ((raw & 0xFF) << 8) | (raw >> 8)
    current = raw * 0.1
    return current


def read_power(bus):
    """Read power in watts."""
    raw = bus.read_word_data(I2C_ADDR, REG_POWER)
    raw = ((raw & 0xFF) << 8) | (raw >> 8)
    power = raw * 0.002
    return power


def estimate_percentage(voltage):
    """Estimate battery percentage from voltage (2S Li-ion: 6.0V - 8.4V)."""
    min_v = 6.0
    max_v = 8.4
    pct = (voltage - min_v) / (max_v - min_v) * 100
    return max(0, min(100, pct))


def main():
    bus = SMBus(I2C_BUS)
    ina219_init(bus)

    try:
        while True:
            voltage = read_voltage(bus)
            current = read_current(bus)
            power = read_power(bus)
            pct = estimate_percentage(voltage)

            print(f"Voltage: {voltage:.2f} V")
            print(f"Current: {current:.1f} mA")
            print(f"Power: {power:.2f} W")
            print(f"Percentage: {pct:.0f}%")
            print("-" * 20)

            time.sleep(30)
    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        bus.close()


if __name__ == "__main__":
    main()
