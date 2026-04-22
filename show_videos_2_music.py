import board
import digitalio
import busio
import cv2
from PIL import Image
import adafruit_rgb_display.ili9341 as ili9341

import pygame
import threading
import numpy as np
from gpiozero import PWMLED
from pydub import AudioSegment
import time
from scipy.fft import rfft, rfftfreq
import random

# ================= DISPLAY SETUP =================

spi0 = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs1 = digitalio.DigitalInOut(board.D23)
dc1 = digitalio.DigitalInOut(board.D24)
rst1 = digitalio.DigitalInOut(board.D25)
display1 = ili9341.ILI9341(spi0, cs=cs1, dc=dc1, rst=rst1, baudrate=40000000)

spi1 = busio.SPI(clock=board.D21, MOSI=board.D20)
dc2 = digitalio.DigitalInOut(board.D17)
rst2 = digitalio.DigitalInOut(board.D18)
display2 = ili9341.ILI9341(spi1, cs=None, dc=dc2, rst=rst2, baudrate=40000000)

spi3 = busio.SPI(clock=board.D15, MOSI=board.D14)
dc3 = digitalio.DigitalInOut(board.D6)
rst3 = digitalio.DigitalInOut(board.D26)
display3 = ili9341.ILI9341(spi3, cs=None, dc=dc3, rst=rst3, baudrate=40000000)

# ================= LED SETUP =================

red_led = PWMLED(13)
green_led = PWMLED(19)
blue_led = PWMLED(5)

# ================= AUDIO LOAD =================

mp3_file = "music.mp3"

pygame.mixer.init()
pygame.mixer.music.load(mp3_file)

audio = AudioSegment.from_mp3(mp3_file)
samples = np.array(audio.get_array_of_samples())

if audio.channels == 2:
    samples = samples.reshape((-1, 2)).mean(axis=1)

sample_rate = audio.frame_rate
chunk_size = 2048

# ================= FULL SONG ANALYSIS =================

print("🎵 Analyzing entire song for optimal lighting...")

def analyze_full_song():
    """Pre-analyze the entire song to find bass peaks and energy levels"""
    total_samples = len(samples)
    step = chunk_size
    
    bass_data = []
    mid_data = []
    high_data = []
    energy_data = []
    timestamps = []
    
    for i in range(0, total_samples - chunk_size, step):
        chunk = samples[i:i + chunk_size]
        
        # FFT analysis
        fft = np.fft.rfft(chunk)
        fft_data = np.abs(fft)
        
        # Extract frequency bands
        bass = np.mean(fft_data[0:25])
        mid = np.mean(fft_data[25:120])
        high = np.mean(fft_data[120:300])
        energy = np.sum(fft_data)
        
        bass_data.append(bass)
        mid_data.append(mid)
        high_data.append(high)
        energy_data.append(energy)
        timestamps.append(i / sample_rate)
    
    # Find peaks and ranges
    bass_max = np.max(bass_data)
    bass_min = np.min(bass_data)
    bass_avg = np.mean(bass_data)
    bass_std = np.std(bass_data)
    
    mid_max = np.max(mid_data)
    high_max = np.max(high_data)
    energy_max = np.max(energy_data)
    
    # Detect beats (bass peaks above threshold)
    beat_threshold = bass_avg + bass_std * 1.2
    beat_times = [timestamps[i] for i, b in enumerate(bass_data) if b > beat_threshold]
    
    print(f"✅ Analysis complete!")
    print(f"   Bass range: {bass_min:.0f} - {bass_max:.0f} (avg: {bass_avg:.0f})")
    print(f"   Detected {len(beat_times)} beats")
    print(f"   Song duration: {timestamps[-1]:.1f}s")
    
    return {
        'bass_data': np.array(bass_data),
        'mid_data': np.array(mid_data),
        'high_data': np.array(high_data),
        'energy_data': np.array(energy_data),
        'timestamps': np.array(timestamps),
        'bass_max': bass_max,
        'mid_max': mid_max,
        'high_max': high_max,
        'energy_max': energy_max,
        'bass_avg': bass_avg,
        'bass_std': bass_std,
        'beat_times': beat_times,
        'beat_threshold': beat_threshold
    }

song_analysis = analyze_full_song()

# ================= SMART LED ENGINE =================

BLUETOOTH_DELAY = 0.22

def clamp(value, min_val=0.0, max_val=1.0):
    """Ensure value is between 0 and 1"""
    return max(min_val, min(max_val, value))

