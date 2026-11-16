# MASSUM 2026: Miniature DJ Club

A miniature DJ club built for the MASSUM 2026 competition by a student team at DSU RCSOO Nikola Karev, Strumica, North Macedonia.

A Raspberry Pi 5 plays a video on three small screens in the DJ booth while a Bluetooth speaker plays the music. RGB stage lights react to the song. The track is analysed before playback, so the lights know where the bass hits and how loud each part of the song is. An Arduino Nano drives the motorized sliding walls.

Photos coming soon.

## Features

- The same video plays on three ILI9341 displays (240x320) in the DJ booth.
- Before playback, the song is split into short chunks and analysed with an FFT for bass, mids, highs and overall energy. Brightness is scaled to the loudest part of the song being played.
- Four lighting modes, switching every 12 seconds (see Lighting modes below).
- A configurable delay keeps the lights in time with a Bluetooth speaker.
- Motorized sliding walls driven by an Arduino Nano and three stepper motors (documentation in progress).

## Hardware

- Raspberry Pi 5 and a microSD card (16 GB or more)
- 3x ILI9341 240x320 SPI displays
- 3.3 V RGB LEDs around the stage and in the bars, switched by 3x BC337 transistors from the Pi
- 12 V LED strip with its own remote controller (stand-alone, not controlled by the Pi)
- Arduino Nano, 3x 28BYJ-48 stepper motors with ULN2003 drivers, buttons and limit switches
- Bluetooth speaker
- Power:
  - Official Raspberry Pi 27 W USB-C power supply (Pi only)
  - Repurposed PC ATX power supply (3.3 V, 5 V and 12 V rails for everything else)

Wiring, pinouts and power distribution are in [docs/hardware_setup.md](docs/hardware_setup.md). Build order and testing are in [docs/assembly-guide.md](docs/assembly-guide.md).

## Setup

### 1. Raspberry Pi OS

