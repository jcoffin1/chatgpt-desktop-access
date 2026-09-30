"""Serialized, failure-safe sound output for ChatGPT Desktop Access."""

import os
import wave
from collections import deque

import nvwave
import tones
import wx
from logHandler import log

from .core import soundKey, tonePattern


_SOUND_GAP_MILLISECONDS = 35
_MAX_PENDING_SOUNDS = 6
_TASK_ACTIVITY_SOUNDS = frozenset((
	"thinking", "working", "command", "search", "file", "build", "tool",
	"commentary", "other", "backgroundPulse1", "backgroundPulse2",
	# Intermediate operation completions share this key with task completion.
	# Discard old ones before queuing the final completion cue.
	"completion",
))
_EVICTABLE_SOUNDS = _TASK_ACTIVITY_SOUNDS - {"completion"}
_pendingProgressSounds = deque()
_activeProgressSound = None
_progressSoundTimer = None
_waveDurationCache = {}


def safeBeep(frequency, duration):
	try:
		tones.beep(frequency, duration)
	except Exception:
		log.debugWarning("ChatGPT Desktop Access tone output failed", exc_info=True)


def _playProgressTone(category, message=""):
	delay = 0
	for index, (frequency, duration) in enumerate(tonePattern(category, message)):
		if index == 0:
			safeBeep(frequency, duration)
		else:
			wx.CallLater(delay, safeBeep, frequency, duration)
		delay += duration + 25
	return max(0, delay - 25)


def _waveDurationMilliseconds(path):
	duration = _waveDurationCache.get(path)
	if duration is not None:
		return duration
	with wave.open(path, "rb") as source:
		frameRate = source.getframerate()
		duration = round(source.getnframes() * 1000.0 / frameRate) if frameRate else 0
	duration = max(1, duration)
	_waveDurationCache[path] = duration
	return duration


def _finishProgressSound():
	global _activeProgressSound, _progressSoundTimer
	_activeProgressSound = None
	_progressSoundTimer = None
	if _pendingProgressSounds:
		_startProgressSound(_pendingProgressSounds.popleft())


def _startProgressSound(item):
	global _activeProgressSound, _progressSoundTimer
	category, message, style, volume = item
	_activeProgressSound = item
	log.debug("ChatGPT Desktop Access sound started: %s (%s)", category, style)
	if style == "tones":
		duration = _playProgressTone(category, message)
	else:
		path = os.path.join(
			os.path.dirname(__file__), "sounds", volume, f"{soundKey(category, message)}.wav",
		)
		try:
			duration = _waveDurationMilliseconds(path)
			nvwave.playWaveFile(path)
		except Exception:
			log.debugWarning("ChatGPT Desktop Access could not play click earcon; using tones", exc_info=True)
			duration = _playProgressTone(category, message)
	_progressSoundTimer = wx.CallLater(
		max(1, duration + _SOUND_GAP_MILLISECONDS), _finishProgressSound,
	)


def playProgressSound(category, message="", style="clicks", volume="normal"):
	"""Play meaningful cues in order, dropping Working ticks during another cue."""
	item = (category, message, style, volume)
	if _progressSoundTimer is None:
		_startProgressSound(item)
		return True
	if category == "working":
		log.debug("ChatGPT Desktop Access skipped Working tick during another sound")
		return False
	while len(_pendingProgressSounds) >= _MAX_PENDING_SOUNDS:
		oldestActivity = next((
			index for index, pending in enumerate(_pendingProgressSounds)
			if pending[0] in _EVICTABLE_SOUNDS
		), None)
		if oldestActivity is None:
			if category in _EVICTABLE_SOUNDS:
				log.debug("ChatGPT Desktop Access sound queue full; skipped %s", category)
				return False
			removed = _pendingProgressSounds.popleft()
		else:
			removed = _pendingProgressSounds[oldestActivity]
			del _pendingProgressSounds[oldestActivity]
		log.debug("ChatGPT Desktop Access sound queue full; replaced %s with %s", removed[0], category)
	_pendingProgressSounds.append(item)
	log.debug("ChatGPT Desktop Access sound queued: %s (depth %d)", category, len(_pendingProgressSounds))
	return True


def discardPendingActivitySounds():
	"""Discard old task cues before a terminal or focus cue is queued."""
	if not _pendingProgressSounds:
		return
	retained = [item for item in _pendingProgressSounds if item[0] not in _TASK_ACTIVITY_SOUNDS]
	discarded = len(_pendingProgressSounds) - len(retained)
	_pendingProgressSounds.clear()
	_pendingProgressSounds.extend(retained)
	if discarded:
		log.debug("ChatGPT Desktop Access discarded %d pending activity sounds at task end", discarded)


def stopProgressSounds():
	"""Stop queued sounds when the add-on unloads."""
	global _activeProgressSound, _progressSoundTimer
	_pendingProgressSounds.clear()
	if _progressSoundTimer is not None:
		try:
			_progressSoundTimer.Stop()
		except Exception:
			pass
	_progressSoundTimer = None
	_activeProgressSound = None
