# 🎧 Raspberry Pi 5 DJ Display System

A multi-display DJ setup for Raspberry Pi 5 with synchronized video playback, audio-reactive LED lighting, intelligent beat detection, and motorized sliding walls.

![Demo](docs/images/finished-setup-front.jpg)

## ✨ Features

### Visual System
- **Triple ILI9341 Display Support** - Synchronized video on 3x 240x320 SPI displays
- **Smart Audio Analysis** - Pre-analyzes entire song for optimal lighting
- **4 Intelligent Visual Modes**:
  - 🌊 **Breathing Pulse** - Energy-based color breathing with beat strobes
  - 🌈 **Rainbow Chase** - Dynamic rainbow wheel synced to song energy
  - 🎨 **Spectrum Dance** - Frequency-reactive RGB with sparkles
  - 💥 **Beat Color Snap** - Color snapping on detected beats
- **Adaptive Normalization** - Lights automatically adjust to your song's frequency range
- **Bluetooth Speaker Support** - Configurable audio delay compensation

### Physical Stage
- **3D Printed Club Environment** - DJ booth, bar, and tables
- **Motorized Sliding Walls** - Arduino-controlled stage dynamics
- **Professional LED Lighting** - Audio-reactive RGB stage lights

## 🎬 Demo

![Lights Demo](docs/images/lights-demo.jpg)

*Audio-reactive LED lighting in action*

![Displays](docs/images/displays-closeup.jpg)

*Triple synchronized display setup*

## 🛠️ Hardware Requirements

### Electronics
- **Raspberry Pi 5** (4GB+ recommended)
- **3x ILI9341 240x320 SPI displays**
- **RGB LED stage lights** (individual RGB LEDs)
- **Arduino Nano** (for sliding walls)
- **3x 28BYJ-48 Stepper Motors** with ULN2003 drivers
- **Bluetooth speaker**
- **MicroSD card** (16GB+)
- **Power supplies:**
  - Official Raspberry Pi 5V 5A power supply (for Pi only)
  - 12V ATX PSU (repurposed from old PC) for servos, lights, and screens

### 3D Printed Components
- DJ booth with display mounts
- Bar counter
- Audience tables
- Sliding wall tracks and panels

See [Hardware Setup Guide](docs/hardware_setup.md) for complete wiring diagrams.

## 📦 Installation

### 1. Raspberry Pi OS Setup

```bash
# Flash Raspberry Pi OS (64-bit recommended)
# Download from: https://www.raspberrypi.com/software/

# Enable SPI interfaces
sudo raspi-config
# Navigate to: Interface Options → SPI → Enable
# Reboot when prompted
```

### 2. Install System Dependencies

```bash
sudo apt update
sudo apt install -y python3-pip python3-pil python3-numpy \
    libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev \
    libopenjp2-7 libtiff5 ffmpeg git
```

### 3. Clone Repository

```bash
git clone https://github.com/yourusername/rpi5-dj-display.git
cd rpi5-dj-display
```

### 4. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### 5. Verify SPI Devices

```bash
ls /dev/spi*
# Should show: /dev/spidev0.0 /dev/spidev1.0 /dev/spidev5.0
```

## 🎵 Usage

### 1. Prepare Your Media

**Optimize video for 240x320 displays:**

```bash
ffmpeg -i input.mp4 \
  -vf "scale=240:320:force_original_aspect_ratio=decrease,pad=240:320:(ow-iw)/2:(oh-ih)/2" \
  -r 25 -c:v libx264 -preset slow -crf 18 -an \
  video_optimized.mp4
```

**Extract audio:**

```bash
ffmpeg -i input.mp4 -q:a 0 -map a music_techno.mp3
```

### 2. Configure File Paths

Edit `show_videos_2_music.py`:

```python
# Line 67
mp3_file = "music_techno.mp3"

# Line 288
cap = cv2.VideoCapture("video_optimized.mp4")
```

### 3. Run the Show

```bash
python3 show_videos_2_music.py
```

**Expected Output:**

```
🎵 Analyzing entire song for optimal lighting...
✅ Analysis complete!
   Bass range: 45230 - 892340 (avg: 234567)
   Detected 342 beats
   Song duration: 183.4s
🎆 Starting light show...
🎨 Switching to mode 0
🎨 Switching to mode 1
...
```

**What happens:**

