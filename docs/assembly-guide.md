# Complete Assembly Guide

Step-by-step instructions for assembling the Raspberry Pi 5 DJ Display System with motorized sliding walls.

## Before You Start

### Required Tools
- Soldering iron and solder
- Wire strippers
- Screwdrivers (Phillips and flathead)
- Multimeter
- Flush cutters
- Hot glue gun
- Helping hands/PCB holder
- Label maker or masking tape (for labeling wires)

### Required Materials
- All electronic components (see hardware_setup.md)
- 3D printed parts (see 3d-models/README.md)
- Wire (22-24 AWG, multiple colors)
- Heat shrink tubing
- Zip ties or velcro straps
- Dupont connectors (optional but recommended)
- Perfboard or PCB for transistor circuits
- Super glue or plastic cement

### Safety Equipment
- Safety glasses (for soldering)
- Well-ventilated workspace
- Fire-safe soldering surface
- First aid kit nearby

## Assembly Overview

**Estimated Total Time:** 15-20 hours over several days

**Recommended Order:**
1. 3D printing (40-60 hours, can run unattended)
2. Breadboard testing (2-3 hours)
3. Transistor circuit assembly (2-3 hours)
4. Display connections (2-3 hours)
5. Arduino and stepper wiring (2-3 hours)
6. Physical integration (3-4 hours)
7. Testing and debugging (2-3 hours)

---

## Phase 1: 3D Printing (Days 1-3)

### Step 1: Print Critical Components First

**Priority 1 (Start immediately):**
1. DJ booth main structure
2. Display mounting brackets
3. Motor mounts for sliding walls

**Priority 2 (While Priority 1 prints):**
1. Wall panels (3x)
2. Wall tracks
3. Limit switch brackets

**Priority 3 (Print last):**
1. Bar counter
2. Tables
3. Decorative elements

**Tips:**
- Print overnight when possible
- Check first layer adhesion before leaving
- Keep filament dry in sealed bags with desiccant

### Step 2: Post-Processing

While other parts print:
1. Remove supports from completed prints
2. Sand display cutouts to ensure smooth fit
3. Test-fit ILI9341 displays in mounting brackets
4. Test-fit motors in motor mounts

---

## Phase 2: Electronics Breadboard Testing (Day 3-4)

Before any permanent soldering, test everything on a breadboard.

### Step 1: Test Raspberry Pi Displays

**One display at a time:**

```bash
# Enable SPI
sudo raspi-config
# Interface Options → SPI → Enable

# Install libraries
pip3 install adafruit-circuitpython-rgb-display

# Test Display 1 (SPI0)
python3 examples/test_displays.py --display 1
```

**Connections for Display 1:**
```
Display VCC → Breadboard 3.3V rail (from ATX PSU)
Display GND → Breadboard GND rail
Display CS  → GPIO 23
Display RST → GPIO 25
Display DC  → GPIO 24
Display MOSI → GPIO 10
Display SCK → GPIO 11
```

**Verify:** Display should show test pattern

Repeat for displays 2 and 3 using pins from hardware_setup.md

### Step 2: Test LED Transistor Circuits

**Build one channel on breadboard:**

```
Breadboard Layout (Red Channel):

3.3V rail ─── 100Ω ─── Red LED Anode
                       Red LED Cathode ─── BC337 Collector
                                          BC337 Base ─── 1kΩ ─── GPIO 13
                                          BC337 Emitter ─── GND rail
```

**Test code:**

```python
from gpiozero import PWMLED
import time

red = PWMLED(13)

# Test full brightness
red.on()
time.sleep(2)

# Test PWM dimming
for brightness in range(0, 101, 10):
    red.value = brightness / 100
    print(f"Brightness: {brightness}%")
    time.sleep(0.5)

red.off()
```

**Verify:** LED should smoothly dim from 0-100%

Repeat for green (GPIO 19) and blue (GPIO 5) channels.

### Step 3: Test Arduino Stepper Control

**Connections:**

```
Arduino D2-D5 → Motor 1 ULN2003 IN1-IN4
Motor VCC → 5V
Motor GND → GND
```

**Test code:**

```cpp
#include <Stepper.h>

const int stepsPerRevolution = 2048;
Stepper motor1(stepsPerRevolution, 2, 4, 3, 5);

void setup() {
  motor1.setSpeed(10);
  Serial.begin(9600);
}

void loop() {
  Serial.println("Forward");
  motor1.step(stepsPerRevolution);
  delay(1000);
  
  Serial.println("Backward");
  motor1.step(-stepsPerRevolution);
  delay(1000);
}
```

**Verify:** Motor should turn smoothly in both directions

---

## Phase 3: Permanent Soldering (Day 4-5)

### Step 1: Build Transistor LED Driver Board

**Use perfboard or custom PCB:**

