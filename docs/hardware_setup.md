# Hardware Setup Guide

## System Overview

This project consists of three main components:
1. **Raspberry Pi 5** - Video playback and LED control
2. **Arduino Nano** - Motorized sliding wall control
3. **Physical Stage Setup** - 3D printed club environment

---

## Raspberry Pi 5 Setup

### Display Connections

#### SPI Bus Assignment

The Raspberry Pi 5 has multiple SPI buses. This project uses:
- **SPI0** - Primary SPI bus (CE0/CE1)
- **SPI1** - Secondary SPI bus
- **SPI5** - Additional SPI bus

#### Pin Mapping Reference

| Display | SPI Bus | MOSI | SCK | CS | DC | RST |
|---------|---------|------|-----|----|----|-----|
| 1 | SPI0 | GPIO 10 | GPIO 11 | GPIO 23 | GPIO 24 | GPIO 25 |
| 2 | SPI1 | GPIO 20 | GPIO 21 | - | GPIO 17 | GPIO 18 |
| 3 | SPI5 | GPIO 14 | GPIO 15 | - | GPIO 6 | GPIO 26 |

#### ILI9341 Display Pinout

```
Display Pin → Raspberry Pi / ATX PSU
──────────────────────────────────────
VCC  → 3.3V (from ATX PSU 3.3V rail)
GND  → Ground
CS   → Chip Select (see table above)
RST  → Reset (see table above)
DC   → Data/Command (see table above)
MOSI → SPI MOSI (see table above)
SCK  → SPI Clock (see table above)
LED  → 3.3V (backlight) via current-limiting resistor (optional)
MISO → Not connected
```

**Important Notes:**
- All displays powered from ATX PSU 3.3V rail (not Raspberry Pi 3.3V)
- All displays share the same power rails (3.3V and GND from ATX PSU)
- Each display has independent control pins (CS, RST, DC)
- SPI1 and SPI5 do not use CS pins (handled in software)

---

### LED Stage Lighting

The system uses RGB LEDs for audio-reactive stage lighting controlled via BC337 NPN transistors.

#### GPIO Pin Assignment

```
LED Channel → GPIO Pin → Transistor
─────────────────────────────────────
Red         → GPIO 13  → BC337 (Q1)
Green       → GPIO 19  → BC337 (Q2)
Blue        → GPIO 5   → BC337 (Q3)
```

#### BC337 Transistor Configuration

**Why BC337 Transistors?**
- Allows switching higher current LEDs/LED strips
- Protects GPIO pins from overcurrent
- Enables 12V LED operation from 3.3V GPIO signals
- Each GPIO can safely drive the transistor base

**BC337 Pinout (TO-92 Package):**
```
   ___
  |   |  Flat side facing you
  |___|
   | | |
   C B E

C = Collector
B = Base
E = Emitter
```

#### Wiring Diagram - Transistor LED Driver

**For each color channel (Red, Green, Blue):**

```
Raspberry Pi GPIO → Base Resistor → BC337 Base
                                    BC337 Emitter → Ground
                                    BC337 Collector → LED Cathode
                                    LED Anode → Current-limiting Resistor → 3.3V Supply

Complete circuit for one channel (e.g., Red):

3.3V+ ────┬─── 100Ω ─── LED Anode
          │
          └─ (to other LEDs in parallel if using multiple)

LED Cathode ─── BC337 Collector (Pin C)
                BC337 Base (Pin B) ─── 1kΩ ─── GPIO 13
                BC337 Emitter (Pin E) ─── Ground
```

**Component Values:**

| Component | Value | Purpose |
|-----------|-------|---------|
| Base Resistor (R1) | 1kΩ | Limits current into BC337 base from GPIO |
| LED Current Resistor (R2) | 47Ω - 100Ω | Limits LED current (calculate based on LED specs) |
| BC337 Transistor | NPN, hFE ~100-250 | Switches LED current |

#### Complete 3-Channel RGB Wiring

