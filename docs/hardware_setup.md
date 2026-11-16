# Hardware Setup Guide

## System overview

The project has three parts:

1. **Raspberry Pi 5**: video on three displays and the audio-reactive stage lights
2. **Arduino Nano**: motorized sliding walls *(documentation in progress)*
3. **Physical club model**: the 3D printed booth, bar, tables and walls *(models in progress)*

---

## Raspberry Pi 5

### Displays

Three ILI9341 240×320 displays, each on its own SPI bus.

| Display | SPI bus | MOSI | SCK | CS | DC | RST |
|---------|---------|------|-----|----|----|-----|
| 1 | SPI0 | GPIO 10 | GPIO 11 | GPIO 23 | GPIO 24 | GPIO 25 |
| 2 | SPI1 | GPIO 20 | GPIO 21 | – | GPIO 17 | GPIO 18 |
| 3 | SPI5 | GPIO 14 | GPIO 15 | – | GPIO 6 | GPIO 26 |

#### ILI9341 pinout

```
Display pin → Raspberry Pi / ATX PSU
──────────────────────────────────────
VCC  → 3.3V (from the ATX PSU 3.3V rail)
GND  → Ground
CS   → Chip Select (see table above)
RST  → Reset (see table above)
DC   → Data/Command (see table above)
MOSI → SPI MOSI (see table above)
SCK  → SPI Clock (see table above)
LED  → 3.3V (backlight), optionally through a current-limiting resistor
MISO → Not connected
```

**Notes:**
- All displays are powered from the ATX PSU 3.3V rail, not from the Pi's 3.3V pin.
- Each display has its own DC and RST pins.
- Displays 2 and 3 are driven without a CS pin (`cs=None` in `dj_show.py`).

---

### Audio-reactive stage lights (3.3 V)

Small 3.3 V RGB LEDs are placed around the stage and in the bars. The Pi controls them with PWM through three BC337 NPN transistors, one per colour. The LEDs in the bars use the same wiring as the stage LEDs.

#### GPIO pins

```
LED channel → GPIO pin → Transistor
─────────────────────────────────────
Red         → GPIO 13  → BC337 (Q1)
Green       → GPIO 19  → BC337 (Q2)
Blue        → GPIO 5   → BC337 (Q3)
```

**Why transistors?** A GPIO pin can only supply a few milliamps. The transistor lets the ATX PSU's 3.3 V rail supply the LED current, while the GPIO pin only switches it.

#### BC337 pinout (TO-92)

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

#### One channel (e.g. red)

```
3.3V (ATX) ─── 100Ω ─── LED anode
                        LED cathode ─── BC337 collector (C)
                                        BC337 base (B) ─── 1kΩ ─── GPIO 13
                                        BC337 emitter (E) ─── GND
```

Green (GPIO 19, Q2) and blue (GPIO 5, Q3) are wired the same way.

| Component | Value | Purpose |
|-----------|-------|---------|
| Base resistor | 1 kΩ | Limits the current from the GPIO pin into the transistor base |
| LED resistor | 47–100 Ω | Limits the LED current (one per LED) |
| BC337 | NPN, up to 800 mA | Switches the LED current |

#### Several LEDs per channel

The stage and bar LEDs of one colour are connected in parallel, each with its own resistor:

```
              ┌─ 100Ω ─ LED1 ─┐
3.3V ─────────┼─ 100Ω ─ LED2 ─┼─── BC337 collector
              └─ 100Ω ─ LED3 ─┘
```

Don't connect LEDs in series: 3.3 V is not enough to light two LEDs in a row.

#### Testing the LEDs

```python
from gpiozero import PWMLED
import time

red, green, blue = PWMLED(13), PWMLED(19), PWMLED(5)

for led in (red, green, blue):
    led.value = 0.5   # 50% brightness
    time.sleep(2)
    led.off()

# All three on = white
red.on(); green.on(); blue.on()
```

---

### 12 V LED strip (ambient lighting)

