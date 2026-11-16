# Assembly guide

This is the order we recommend for building the miniature DJ club. Wiring details and pinouts are in [hardware_setup.md](hardware_setup.md).

## Before you start

### Tools
- Soldering iron and solder
- Wire strippers and flush cutters
- Screwdrivers
- Multimeter
- Hot glue gun
- Helping hands or a PCB holder
- Label maker or masking tape for labelling wires

### Materials
- The electronic parts listed in the Hardware section of the [README](../README.md)
- 3D printed parts (models in progress, see [3d-models/](../3d-models/))
- Wire (22 to 24 AWG, several colours) and heat-shrink tubing
- Zip ties or velcro straps
- Dupont connectors (optional, but they make repairs easier)
- Perfboard for the transistor circuit

### Safety
- Safety glasses while soldering
- A well-ventilated workspace and a fire-safe soldering surface

## Build order

1. Print the 3D parts
2. Test the displays and LEDs on a breadboard
3. Solder the transistor LED driver board
4. Solder the display wiring
5. Wire the Arduino and stepper motors
6. Prepare the ATX power supply and the common ground
7. Mount everything in the club model
8. Test and calibrate

## 1. 3D printing

Work in progress. The 3D model files and print instructions will be added to [3d-models/](../3d-models/) later.

After printing, remove the supports, sand the display cutouts until the displays fit, and test-fit the stepper motors in their mounts.

## 2. Breadboard testing

Test everything on a breadboard before soldering anything permanently.

### Displays

Enable SPI and install the requirements first (see the [README](../README.md)). Then wire one display at a time. Display 1:

```
Display VCC  → 3.3V rail (from the ATX PSU)
Display GND  → GND rail
Display CS   → GPIO 23
Display RST  → GPIO 25
Display DC   → GPIO 24
Display MOSI → GPIO 10
Display SCK  → GPIO 11
```

Check it with a solid-colour test:

```python
import board, busio, digitalio
from PIL import Image
import adafruit_rgb_display.ili9341 as ili9341

spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
display = ili9341.ILI9341(
    spi,
    cs=digitalio.DigitalInOut(board.D23),
    dc=digitalio.DigitalInOut(board.D24),
    rst=digitalio.DigitalInOut(board.D25),
    baudrate=40000000,
)
display.image(Image.new("RGB", (240, 320), (255, 0, 0)))  # whole screen red
```

Repeat for displays 2 and 3, using the pins from the [display table](hardware_setup.md#displays) and the `busio.SPI(...)` lines from `dj_show.py`.

### LED channel

Build one channel on the breadboard:

```
3.3V rail ─── 100Ω ─── red LED anode
                       red LED cathode ─── BC337 collector
                                           BC337 base ─── 1kΩ ─── GPIO 13
                                           BC337 emitter ─── GND rail
```

```python
from gpiozero import PWMLED
import time

red = PWMLED(13)
for brightness in range(0, 101, 10):
    red.value = brightness / 100
    print(f"Brightness: {brightness}%")
    time.sleep(0.5)
red.off()
```

The LED should fade smoothly from off to full. Repeat for green (GPIO 19) and blue (GPIO 5).

## 3. Transistor LED driver board

Build the three channels on perfboard:

```
[GPIO pad] ─── [1kΩ] ─── [BC337 base]
                         [BC337 emitter] ─── [GND pad]
                         [BC337 collector] ─── [LED− pad]

[3.3V pad] ─── [100Ω] ─── [LED+ pad]
```

1. Place the three BC337s. Watch the orientation (flat side, C-B-E).
2. Solder the emitters to a shared GND rail.
3. Add the 1 kΩ resistors to the bases.
4. Solder the collectors to the LED output pads.
5. Add screw terminals or wire pads for the connections.

Test each channel before moving on to the next one.

## 4. Display wiring

For each display:
1. Cut the wires about 10 cm longer than needed.
2. Strip and tin the wire ends.
3. Solder them to the display pins, then cover each joint with heat-shrink tubing.
4. Label every wire.
5. Hot-glue the wires to the edge of the display board for strain relief.

Suggested colours: VCC red, GND black, MOSI orange, SCK yellow, CS green, DC blue, RST white.

## 5. Arduino and stepper motors

Work in progress. Wiring and code for the sliding walls will be added later.

## 6. Power supply

Follow the [power distribution](hardware_setup.md#power-distribution) section of the hardware guide:

1. Install the green-to-black jumper so the ATX PSU turns on without a motherboard.
2. Bundle the wires of each rail you need (3.3 V orange, 5 V red, 12 V yellow, GND black) into labelled screw terminals.
3. Measure the outputs with a multimeter before connecting anything:
   - 3.3 V rail: 3.20 to 3.45 V
   - 5 V rail: 4.90 to 5.15 V
   - 12 V rail: 11.4 to 12.6 V
4. Connect the Pi GND to the ATX GND. Run all grounds to a single point.

## 7. Mounting

1. Displays: test-fit them in the booth, sand the cutouts if they are tight, fix them with a little hot glue, and route the cables through the cable channels.
2. Stage and bar LEDs: mark the positions, drill small holes, insert the LEDs from the inside, secure them with hot glue and connect them to the driver board. Test them before closing anything up.
3. 12 V LED strip: stick the strip where you want ambient light and connect it to its controller and the 12 V rail.
4. Sliding walls: work in progress.
5. Cables: keep power and signal cables apart, leave some slack for repairs, and label everything.

## 8. Testing and calibration

### Before the first power-on

- [ ] All grounds connected (check continuity with the multimeter)
- [ ] No shorts between the power rails
- [ ] Transistors oriented correctly (C-B-E)
- [ ] LED polarity correct (anode to resistor, cathode to transistor)
- [ ] Display wires seated properly
- [ ] ATX power-on jumper installed
- [ ] Raspberry Pi OS set up and requirements installed

### First power-on

1. Plug in the ATX PSU and switch it on. The fan should spin.
2. Measure the 3.3 V, 5 V and 12 V rails.
3. If the voltages are correct, power on the Raspberry Pi.

If anything smokes, sparks or smells burnt, switch everything off immediately.

### Component tests

1. Run the solid-colour test from step 2 on each display.
2. Run the LED test from step 2 for each colour.
3. Pair the Bluetooth speaker and play a test sound.
4. Switch on the LED strip with its remote and try the effects.

### Full show

```bash
source .venv/bin/activate
python3 dj_show.py
```

Check that all three displays show the video, the music plays through the Bluetooth speaker, and the LEDs react to the music and change mode every 12 seconds.

### Light and music sync

1. Play a song with strong bass kicks.
2. Watch whether the white flashes land on the kicks.
3. Adjust `BLUETOOTH_DELAY` in `dj_show.py` in steps of 0.05 s until they match.

For more fixes, see the troubleshooting sections in the [README](../README.md) and in [hardware_setup.md](hardware_setup.md).