```
Power Distribution:
─────────────────────
ATX PSU 3.3V rail → Common LED anode supply
ATX PSU GND → Common ground with Raspberry Pi

Red Channel:
───────────
GPIO 13 → 1kΩ → BC337 Q1 Base
                BC337 Q1 Emitter → GND
                BC337 Q1 Collector → Red LED Cathode
Red LED Anode → 100Ω → 3.3V

Green Channel:
─────────────
GPIO 19 → 1kΩ → BC337 Q2 Base
                BC337 Q2 Emitter → GND
                BC337 Q2 Collector → Green LED Cathode
Green LED Anode → 100Ω → 3.3V

Blue Channel:
────────────
GPIO 5 → 1kΩ → BC337 Q3 Base
               BC337 Q3 Emitter → GND
               BC337 Q3 Collector → Blue LED Cathode
Blue LED Anode → 100Ω → 3.3V

Common Ground Connection:
────────────────────────
Raspberry Pi GND ←→ ATX PSU GND (CRITICAL for proper operation)
```

#### LED Current Calculation

For standard 5mm LEDs at 3.3V:

**Red LED (typical forward voltage: 2V):**
```
Resistor = (3.3V - 2V) / 20mA = 65Ω → Use 68Ω or 82Ω
```

**Green/Blue LED (typical forward voltage: 3V):**
```
Resistor = (3.3V - 3V) / 20mA = 15Ω → Use 22Ω or 47Ω
```

**For high-power LEDs:**
- Adjust resistor values based on LED specifications
- 3.3V rail limits brightness - suitable for indicator/stage LEDs
- BC337 can handle up to 800mA continuous

#### Multiple LEDs per Channel

To connect multiple LEDs per color in parallel (same forward voltage):

```
                    ┌─ 100Ω ─ LED1 ─┐
3.3V ──────────────┼─ 100Ω ─ LED2 ─┼─── BC337 Collector
                    └─ 100Ω ─ LED3 ─┘

Each LED gets its own current-limiting resistor
```

> **Note:** Series connection is not recommended at 3.3V due to insufficient voltage headroom.

---

### Testing LED Connections

#### Test Individual Transistor Channel

```python
from gpiozero import PWMLED
import time

# Test Red channel
red = PWMLED(13)
red.value = 0.5  # 50% brightness
time.sleep(2)
red.off()

# Test Green channel
green = PWMLED(19)
green.pulse()  # Fade in/out
time.sleep(5)
green.off()

# Test Blue channel
blue = PWMLED(5)
blue.on()  # Full brightness
time.sleep(2)
blue.off()
```

#### Test All Channels (White)

```python
from gpiozero import PWMLED

red = PWMLED(13)
green = PWMLED(19)
blue = PWMLED(5)

# White = all channels on
red.on()
green.on()
blue.on()

# Adjust brightness
red.value = 0.8
green.value = 0.8
blue.value = 0.8
```

---

## Arduino Nano - Motorized Sliding Walls



---

## Power Distribution

### Overview

The system uses two separate power supplies:
1. **Official Raspberry Pi 5V 5A PSU** - Powers only the Raspberry Pi 5
2. **12V ATX PSU** (repurposed from old PC) - Powers servos, lights, and displays

### Power Supply Specifications

#### Raspberry Pi Power Supply

```
Type: Official Raspberry Pi 27W USB-C Power Supply
Voltage: 5V DC
Current: 5A (27W)
Powers:
  - Raspberry Pi 5 mainboard
  - USB peripherals (if any)
  
Do NOT power displays, LEDs, or Arduino from this supply
```

#### 12V ATX Power Supply

```
Type: Standard PC ATX PSU (repurposed)
Minimum Rating: 200W
Key Rails:
  - +3.3V rail → RGB LEDs, ILI9341 displays
  - +5V rail → Arduino Nano, stepper motors
  - GND (Black wires) → Common ground

Typical ATX Wire Colors:
  Orange  = +3.3V
  Red     = +5V
  Yellow  = +12V (not used in this project)
  Black   = Ground
  Green   = Power-on (short to GND to turn on PSU)
```