A standard 12 V LED strip with its own remote controller gives the club its ambient light. It is powered from the ATX PSU 12 V rail and is **not** connected to the Raspberry Pi. Effects such as strobe and flash are selected with the strip's remote.

```
ATX 12V (yellow) ─── LED strip controller ─── 12V LED strip
ATX GND (black)  ─── LED strip controller
```

---

## Arduino Nano: motorized sliding walls

> 🚧 **Work in progress.** The Arduino code, wiring diagram and pin list for the sliding walls will be added later.

Parts used: Arduino Nano, 3× 28BYJ-48 stepper motors with ULN2003 driver boards, control buttons and limit switches, all powered from the ATX PSU 5 V rail.

---

## Power distribution

Two separate power supplies are used:

1. **Official Raspberry Pi 27 W USB-C PSU (5 V, 5 A)**: powers only the Raspberry Pi 5.
2. **ATX PSU** (repurposed from an old PC): powers everything else.

| ATX rail | Wire colour | Powers |
|----------|-------------|--------|
| +3.3 V | Orange | ILI9341 displays, stage and bar RGB LEDs (through the BC337s) |
| +5 V | Red | Arduino Nano, ULN2003 stepper drivers |
| +12 V | Yellow | LED strip with remote controller |
| GND | Black | Common ground, also connected to the Pi |

```
┌───────────────────────────────┐
│     Official Pi 27W PSU       │──→ Raspberry Pi 5 (USB-C)
└───────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                     ATX PSU (repurposed)                      │
├──────────────┬──────────────┬───────────────┬────────────────┤
│ +3.3V        │ +5V          │ +12V          │ GND            │
└──────┬───────┴──────┬───────┴───────┬───────┴───────┬────────┘
       │              │               │               │
       ├→ 3× ILI9341  ├→ Arduino Nano └→ LED strip    ├→ all components
       │   displays   │                  controller   │
       └→ RGB LEDs    └→ 3× ULN2003                   └→ Pi GND (required!)
          (via BC337)     stepper drivers
```

### Turning on an ATX PSU without a motherboard

1. Find the **green** wire (PS_ON, pin 16) on the 24-pin connector.
2. Connect it to any **black** wire (GND) with a short piece of insulated wire.
3. The PSU now turns on as soon as it is switched on at the mains.

Don't run the PSU with nothing connected. Keep its fan unobstructed.

### Common ground

The Pi's GND **must** be connected to the ATX PSU's GND. Without it the transistors have no shared reference and the LEDs won't switch reliably.

- Use any GND pin on the Pi header: 6, 9, 14, 20, 25, 30, 34 or 39.
- Use a thick wire (18–22 AWG) and keep it short.

---

## 3D printed parts

The DJ booth, bar counter, tables and sliding wall mechanisms are 3D printed. The model files are not published yet. See [3d-models/README.md](../3d-models/README.md).

---

## Safety

⚠️ **Electrical**
- Never connect or disconnect parts while the power is on.
- An ATX PSU contains mains voltage inside. Never open its case.
- Use wire thick enough for the current, and fuses on high-current lines.

⚠️ **Mechanical**
- Keep fingers away from the sliding walls while the motors are running.
- Check that the limit switches stop the walls before running a full show.

⚠️ **Thermal**
- Keep the Raspberry Pi below 80 °C (`vcgencmd measure_temp`).
- Make sure the ATX PSU fan is working.

---

## Troubleshooting power

**The Pi won't boot:** use the official 27 W PSU and a good USB-C cable.

**Displays flicker:** measure the voltage at the display VCC pin (it should be 3.3 V ± 0.2 V). A 100 µF capacitor near the display power pins helps.

**LEDs dim or uneven:** check the transistor orientation, the 3.3 V supply, the resistor values and the common ground.

**Steppers don't move:** check the 5 V supply to the ULN2003 boards and the IN1–IN4 connections.

**The ATX PSU won't turn on:** check the green-to-black jumper and the PSU's mains switch, and make sure something is connected as a load.

---

For the build order and test steps, see [assembly-guide.md](assembly-guide.md).
