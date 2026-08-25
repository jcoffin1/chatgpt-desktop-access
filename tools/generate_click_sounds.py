"""Generate original, license-free click earcons for Codex Status Announcer."""

from pathlib import Path
import math
import random
import struct
import wave


SAMPLE_RATE = 44100
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "globalPlugins" / "codexStatusAnnouncer" / "sounds"
PATTERNS = {
	"thinking": ((0, 0.55), (105, 0.68)),
	"working": ((0, 0.62),),
	"command": ((0, 0.62), (125, 0.88)),
	"search": ((0, 0.74), (78, 0.88), (156, 1.02)),
	"file": ((0, 0.58), (155, 0.72)),
	"build": ((0, 0.60), (92, 0.74), (184, 0.90)),
	"tool": ((0, 0.84), (48, 0.84)),
	"completion": ((0, 0.62), (95, 0.82), (190, 1.05)),
	"failure": ((0, 0.78), (125, 0.58), (250, 0.42)),
	"other": ((0, 0.50),),
	"commentary": ((0, 0.66),),
	"attention": ((0, 0.90), (70, 1.10), (190, 0.90), (260, 1.10)),
	"backgroundPulse1": ((0, 0.48), (135, 0.70)),
	"backgroundPulse2": ((0, 0.54), (165, 0.78)),
	"monitoringActive": ((0, 0.55), (115, 0.95)),
	"monitoringInactive": ((0, 0.82), (145, 0.46)),
	"submission": ((0, 0.52), (80, 0.72), (170, 0.98)),
}
# Keep large perceptual gaps between these short sounds. Small amplitude
# differences are difficult to distinguish in NVDA's normal audio mix.
LEVELS = {"soft": 0.10, "normal": 0.30, "loud": 0.58}


def clickSample(relativeTime, brightness, amplitude, rng):
	if relativeTime < 0 or relativeTime >= 0.038:
		return 0.0
	envelope = math.exp(-relativeTime / 0.0065)
	resonance = math.sin(2 * math.pi * (1150 + brightness * 900) * relativeTime)
	noise = rng.uniform(-1.0, 1.0)
	return envelope * (0.62 * noise + 0.38 * resonance) * amplitude


def render(name, pattern, levelName, amplitude):
	rng = random.Random(f"codex-status-announcer-{name}")
	duration = pattern[-1][0] / 1000 + 0.055
	frames = []
	for sampleIndex in range(math.ceil(duration * SAMPLE_RATE)):
		time = sampleIndex / SAMPLE_RATE
		value = sum(clickSample(time - offset / 1000, brightness, amplitude, rng) for offset, brightness in pattern)
		value = max(-0.50, min(0.50, value))
		frames.append(struct.pack("<h", round(value * 32767)))
	levelDir = OUTPUT_DIR / levelName
	levelDir.mkdir(parents=True, exist_ok=True)
	path = levelDir / f"{name}.wav"
	with wave.open(str(path), "wb") as output:
		output.setnchannels(1)
		output.setsampwidth(2)
		output.setframerate(SAMPLE_RATE)
		output.writeframes(b"".join(frames))


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
for levelName, amplitude in LEVELS.items():
	for soundName, soundPattern in PATTERNS.items():
		render(soundName, soundPattern, levelName, amplitude)
print(f"Generated {len(PATTERNS) * len(LEVELS)} click earcons in {OUTPUT_DIR}")