### ATX PSU Preparation

**To use ATX PSU without motherboard:**

1. Locate the 24-pin ATX connector
2. Find the **GREEN** wire (PS_ON signal)
3. Find any **BLACK** wire (Ground)
4. Short GREEN to BLACK using a jumper wire or paperclip
5. PSU will turn on when AC power is connected

```
ATX 24-Pin Connector (view from wire side):

        ┌─────────────────────┐
        │ ● ● ● ● ● ● ● ● ● ● │
        │  ● ● ● ● ● ● ● ● ● ●│
        └─────────────────────┘
           Pin 16 (Green - PS_ON)
           Short to any Black (GND)
```

**Safety:**
- Never run ATX PSU without any load
- Connect at least one device before powering on
- Ensure adequate ventilation
- Keep PSU fan unobstructed

### Power Distribution Diagram

```
POWER DISTRIBUTION:

┌─────────────────────────────────────────────────────────────┐
│                    Official Pi 5V 5A PSU                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         └─→ Raspberry Pi 5 (USB-C)
                         

┌─────────────────────────────────────────────────────────────┐
│                      12V ATX PSU (Repurposed)               │
├─────────────────────────────────────────────────────────────┤
│  +3.3V Rail (Orange)   │  +5V Rail (Red)  │  GND (Black)    │
└────────┬───────────────┴──────────┬───────┴────────┬────────┘
         │                          │                 │
         ├─→ RGB LEDs               ├─→ Arduino Nano  ├─→ Common GND
         │   (via BC337)            │                 │
         │                          ├─→ 3x ULN2003    │
         ├─→ 3x ILI9341 Displays    │   Stepper       │
         │   (VCC pins)             │   Drivers       │
         │                          │                 │
         └─→ Display Backlights     │                 │
             (LED pins)             │                 │
                                    └─────────────────┴─→ Pi GND
                                          (CRITICAL!)
```

### Current Budget

**ATX PSU Loads:**

| Component | Voltage | Current (max) | Power |
|-----------|---------|---------------|-------|
| RGB LEDs (3 channels) | 3.3V | 180mA | 0.6W |
| 3x ILI9341 Displays | 3.3V | 150mA | 0.5W |
| Arduino Nano | 5V | 50mA | 0.25W |
| 3x Stepper Motors | 5V | 600mA | 3W |
| **Total** | - | **~1A** | **~4.35W** |

**Minimum ATX PSU Rating:** 200W (provides significant headroom)

### Critical Grounding

**IMPORTANT:** Common ground between Raspberry Pi and 12V ATX PSU is essential for proper operation.

```
Connection:
  Raspberry Pi GND pin (any GND on 40-pin header)
    ↕
  12V ATX PSU Black wire (GND)

Why this matters:
  - BC337 transistors need common reference
  - Prevents ground loops
  - Ensures proper signal levels
  - Protects against voltage spikes
```

**Recommended Ground Connection:**
1. Use a thick wire (18-22 AWG)
2. Keep connection short (<30cm if possible)
3. Connect to GPIO header pins 6, 9, 14, 20, 25, 30, 34, or 39 (all GND)
4. Alternatively, use USB GND if accessible

---

## Physical Stage Construction

### 3D Printed Components

The complete club environment consists of 3D printed models:
- **DJ Booth** - Main performance area with display cutouts
- **Bar Counter** - Club bar setup with LED mounts
- **Tables** - Audience seating areas
- **Sliding Wall Mechanisms** - Motorized wall tracks and mounts

All 3D model files (.STL, .STEP) are available in the [`3d-models/`](../3d-models/) directory.

#### Printing Recommendations

| Component | Material | Infill | Supports | Layer Height |
|-----------|----------|--------|----------|--------------|
| DJ Booth Main | PLA/PETG | 20% | Yes | 0.2mm |
| Display Mounts | PLA | 40% | No | 0.15mm |
| Bar Counter | PLA | 15% | Yes | 0.2mm |
| Tables | PLA | 15% | No | 0.2mm |
| Wall Panels | PLA | 10% | No | 0.2mm |
| Motor Mounts | PETG | 50% | Yes | 0.2mm |