def smooth_transition(current, target, speed=0.15):
    """Smooth LED transitions instead of hard cuts"""
    return current + (target - current) * speed

class SmartLEDEngine:
    def __init__(self, analysis):
        self.analysis = analysis
        self.current_r = 0.0
        self.current_g = 0.0
        self.current_b = 0.0
        self.last_beat_time = 0
        self.beat_index = 0
        self.strobe_active = False
        
        # Color palettes for different energy levels
        self.low_energy_colors = [
            (0.2, 0.0, 0.5),   # Deep purple
            (0.0, 0.2, 0.5),   # Deep blue
            (0.5, 0.0, 0.2),   # Deep red
        ]
        
        self.mid_energy_colors = [
            (0.0, 1.0, 1.0),   # Cyan
            (1.0, 0.0, 1.0),   # Magenta
            (1.0, 0.5, 0.0),   # Orange
        ]
        
        self.high_energy_colors = [
            (1.0, 1.0, 0.0),   # Yellow
            (0.0, 1.0, 0.0),   # Green
            (1.0, 0.0, 0.0),   # Red
            (1.0, 1.0, 1.0),   # White
        ]
    
    def get_current_data(self, current_time):
        """Get normalized frequency data for current time"""
        # Find closest timestamp in analysis
        idx = np.searchsorted(self.analysis['timestamps'], current_time)
        idx = min(idx, len(self.analysis['bass_data']) - 1)
        
        # Normalize using max values from analysis
        bass = self.analysis['bass_data'][idx] / self.analysis['bass_max']
        mid = self.analysis['mid_data'][idx] / self.analysis['mid_max']
        high = self.analysis['high_data'][idx] / self.analysis['high_max']
        energy = self.analysis['energy_data'][idx] / self.analysis['energy_max']
        
        return bass, mid, high, energy, idx
    
    def is_beat(self, current_time):
        """Check if current time is near a detected beat"""
        for beat_time in self.analysis['beat_times']:
            if abs(current_time - beat_time) < 0.05:  # 50ms window
                if current_time - self.last_beat_time > 0.15:  # Prevent double-triggers
                    self.last_beat_time = current_time
                    self.beat_index += 1
                    return True
        return False
    
    def bass_strobe_flash(self):
        """Quick white flash on bass hits"""
        red_led.value = 1.0
        green_led.value = 1.0
        blue_led.value = 1.0
        time.sleep(0.02)
    
    def breathing_pulse(self, bass, mid, high, energy):
        """Smooth breathing effect based on energy"""
        # Choose color palette based on energy
        if energy > 0.7:
            palette = self.high_energy_colors
        elif energy > 0.4:
            palette = self.mid_energy_colors
        else:
            palette = self.low_energy_colors
        
        # Cycle through palette based on time
        color_idx = int((time.time() * 0.5) % len(palette))
        base_color = palette[color_idx]
        
        # Pulse intensity with bass
        intensity = 0.3 + bass * 0.7
        
        target_r = base_color[0] * intensity
        target_g = base_color[1] * intensity
        target_b = base_color[2] * intensity
        
        # Smooth transition
        self.current_r = smooth_transition(self.current_r, target_r, 0.2)
        self.current_g = smooth_transition(self.current_g, target_g, 0.2)
        self.current_b = smooth_transition(self.current_b, target_b, 0.2)
        
        red_led.value = clamp(self.current_r)
        green_led.value = clamp(self.current_g)
        blue_led.value = clamp(self.current_b)
    
    def rainbow_chase(self, bass, mid, high, energy):
        """Fast rainbow color wheel, speed increases with energy"""
        # Speed based on energy (0.5x to 4x speed)
        speed = 1.5 + energy * 4.0
        
        # HSV to RGB rainbow effect
        hue = (time.time() * speed) % 1.0
        
        # Simple HSV to RGB conversion
        h = hue * 6
        x = 1 - abs((h % 2) - 1)
        
        if h < 1:
            r, g, b = 1, x, 0
        elif h < 2:
            r, g, b = x, 1, 0
        elif h < 3:
            r, g, b = 0, 1, x
        elif h < 4:
            r, g, b = 0, x, 1
        elif h < 5:
            r, g, b = x, 0, 1
        else:
            r, g, b = 1, 0, x
        
        # Modulate brightness with bass
        brightness = 0.4 + bass * 0.6
        
        target_r = r * brightness
        target_g = g * brightness
        target_b = b * brightness
        
        # Smooth but fast transitions
        self.current_r = smooth_transition(self.current_r, target_r, 0.4)
        self.current_g = smooth_transition(self.current_g, target_g, 0.4)
        self.current_b = smooth_transition(self.current_b, target_b, 0.4)
        
        red_led.value = clamp(self.current_r)
        green_led.value = clamp(self.current_g)
        blue_led.value = clamp(self.current_b)
    
    def spectrum_dance(self, bass, mid, high, energy):
        """Each frequency controls a color with smooth blending"""
        # Boost mid and high for visibility
        target_r = clamp(bass * 1.2)
        target_g = clamp(mid * 1.5)
        target_b = clamp(high * 1.8)
        
        # Faster transitions for more reactive feel
        self.current_r = smooth_transition(self.current_r, target_r, 0.35)
        self.current_g = smooth_transition(self.current_g, target_g, 0.35)
        self.current_b = smooth_transition(self.current_b, target_b, 0.35)
        
        red_led.value = clamp(self.current_r)
        green_led.value = clamp(self.current_g)
        blue_led.value = clamp(self.current_b)
    
    def beat_color_snap(self, bass, mid, high):
        """Snap to new vibrant color on each beat, hold and pulse"""
        colors = [
            (1.0, 0.0, 0.0),   # Red
            (0.0, 1.0, 0.0),   # Green
            (0.0, 0.0, 1.0),   # Blue
            (1.0, 1.0, 0.0),   # Yellow
            (1.0, 0.0, 1.0),   # Magenta
            (0.0, 1.0, 1.0),   # Cyan
        ]
        
        color = colors[self.beat_index % len(colors)]
        
        # Pulse the color with current bass level
        intensity = 0.6 + bass * 0.4
        
        target_r = color[0] * intensity
        target_g = color[1] * intensity
        target_b = color[2] * intensity
        
        # Hold color but let it pulse
        self.current_r = smooth_transition(self.current_r, target_r, 0.3)
        self.current_g = smooth_transition(self.current_g, target_g, 0.3)
        self.current_b = smooth_transition(self.current_b, target_b, 0.3)
        
        red_led.value = clamp(self.current_r)
        green_led.value = clamp(self.current_g)
        blue_led.value = clamp(self.current_b)
    
    def sparkle_burst(self, high):
        """Random sparkles on high frequencies"""
        if random.random() < high * 0.3:
            # Quick white flash
            red_led.value = 1.0
            green_led.value = 1.0
            blue_led.value = 1.0
            time.sleep(0.008)