1. Analyzes the entire song (~10-30 seconds depending on length)
2. Detects beats and calculates frequency ranges
3. Starts synchronized video + audio playback
4. Auto-rotates lighting modes every 12 seconds

### 4. Stop Playback

Press `Ctrl+C` to stop.

## ⚙️ Configuration

### Audio Sync Adjustment

Edit these variables in `show_videos_2_music.py`:

```python
# Line 73 - Bluetooth audio delay compensation
BLUETOOTH_DELAY = 0.22  # Seconds

# If lights are BEHIND the beat: increase (try 0.25-0.35)
# If lights are AHEAD of the beat: decrease (try 0.15-0.20)
```

### Visual Settings

```python
# Line 220 - Mode rotation speed
mode_duration = 12  # Seconds per lighting mode

# Line 75 - LED intensity
BOOST = 8.0  # Higher = brighter (range: 5-15)
```

### Individual Mode Adjustments

Fine-tune transition speeds in the `SmartLEDEngine` class:

```python
# Breathing Pulse - smoother transitions
self.current_r = smooth_transition(self.current_r, target_r, 0.2)

# Rainbow Chase - faster color changes
self.current_r = smooth_transition(self.current_r, target_r, 0.4)

# Spectrum Dance - more reactive
self.current_r = smooth_transition(self.current_r, target_r, 0.35)

# Beat Color Snap - quicker snaps
self.current_r = smooth_transition(self.current_r, target_r, 0.3)
```

## 🎨 Lighting Modes Explained

| Mode | Description | Characteristics | Best For |
|------|-------------|-----------------|----------|
| **0: Breathing Pulse** | Smooth color palette cycling with bass intensity | Slow color transitions, white flash on beats, energy-based palette selection | Melodic sections, buildups, ambient parts |
| **1: Rainbow Chase** | Fast-moving rainbow wheel | Speed increases with song energy, bass modulates brightness | High energy drops, climactic sections |
| **2: Spectrum Dance** | Direct frequency-to-color mapping | Red=bass, Green=mid, Blue=high, random sparkles on treble | Complex tracks with varied instrumentation |
| **3: Beat Color Snap** | Vibrant solid colors change on beats | Snaps to new color each kick, pulses with bass | Percussive sections, four-on-the-floor beats |

**Mode Rotation:**

Modes automatically cycle every 12 seconds. To change rotation speed, edit `mode_duration` variable.

## 🤖 Arduino Motorized Walls



## 📐 3D Printed Stage Components

The project includes complete 3D printable models for a miniature DJ club environment.

### What's Included

- **DJ Booth** - Main structure with cutouts for 3 displays
- **Bar Counter** - Club bar with LED backlighting mounts
- **Tables** - Modular audience seating (multiple sizes)
- **Sliding Walls** - Motorized wall panels with motor mounts

![Stage Setup](docs/images/finished-setup-top.jpg)

### Printing

All STL files are in the [`3d-models/`](3d-models/) directory with assembly instructions.

**Quick Stats:**

- Material: PLA recommended
- Total print time: ~40-60 hours
- Filament needed: ~800g-1200g
- Estimated cost: $15-25 in materials

See [`3d-models/README.md`](3d-models/README.md) for detailed printing guidelines.

## 🐛 Troubleshooting

### Display Issues

**"No module named 'board'"**

```bash
pip3 install adafruit-blinka adafruit-circuitpython-rgb-display
```

**Displays showing garbage/static:**

- Verify SPI is enabled: `sudo raspi-config` → Interface Options → SPI
- Check connections match [wiring diagram](docs/hardware_setup.md)
- Try lowering baudrate to `20000000` in script (lines 14, 20, 26)

**One or more displays not working:**

```bash
# Test SPI devices
ls /dev/spi*

# Should show all three: spidev0.0, spidev1.0, spidev5.0
# If missing, check /boot/config.txt for:
# dtparam=spi=on
# dtoverlay=spi1-3cs
# dtoverlay=spi5-1cs
```

### LED Issues

**LEDs not responding:**

Verify GPIO pins: Red=13, Green=19, Blue=5

Test individual LED:

```python
from gpiozero import PWMLED
led = PWMLED(13)
led.on()  # Should turn on red LED
```

**LEDs too dim:**

- Increase `BOOST` variable (default 8.0, try 10-15)
- Check resistor values (220Ω standard)
- For LED strips, use MOSFET driver circuit

**LEDs too bright/flickering:**

- Decrease `BOOST` variable (try 5-6)
- Check power supply stability
- Add capacitor (100µF) across LED power