See [`3d-models/README.md`](../3d-models/README.md) for detailed printing instructions and assembly guides.

---

## Assembly Notes

### Step-by-Step Assembly Order

1. **3D Print all components** (40-60 hours total)
2. **Wire Raspberry Pi displays** on breadboard first (test before soldering)
3. **Build transistor LED driver circuits** on perfboard/PCB
4. **Test each display individually** before mounting
5. **Mount displays in DJ booth** front panel cutouts
6. **Position RGB LEDs** for optimal stage lighting coverage
7. **Assemble sliding wall mechanisms** with motor mounts
8. **Install limit switches** at top/bottom wall positions
9. **Wire Arduino and stepper motors**
10. **Connect power supplies** (Pi first, then ATX)
11. **Test steppers individually** before full assembly
12. **Cable management** - route Pi and Arduino cables separately
13. **Final integration test**

### Cable Management Tips

- Use zip ties or velcro straps for bundling
- Separate power cables from signal cables
- Label all connections (use label maker or tape)
- Leave slack for maintenance access
- Route high-current wires away from display ribbon cables

### Testing Checklist

**Before First Power-On:**
- [ ] Verify all ground connections
- [ ] Check polarity of all power connections
- [ ] Ensure no short circuits (use multimeter)
- [ ] Verify transistor orientation (C-B-E)
- [ ] Check LED polarity (anode/cathode)
- [ ] Confirm resistor values

**Individual Component Tests:**
- [ ] Each display shows test pattern
- [ ] Each LED channel responds to GPIO
- [ ] Each stepper motor turns smoothly
- [ ] Buttons register presses
- [ ] Limit switches trigger correctly
- [ ] Bluetooth speaker pairs and plays audio

**Integrated System Test:**
- [ ] All three displays synchronized
- [ ] LEDs react to music
- [ ] Walls move on button press
- [ ] Walls stop at limit switches
- [ ] No overheating components
- [ ] Audio/video sync is acceptable

---

## Safety Warnings

⚠️ **Electrical Safety:**
- Never connect/disconnect components while powered
- ATX PSU contains high voltage even when off - allow discharge time
- Use proper gauge wire for current requirements
- Add fuses to high-current circuits
- Ensure adequate cooling for all components

⚠️ **Mechanical Safety:**
- Secure all moving parts before testing steppers
- Keep fingers clear of sliding wall mechanism
- Ensure limit switches are properly positioned
- Test emergency stop functionality

⚠️ **Thermal Safety:**
- Monitor component temperatures during extended operation
- Add heatsinks to BC337 if handling >500mA
- Ensure ATX PSU fan is operational
- Keep Raspberry Pi temperature <80°C

---

## Troubleshooting Power Issues

**Raspberry Pi won't boot:**
- Check official PSU is 5V 5A rated
- Verify USB-C connection is secure
- Try different USB-C cable

**Displays flickering:**
- Check 3.3V supply from ATX PSU is stable
- Measure voltage at display VCC pin (should be 3.3V ±0.2V)
- Add 100µF capacitor near display power pins

**LEDs dim or uneven brightness:**
- Verify BC337 transistors are correctly oriented
- Check 3.3V supply voltage
- Measure resistor values
- Ensure common ground is connected

**Steppers not moving:**
- Check 5V supply to ULN2003 drivers
- Verify all IN1-IN4 connections
- Test with simple Arduino blink sketch
- Check motor wire connections to driver

**ATX PSU won't turn on:**
- Verify GREEN wire is shorted to BLACK (GND)
- Ensure at least one load is connected
- Check AC power switch on PSU (if present)
- Try different wall outlet

---

For additional assembly guidance with photos, see [`docs/assembly-guide.md`](assembly-guide.md).
