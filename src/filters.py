from scipy.signal import butter, sosfiltfilt

def apply_filter(x, fs, filter_type, cutoff, order=4):
    nyquist = fs / 2
    if filter_type == "Band-pass":
        low, high = cutoff
        low = max(0.001, low / nyquist)
        high = min(0.999, high / nyquist)
        sos = butter(order, [low, high], btype="bandpass", output="sos")
    else:
        wn = max(0.001, min(0.999, cutoff / nyquist))
        btype = "lowpass" if filter_type == "Low-pass" else "highpass"
        sos = butter(order, wn, btype=btype, output="sos")
    return sosfiltfilt(sos, x)