# ================= MAIN LED SYNC THREAD =================

engine = SmartLEDEngine(song_analysis)

def led_music_sync():
    pygame.mixer.music.play()
    
    mode = 0  # Visual mode
    mode_timer = time.time()
    mode_duration = 12  # Change effect every 12 seconds
    
    print("🎆 Starting light show...")
    
    while pygame.mixer.music.get_busy():
        # Get current playback time
        current_time = pygame.mixer.music.get_pos() / 1000.0
        analysis_time = current_time + BLUETOOTH_DELAY
        
        # Get analyzed data for this moment
        bass, mid, high, energy, idx = engine.get_current_data(analysis_time)
        
        # Check for beat
        is_beat = engine.is_beat(analysis_time)
        
        # Auto-switch modes based on time
        if time.time() - mode_timer > mode_duration:
            mode = (mode + 1) % 4
            mode_timer = time.time()
            print(f"🎨 Switching to mode {mode}")
        
        # ===== VISUAL MODES =====
        
        if mode == 0:  # BREATHING PULSE (your favorite!)
            if is_beat:
                engine.bass_strobe_flash()
            engine.breathing_pulse(bass, mid, high, energy)
        
        elif mode == 1:  # RAINBOW CHASE (fixed - was energy wave)
            if is_beat:
                engine.bass_strobe_flash()
            engine.rainbow_chase(bass, mid, high, energy)
        
        elif mode == 2:  # SPECTRUM DANCE
            engine.spectrum_dance(bass, mid, high, energy)
            if high > 0.7:
                engine.sparkle_burst(high)
        
        elif mode == 3:  # BEAT COLOR SNAP (fixed - was going black)
            if is_beat:
                engine.bass_strobe_flash()
            engine.beat_color_snap(bass, mid, high)
        
        time.sleep(0.01)  # 100Hz update rate

# Start LED/music thread
threading.Thread(target=led_music_sync, daemon=True).start()

# ================= VIDEO LOOP =================

cap = cv2.VideoCapture("video_optimized.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)

    display1.image(image)
    display2.image(image)
    display3.image(image)