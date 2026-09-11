import numpy as np

def analyze_signal(x, fs):
    x = np.asarray(x, dtype=float)
    peak = float(np.max(np.abs(x)))
    rms = float(np.sqrt(np.mean(x**2)))
    freqs, mag = fft_analysis(x, fs)
    dominant = float(freqs[np.argmax(mag[1:]) + 1]) if len(mag) > 1 else 0.0
    return {
        "mean": float(np.mean(x)),
        "rms": rms,
        "peak": peak,
        "peak_to_peak": float(np.ptp(x)),
        "std": float(np.std(x)),
        "dominant_frequency": dominant,
        "crest_factor": float(peak / rms) if rms else 0.0,
    }

def fft_analysis(x, fs):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return np.array([0.0]), np.array([0.0])
    window = np.hanning(n)
    spectrum = np.fft.rfft((x - np.mean(x)) * window)
    freqs = np.fft.rfftfreq(n, d=1/fs)
    magnitude = (2.0 / np.sum(window)) * np.abs(spectrum)
    return freqs, magnitude