**Layout (for one channel):**
```
[GPIO Pin Pad] ─── [1kΩ Resistor] ─── [BC337 Base]
                                      [BC337 Emitter] ─── [GND Pad]
                                      [BC337 Collector] ─── [LED- Pad]

[3.3V Pad] ─── [100Ω Resistor] ─── [LED+ Pad]
```

**Build order:**
1. Mark and drill holes for mounting screws
2. Place all BC337 transistors (watch orientation!)
3. Solder emitters to GND rail
4. Add 1kΩ resistors to base pins
5. Solder collectors to LED output pads
6. Add 100Ω resistors to 3.3V rail
7. Add screw terminals or wire pads for connections

**Test each channel** before proceeding to next.

### Step 2: Solder Display Connections

**Use ribbon cable or individual wires:**

**For each display:**
1. Cut wires to appropriate length (+10cm extra)
2. Strip and tin wire ends
3. Solder to display pins (use flux for clean joints)
4. Add heat shrink tubing over each joint
5. Label each wire clearly (use label maker)

**Color coding suggestion:**
- VCC: Red
- GND: Black
- MOSI: Orange
- SCK: Yellow
- CS: Green
- DC: Blue
- RST: White

**Strain relief:**
- Hot glue wires to display PCB edge
- Leave small service loop near display

### Step 3: Arduino Stepper Wiring

**Andrej's section - document as completed**

Recommend:
1. Use Dupont connector housings for removability
2. Label each motor connector (Motor 1, 2, 3)
3. Use ribbon cable for organized routing
4. Add strain relief at Arduino pins

---

## Phase 4: Power Supply Setup (Day 5)

### Step 1: Prepare ATX PSU

**SAFETY WARNING:** Unplug ATX PSU before working inside!

**ATX Power-On:**
1. Locate 24-pin ATX connector
2. Find GREEN wire (PS_ON)
3. Find any BLACK wire (GND)
4. Short GREEN to BLACK with 18-22 AWG wire
5. Insulate connection with heat shrink

**Add screw terminals for easy access:**
1. Identify wires needed:
   - 3.3V (Orange) - need 2-3 wires
   - 5V (Red) - need 2-3 wires
   - GND (Black) - need 5+ wires
2. Bundle same-voltage wires together
3. Solder to screw terminal blocks
4. Label clearly: "3.3V", "5V", "GND"
5. Secure terminal block to PSU case

**Test output voltages with multimeter:**
- 3.3V rail: Should read 3.20-3.45V
- 5V rail: Should read 4.90-5.15V
- No shorts between any rails

### Step 2: Create Common Ground

**Critical for proper operation!**

```
Pi GPIO GND (Pin 6) ─── 18 AWG wire ─── ATX PSU GND terminal
                                       Arduino GND
                                       Transistor board GND
                                       Display GND
```

**Use a ground distribution block or terminal:**
1. One thick wire from ATX PSU GND
2. Multiple branches to all components
3. Star-ground configuration (all grounds meet at one point)

---

## Phase 5: Physical Integration (Day 6)

### Step 1: Mount Displays in DJ Booth

1. **Test fit** displays in 3D printed mounts
2. If too tight, sand cutouts slightly
3. Apply small amount of hot glue to edges
4. Press display into mount
5. Allow glue to cool fully before handling
6. Route display cables through cable channels
7. Mount assembled displays in booth front panel

### Step 2: Install LEDs

**Stage lighting placement:**
1. Mark LED positions on booth sides
2. Drill small holes for LED leads
3. Insert LEDs from inside
4. Secure with hot glue
5. Connect to transistor board outputs
6. Test before permanent mounting

### Step 3: Assemble Sliding Wall Mechanism

**Follow 3d-models/sliding-walls/assembly-instructions.pdf**

