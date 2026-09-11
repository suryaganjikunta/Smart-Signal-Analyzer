import numpy as np
from scipy import signal


def generate_signal(
    signal_type,
    fs,
    duration,
    frequency,
    amplitude,
    noise_level
):
    # Create time array
    t = np.arange(0, duration, 1 / fs)

    # Generate the selected signal
    if signal_type == "Sine":
        x = amplitude * np.sin(2 * np.pi * frequency * t)

    elif signal_type == "Square":
        x = amplitude * signal.square(
            2 * np.pi * frequency * t
        )

    elif signal_type == "Triangle":
        x = amplitude * signal.sawtooth(
            2 * np.pi * frequency * t,
            width=0.5
        )

    elif signal_type == "Chirp":
        x = amplitude * signal.chirp(
            t,
            f0=max(1, frequency / 4),
            f1=frequency,
            t1=duration,
            method="linear"
        )

    elif signal_type == "Mixed + Noise":
        x = (
            amplitude * np.sin(2 * np.pi * frequency * t)
            + 0.45 * amplitude
            * np.sin(2 * np.pi * 3 * frequency * t)
        )

    else:
        x = np.zeros_like(t)

    # Add noise only when noise level is greater than zero
    if noise_level > 0:
        rng = np.random.default_rng(42)
        noise = noise_level * amplitude * rng.normal(
            0,
            1,
            len(t)
        )
        x = x + noise

    return t, x