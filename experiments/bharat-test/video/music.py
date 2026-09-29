"""Compose an original, royalty-free ambient bed (numpy only): soft pads, a gentle arpeggio and a bass line.

Nothing is sampled or downloaded, so there is no third-party copyright. Writes video/music.wav (44.1 kHz stereo).
Usage: python music.py [--seconds 70]
"""
import argparse
import wave
from pathlib import Path

import numpy as np

SR = 44100
HERE = Path(__file__).resolve().parent


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def tone(freq, dur, harmonics=(1.0, 0.25, 0.08), detune=0.0):
    t = np.arange(int(dur * SR)) / SR
    sig = sum(a * np.sin(2 * np.pi * freq * (k + 1) * t + k) for k, a in enumerate(harmonics))
    if detune:
        sig = 0.5 * sig + 0.5 * sum(a * np.sin(2 * np.pi * (freq + detune) * (k + 1) * t) for k, a in enumerate(harmonics))
    return sig


def envelope(n, attack, release):
    env = np.ones(n)
    a, r = int(attack * SR), int(release * SR)
    env[:a] = np.linspace(0, 1, a) ** 2
    env[-r:] *= np.linspace(1, 0, r) ** 2
    return env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=float, default=70.0)
    args = ap.parse_args()
    total = int(args.seconds * SR)
    left, right = np.zeros(total), np.zeros(total)

    bpm = 80
    beat = 60 / bpm
    bar = 4 * beat
    # D major: I - vi - IV - V (D, Bm, G, A), two bars each, as MIDI note sets.
    chords = [(62, 66, 69, 74), (59, 62, 66, 71), (55, 59, 62, 67), (57, 61, 64, 69)]
    roots = [38, 35, 43, 45]
    t0, ci = 0.0, 0
    while t0 < args.seconds:
        notes, root = chords[ci % 4], roots[ci % 4]
        dur = 2 * bar
        start = int(t0 * SR)
        # Pad: detuned, slow swell, overlapping into the next chord.
        for j, m in enumerate(notes):
            seg = tone(hz(m), dur + 1.2, detune=0.18) * envelope(int((dur + 1.2) * SR), 1.4, 1.6) * 0.05
            end = min(total, start + len(seg))
            pan = 0.35 + 0.1 * j
            left[start:end] += seg[:end - start] * (1 - pan)
            right[start:end] += seg[:end - start] * pan
        # Bass: root on beats 1 and 3.
        for b in range(0, 8, 2):
            s = int((t0 + b * beat) * SR)
            if s >= total:
                break
            n = int(1.6 * beat * SR)
            seg = tone(hz(root), n / SR, harmonics=(1.0, 0.15)) * np.exp(-np.arange(n) / SR * 2.2) * 0.09
            e = min(total, s + n)
            left[s:e] += seg[:e - s]
            right[s:e] += seg[:e - s]
        # Arpeggio: soft plucks on eighth notes, one octave up, starting after the first chord.
        if ci > 0:
            pattern = [notes[0], notes[1], notes[2], notes[3], notes[2], notes[1], notes[2], notes[3]]
            for k in range(16):
                s = int((t0 + k * beat / 2) * SR)
                if s >= total:
                    break
                n = int(0.9 * SR)
                m = pattern[k % 8] + 12
                seg = tone(hz(m), 0.9, harmonics=(1.0, 0.4, 0.15)) * np.exp(-np.arange(n) / SR * 5.5) * 0.028
                e = min(total, s + n)
                pan = 0.25 if k % 2 else 0.75
                left[s:e] += seg[:e - s] * (1 - pan)
                right[s:e] += seg[:e - s] * pan
        t0 += dur
        ci += 1

    # Gentle echo for space, master fades, then normalise peaks to -3 dBFS.
    for delay, gain in ((0.37, 0.25), (0.74, 0.12)):
        d = int(delay * SR)
        left[d:] += left[:-d] * gain
        right[d:] += right[:-d] * gain
    fade_in, fade_out = int(2.0 * SR), int(4.0 * SR)
    for ch in (left, right):
        ch[:fade_in] *= np.linspace(0, 1, fade_in)
        ch[-fade_out:] *= np.linspace(1, 0, fade_out)
    peak = max(np.abs(left).max(), np.abs(right).max())
    scale = 10 ** (-3 / 20) / peak
    stereo = (np.stack([left, right], axis=1) * scale * 32767).astype(np.int16)
    out = HERE / 'music.wav'
    with wave.open(str(out), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())
    rms = np.sqrt(np.mean((stereo.astype(np.float64) / 32767) ** 2))
    print(f'{out.name}: {args.seconds:.1f} s, peak -3.0 dBFS, RMS {20 * np.log10(rms):.1f} dBFS')


if __name__ == '__main__':
    main()