**Summary:**
1. Install wall tracks on base platform
2. Mount stepper motors in motor mounts
3. Attach gear system (Filip's design)
4. Test manual sliding motion (should be smooth)
5. Connect motors to gears
6. Install limit switches at top/bottom positions
7. Test motor movement without Arduino
8. Connect to Arduino and test with code

### Step 4: Cable Management

1. Bundle similar cables together with zip ties
2. Route power cables separately from signal cables
3. Leave slack for maintenance (service loops)
4. Label everything!
5. Secure cables to structure with cable clips or hot glue

---

## Phase 6: Final Assembly & Testing (Day 7)

### Step 1: System Integration Checklist

**Before power-on:**

- [ ] All ground connections verified with multimeter (continuity)
- [ ] No short circuits between power rails
- [ ] All transistors oriented correctly (C-B-E)
- [ ] LED polarities correct (anode to resistor, cathode to transistor)
- [ ] Display ribbon cables seated properly
- [ ] Stepper motor connectors secure
- [ ] ATX PSU power-on jumper installed
- [ ] Raspberry Pi SD card inserted with OS
- [ ] All Python dependencies installed
- [ ] Arduino code uploaded

### Step 2: First Power-On

**Power-on sequence:**

1. **Connect Raspberry Pi PSU** (do NOT turn on yet)
2. **Connect ATX PSU to wall power** (do NOT switch on yet)
3. **Double-check all connections**
4. **Turn on ATX PSU** - should hear fan spin
5. **Measure voltages:** 3.3V and 5V rails with multimeter
6. **If voltages correct, turn on Raspberry Pi**
7. **Boot and verify Pi starts normally**

**If anything smokes, sparks, or smells burning: IMMEDIATELY POWER OFF**

### Step 3: Component Testing

**Test in this order:**

**A. Displays:**
```bash
cd ~/rpi5-dj-display
python3 examples/test_displays.py
```
All three displays should show test patterns.

**B. LEDs:**
```bash
python3 examples/test_leds.py
```
All three colors should fade smoothly.

**C. Audio Playback:**
1. Pair Bluetooth speaker
2. Play test audio file
3. Verify sound output

**D. Arduino Motors:**
1. Open Arduino Serial Monitor
2. Press UP button
3. Walls should move up until limit switch
4. Press DOWN button
5. Walls should move down until limit switch

### Step 4: Full System Test

**Run complete show:**

```bash
python3 show_videos_2_music.py
```

**Verify:**
- All displays show synchronized video
- Audio plays through Bluetooth speaker
- LEDs react to music
- Lights change modes every 12 seconds
- No flickering or glitches

**Adjust if needed:**
- `BLUETOOTH_DELAY` for audio sync
- `BOOST` for LED brightness
- Display brightness (if supported)

### Step 5: Calibration

**Audio/Light Sync:**
1. Play music with strong bass kicks
2. Observe LED flash timing vs audio
3. Adjust `BLUETOOTH_DELAY` by 0.05s increments
4. Repeat until perfectly synced

**Wall Travel:**
1. Manually test full wall travel
2. Verify limit switches stop motion
3. Adjust switch position if needed
4. Test emergency stop (unplug Arduino)

---

## Phase 7: Final Touches (Day 7-8)

### Decorating the Club

**Collaborate with Gradezna Struka team:**
1. Paint 3D printed parts (optional)
2. Add miniature furniture
3. Place decorative bottles on bar
4. Add wall decorations
5. Final lighting adjustments

### Photography

**Document your build:**
1. Front view with all displays on
2. Side angle showing depth
3. Top-down view of layout
4. Closeup of displays
5. LEDs in action (different colors)
6. Sliding walls mid-motion
7. Team photo with finished project!

### Final Checklist

- [ ] All components working reliably
- [ ] No loose wires or connections
- [ ] Cable management clean
- [ ] All parts securely mounted
- [ ] Documentation complete
- [ ] Code commented and clean
- [ ] GitHub repository updated
- [ ] Photos/videos taken
- [ ] Ready for MASSUM presentation!

---

## Troubleshooting

### Common Issues

**Display shows garbage:**
- Check SPI is enabled in raspi-config
- Verify correct pins used
- Try lowering baudrate to 20MHz

**LEDs not responsive:**
- Verify transistor orientation
- Check 3.3V supply voltage
- Test individual GPIO with simple script

**Audio/Video out of sync:**
- Increase/decrease `BLUETOOTH_DELAY`
- Check Bluetooth buffer settings
- Try wired speaker instead

**Motor not turning:**
- Check 5V supply to ULN2003
- Verify all 4 coil wires connected
- Test with simple Arduino sketch

**Pi overheating:**
- Add heatsink or fan
- Check ambient temperature
- Reduce display refresh rate
- Close unnecessary processes

### Getting Help

1. Check documentation in `docs/` folder
2. Review `hardware_setup.md` wiring
3. Open GitHub issue with:
   - Clear description of problem
   - Photos of affected area
   - Error messages (if any)
   - What you've already tried

---

## Maintenance

### Regular Checks
- Clean dust from displays weekly
- Check wire connections monthly
- Update software as needed
- Backup SD card regularly

### Storage
- Power off properly (no sudden unplugs)
- Store in dry, dust-free location
- Remove batteries if storing long-term
- Protect displays from scratches

---

## Congratulations! 🎉

You've built a complete DJ display system with:
- ✅ Triple synchronized displays
- ✅ Audio-reactive LED lighting
- ✅ Motorized sliding walls
- ✅ Professional club environment
- ✅ Full software integration

**Team effort by:**
- Kiril Cvetkov (Software & Raspberry Pi)
- Andrej Trendov (Arduino & Motors)
- Filip Mihailov (Mechanical Design)
- Kire Angelov (CAD Modeling)
- Gradezna Struka (Original Design)

**Built for MASSUM 2025**

---

*Last updated: April 2025*