**Wrong colors displaying:**

- Verify common anode vs cathode configuration
- Swap GPIO assignments if colors are inverted

### Audio/Video Sync

**Lights lag behind music:**

```python
BLUETOOTH_DELAY = 0.30  # Increase by 0.05 increments
```

**Lights ahead of music:**

```python
BLUETOOTH_DELAY = 0.15  # Decrease by 0.05 increments
```

**Bluetooth audio crackling:**

```bash
# Increase Bluetooth audio buffer
echo "default-fragment-size-msec = 25" | sudo tee -a /etc/pulse/daemon.conf
pulseaudio -k  # Restart audio
```

**Video playback choppy:**

- Ensure Pi isn't throttling: `vcgencmd measure_temp` (should be <80°C)
- Use optimized video (see Usage section)
- Close other applications
- Consider overclocking in `raspi-config`

### Analysis/Performance

**"Analysis taking too long":**

- Normal for songs >5 minutes
- Progress isn't shown but it's working
- Expect 10-30 seconds analysis time

**High CPU usage:**

```bash
# Check temperature
vcgencmd measure_temp

# Monitor CPU
htop

# If overheating, improve cooling or reduce chunk_size:
# Edit line 72 in show_videos_2_music.py
# chunk_size = 4096  # Double the value
```

**Script crashes on startup:**

```bash
# Check Python version (need 3.9+)
python3 --version

# Verify all dependencies installed
pip3 list | grep -E 'pygame|numpy|opencv|pydub|scipy|gpiozero'
```

## 📊 System Performance

Tested on Raspberry Pi 5 (4GB):

| Component | CPU Usage | Notes |
|-----------|-----------|-------|
| Video Playback | ~15-20% | 3 displays @ 25fps |
| Audio Analysis | ~10-15% | Real-time FFT |
| LED Control | ~5% | 100Hz update rate |
| **Total** | **~30-40%** | Leaves headroom for Arduino serial |

**RAM Usage:** ~400-600MB

## 🎤 Sample Media Sources

**Royalty-Free Music:**

- [Pixabay Music](https://pixabay.com/music/) - Free electronic/techno tracks
- [Free Music Archive](https://freemusicarchive.org/) - Creative Commons licensed
- [YouTube Audio Library](https://www.youtube.com/audiolibrary) - Free download

**Video Clips:**

- [Pexels Videos](https://www.pexels.com/videos/) - Free stock footage
- [Pixabay Videos](https://pixabay.com/videos/) - No attribution required
- Use your own DJ visuals or VJ loops

> ⚠️ **Copyright:** This repository does not include copyrighted music or video. Users must provide their own media files.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

**Software:**

- [ ] Web interface for remote control
- [ ] MIDI controller support for manual mode switching
- [ ] Additional visual modes (fire, water, geometric patterns)
- [ ] WS2812B/NeoPixel LED strip support
- [ ] Save/load lighting presets
- [ ] Real-time BPM detection

**Hardware:**

- [ ] DMX512 output for professional lighting
- [ ] Wireless display sync
- [ ] Fog machine integration
- [ ] Additional motor control (rotating platforms)

**3D Models:**

- [ ] Alternative booth designs
- [ ] Scalable platform sizes
- [ ] Cable management solutions

### How to Contribute

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**3D Models:** Licensed under Creative Commons BY-SA 4.0

## 🙏 Acknowledgments

- **Adafruit** - CircuitPython display libraries and hardware support
- **FFmpeg Team** - Video/audio processing tools
- **Raspberry Pi Foundation** - Amazing hardware platform
- **Contributors** - Arduino wall control system

## 📧 Contact & Support

- **Email:**kafklabs@gmail.com

## 🌟 Show Your Support

If this project helped you create an awesome DJ setup:

- ⭐ Star this repository
- 📸 Share photos of your build
- 🐛 Report bugs or suggest features
- 🤝 Contribute code or 3D models

## 📸 Gallery

| | | |
|:--:|:--:|:--:|
| ![Setup 1](docs/images/finished-setup-front.jpg) | ![Setup 2](docs/images/finished-setup-side.jpg) | ![Setup 3](docs/images/lights-demo.jpg) |
| *Front view* | *Side angle* | *Reactive lighting* |

---

**Built with ❤️ for makers, DJs, and miniature club enthusiasts**

*Project Status: Active Development | Last Updated: 2025*