Flash Raspberry Pi OS (64-bit) with [Raspberry Pi Imager](https://www.raspberrypi.com/software/), then enable SPI:

```bash
sudo raspi-config
# Interface Options → SPI → Enable, then reboot
```

Add the extra SPI buses to `/boot/firmware/config.txt` (`/boot/config.txt` on older releases):

```
dtparam=spi=on
dtoverlay=spi1-3cs
dtoverlay=spi5-1cs
```

Reboot and check that all three SPI devices exist:

```bash
ls /dev/spi*
# Should show: /dev/spidev0.0 /dev/spidev1.0 /dev/spidev5.0
```

### 2. System packages

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv python3-pil python3-numpy \
    libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev \
    libopenjp2-7 libtiff6 ffmpeg git
```

### 3. Clone and install

```bash
git clone https://github.com/KitioAdfafas/Massum-2026.git
cd Massum-2026

python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`--system-site-packages` lets the virtual environment use the GPIO libraries that come preinstalled with Raspberry Pi OS.

## Usage

### 1. Prepare the media

The script expects two files next to `dj_show.py`:

| File | What it is |
|------|------------|
| `music.mp3` | The song to play and analyse |
| `video_optimized.mp4` | The video for the three displays (240x320) |

Convert any video to fit the displays:

```bash
ffmpeg -i input.mp4 \
  -vf "scale=240:320:force_original_aspect_ratio=decrease,pad=240:320:(ow-iw)/2:(oh-ih)/2" \
  -r 25 -c:v libx264 -preset slow -crf 18 -an \
  video_optimized.mp4
```

Extract the audio from a video if needed:

```bash
ffmpeg -i input.mp4 -q:a 0 -map a music.mp3
```

This repository does not include any music or video. Use your own files or royalty-free ones, for example from [Pixabay Music](https://pixabay.com/music/), [Free Music Archive](https://freemusicarchive.org/) or [Pexels Videos](https://www.pexels.com/videos/).

### 2. Run the show

```bash
source .venv/bin/activate
python3 dj_show.py
```

The script first analyses the whole song, which takes a few seconds and prints a short summary. Then the music starts, the lights follow it and switch mode every 12 seconds, and the video loops on all three displays.

Press `Ctrl+C` to stop. The video keeps looping after the song ends.

## Configuration

All settings are variables in `dj_show.py`:

| Variable | Default | What it does |
|----------|---------|--------------|
| `mp3_file` | `"music.mp3"` | Song to play and analyse |
| `cv2.VideoCapture(...)` | `"video_optimized.mp4"` | Video for the displays |
| `BLUETOOTH_DELAY` | `0.22` | Seconds the lights run ahead to make up for Bluetooth lag |
| `mode_duration` | `12` | Seconds before switching to the next lighting mode |
| `chunk_size` | `2048` | Audio samples per analysis chunk |
| `baudrate` | `40000000` | SPI speed for each display |

To sync the lights with a Bluetooth speaker: if the lights are behind the beat, increase `BLUETOOTH_DELAY` (try 0.25 to 0.35). If they are ahead, decrease it (try 0.15 to 0.20). Change it in steps of 0.05.

The smoothing speed of each mode is the last argument of the `smooth_transition(...)` calls in the `SmartLEDEngine` class. Higher values make the colours change faster.

## Lighting modes

| Mode | Description | Characteristics | Best for |
|------|-------------|-----------------|----------|
| 0: Breathing Pulse | Colour palette cycling with bass intensity | Slow colour transitions, white flash on beats, palette chosen by song energy | Melodic sections, build-ups |
| 1: Rainbow Chase | Fast-moving rainbow wheel | Speed increases with energy, bass sets brightness | Drops, high-energy parts |
| 2: Spectrum Dance | Direct frequency-to-colour mapping | Red is bass, green is mids, blue is highs, white sparkles on loud highs | Tracks with lots of instruments |
| 3: Beat Color Snap | Solid colour that changes on every beat | Snaps to the next colour on each kick, pulses with the bass | Four-on-the-floor beats |

## Troubleshooting

### `No module named 'board'`

The virtual environment is not active, or the requirements are not installed. Run `source .venv/bin/activate` and `pip install -r requirements.txt`.

### Displays show garbage or static

- Check that SPI is enabled (`sudo raspi-config`, then Interface Options > SPI).
- Check the wiring against [hardware_setup.md](docs/hardware_setup.md).
- Lower `baudrate` from `40000000` to `20000000` in the three `ili9341.ILI9341(...)` calls.

### One display stays blank

Run `ls /dev/spi*`. If `spidev1.0` or `spidev5.0` is missing, check the `dtoverlay` lines in `config.txt` and reboot.

### LEDs don't respond

Test one channel directly (red is GPIO 13, green GPIO 19, blue GPIO 5):

```python
from gpiozero import PWMLED
led = PWMLED(13)
led.on()  # the red LEDs should light up
```

If nothing happens, check the transistor orientation (C-B-E), the 3.3 V supply and the common ground between the Pi and the ATX PSU.

### Lights out of sync with the music

Adjust `BLUETOOTH_DELAY` (see Configuration above).

### Choppy video

Check the Pi's temperature with `vcgencmd measure_temp`; it should stay below 80 °C. Make sure the video was converted with the command above, and close other programs.

## Project status

The Raspberry Pi light and video show is finished. Still to be added:

- Arduino code and wiring for the motorized sliding walls
- 3D models (STL/STEP) for the DJ booth, bar, tables and sliding walls (see [3d-models/](3d-models/))
- Photos of the finished club

## License

The code and documentation are under the MIT License (see [LICENSE](LICENSE)). The 3D models are under Creative Commons BY-SA 4.0 (see [3d-models/LICENSE](3d-models/LICENSE)).

## Credits

Built by the MASSUM 2026 team at DSU RCSOO Nikola Karev, Strumica. The school's construction team made the original club design and the physical model. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for details.

Thanks to Adafruit for the CircuitPython display libraries and to the FFmpeg project.

## Contact

kafklabs@gmail.com
