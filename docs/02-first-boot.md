# 02 — First Boot Setup

Run all commands as `pi` user (or prefix with `sudo`).

## Step 1: Update System

```bash
sudo apt update
sudo apt full-upgrade -y
```

## Step 2: Install Essentials

```bash
sudo apt install -y \
  git \
  i2c-tools \
  python3-pip \
  alsa-utils \
  vim \
  htop
```

## Step 3: Enable I2C (for UPS HAT)

```bash
sudo raspi-config nonint do_i2c 0
```

Verify after reboot:
```bash
sudo i2cdetect -y 1
```
You should see `42` in the grid (UPS HAT address).

## Step 4: Copy Repo to Pi

From your computer:
```bash
scp -r /path/to/TechnoLicht pi@technolight-pi.local:/home/pi/
```

Or clone from git if you pushed:
```bash
git clone <your-repo-url> ~/TechnoLicht
```

## Step 5: Reboot

```bash
sudo reboot
```

## Done

Proceed to `03-network.md`.
