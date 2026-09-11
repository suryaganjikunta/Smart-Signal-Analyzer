import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from src.signal_generator import generate_signal
from src.signal_analysis import analyze_signal, fft_analysis
from src.filters import apply_filter


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Smart Signal Analyzer",
    page_icon="📡",
    layout="wide"
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("📡 Smart Signal Analyzer")

st.caption(
    "A practical DSP dashboard for time-domain, FFT, "
    "filtering, and signal-quality analysis."
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("Signal Input")

    mode = st.radio(
        "Input mode",
        ["Generate Signal", "Upload CSV"]
    )

    # -----------------------------------------------------
    # GENERATE SIGNAL
    # -----------------------------------------------------

    if mode == "Generate Signal":

        signal_type = st.selectbox(
            "Signal type",
            [
                "Sine",
                "Square",
                "Triangle",
                "Chirp",
                "Mixed + Noise"
            ]
        )

        fs = st.number_input(
            "Sampling frequency (Hz)",
            min_value=100,
            max_value=100000,
            value=1000,
            step=100
        )

        duration = st.number_input(
            "Duration (seconds)",
            min_value=0.1,
            max_value=10.0,
            value=2.0,
            step=0.1
        )

        frequency = st.number_input(
            "Main frequency (Hz)",
            min_value=1.0,
            max_value=float(fs / 2),
            value=min(50.0, float(fs / 4)),
            step=1.0
        )

        amplitude = st.number_input(
            "Amplitude",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1
        )

        noise = st.slider(
            "Noise level",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.01
        )

        t, x = generate_signal(
            signal_type,
            fs,
            duration,
            frequency,
            amplitude,
            noise
        )

        input_name = f"Generated {signal_type}"

    # -----------------------------------------------------
    # UPLOAD CSV
    # -----------------------------------------------------

    else:

        uploaded = st.file_uploader(
            "Upload a CSV file",
            type=["csv"]
        )

        fs = st.number_input(
            "Sampling frequency (Hz)",
            min_value=100,
            max_value=100000,
            value=1000,
            step=100
        )

        if uploaded is not None:

            df = pd.read_csv(uploaded)

            numeric = df.select_dtypes(
                include=np.number
            )

            if numeric.empty:

                st.error(
                    "CSV must contain at least one numeric column."
                )

                st.stop()

            column = st.selectbox(
                "Signal column",
                list(numeric.columns)
            )

            x = (
                numeric[column]
                .dropna()
                .to_numpy(dtype=float)
            )

            t = np.arange(len(x)) / fs

            input_name = uploaded.name

        else:

            st.info(
                "Upload a CSV file to analyze it."
            )

            st.stop()

    # -----------------------------------------------------
    # FILTER SETTINGS
    # -----------------------------------------------------

    st.divider()

    st.header("Digital Filter")

    filter_type = st.selectbox(
        "Filter type",
        [
            "None",
            "Low-pass",
            "High-pass",
            "Band-pass"
        ]
    )

    cutoff1 = st.number_input(
        "Cutoff / Low cutoff (Hz)",
        min_value=1.0,
        max_value=float(fs / 2 - 1),
        value=min(100.0, float(fs / 4)),
        step=1.0
    )

    cutoff2 = st.number_input(
        "High cutoff (Hz)",
        min_value=2.0,
        max_value=float(fs / 2 - 0.5),
        value=min(250.0, float(fs / 2 - 1)),
        step=1.0
    )

    order = st.slider(
        "Filter order",
        min_value=1,
        max_value=8,
        value=4
    )


# ---------------------------------------------------------
# APPLY FILTER
# ---------------------------------------------------------

if filter_type == "None":

    y = x.copy()

elif filter_type == "Band-pass":

    if cutoff2 <= cutoff1:

        st.error(
            "High cutoff must be greater than low cutoff."
        )

        st.stop()

    y = apply_filter(
        x,
        fs,
        filter_type,
        (cutoff1, cutoff2),
        order
    )

else:

    y = apply_filter(
        x,
        fs,
        filter_type,
        cutoff1,
        order
    )


# ---------------------------------------------------------
# SIGNAL ANALYSIS
# ---------------------------------------------------------

metrics = analyze_signal(
    y,
    fs
)

freqs, magnitude = fft_analysis(
    y,
    fs
)


# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------

tabs = st.tabs(
    [
        "📈 Waveform",
        "🔊 FFT Spectrum",
        "🧮 Measurements",
        "🧠 Smart Analysis",
        "📥 Export"
    ]
)


# =========================================================
# WAVEFORM
# =========================================================

with tabs[0]:

    fig, ax = plt.subplots(
        figsize=(11, 4)
    )

    ax.plot(
        t,
        y,
        linewidth=1
    )

    ax.set_title(
        "Time-Domain Signal"
    )

    ax.set_xlabel(
        "Time (s)"
    )

    ax.set_ylabel(
        "Amplitude"
    )

    ax.grid(
        True,
        alpha=0.25
    )

    st.pyplot(
    fig,
    width="stretch"
    )

    plt.close(fig)


# =========================================================
# FFT SPECTRUM
# =========================================================

with tabs[1]:

    fig, ax = plt.subplots(
        figsize=(11, 4)
    )

    ax.plot(
        freqs,
        magnitude,
        linewidth=1
    )

    ax.set_title(
        "Single-Sided FFT Magnitude Spectrum"
    )

    ax.set_xlabel(
        "Frequency (Hz)"
    )

    ax.set_ylabel(
        "Magnitude"
    )

    ax.set_xlim(
        0,
        fs / 2
    )

    ax.grid(
        True,
        alpha=0.25
    )

    st.pyplot(
    fig,
    width="stretch"
    )

    plt.close(fig)


# =========================================================
# MEASUREMENTS
# =========================================================

with tabs[2]:

    cols = st.columns(4)

    cols[0].metric(
        "Mean",
        f"{metrics['mean']:.4f}"
    )

    cols[1].metric(
        "RMS",
        f"{metrics['rms']:.4f}"
    )

    cols[2].metric(
        "Peak",
        f"{metrics['peak']:.4f}"
    )

    cols[3].metric(
        "Peak-to-Peak",
        f"{metrics['peak_to_peak']:.4f}"
    )

    cols = st.columns(3)

    cols[0].metric(
        "Dominant Frequency",
        f"{metrics['dominant_frequency']:.2f} Hz"
    )

    cols[1].metric(
        "Std. Deviation",
        f"{metrics['std']:.4f}"
    )

    cols[2].metric(
        "Crest Factor",
        f"{metrics['crest_factor']:.3f}"
    )

    st.dataframe(
    pd.DataFrame([metrics]),
    width="stretch"
    )


# =========================================================
# SMART ANALYSIS
# =========================================================

with tabs[3]:

    dominant_frequency = metrics[
        "dominant_frequency"
    ]

    # Frequency interpretation

    if dominant_frequency < 1e-9:

        interpretation = (
            "The signal has no strong "
            "non-zero dominant frequency."
        )

    else:

        interpretation = (
            f"The strongest spectral component "
            f"is around {dominant_frequency:.2f} Hz."
        )

    # Noise interpretation

    if mode == "Generate Signal":

        if noise == 0:

            noise_text = (
                "No artificial noise was added "
                "to this signal."
            )

        elif noise >= 0.5:

            noise_text = (
                "The signal contains a high "
                "level of added noise."
            )

        elif noise >= 0.2:

            noise_text = (
                "The signal contains a moderate "
                "level of added noise."
            )

        else:

            noise_text = (
                "The signal contains a low "
                "level of added noise."
            )

    else:

        if metrics["std"] > abs(metrics["peak"]) * 0.35:

            noise_text = (
                "The uploaded signal shows "
                "relatively high variation."
            )

        else:

            noise_text = (
                "The uploaded signal appears "
                "relatively stable."
            )

    # Display analysis

    st.success(
        interpretation
    )

    st.info(
        noise_text
    )

    st.write(
        f"**Input:** {input_name}"
    )

    st.write(
        f"**Samples:** {len(y):,}"
    )

    st.write(
        f"**Sampling rate:** {fs:g} Hz"
    )

    st.write(
        f"**Duration:** {len(y) / fs:.3f} s"
    )

    st.write(
        f"**Filter:** {filter_type}"
    )


# =========================================================
# EXPORT
# =========================================================

with tabs[4]:

    export_df = pd.DataFrame(
        {
            "time_s": t,
            "signal": y
        }
    )

    csv_data = (
        export_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "Download analyzed signal CSV",
        csv_data,
        "analyzed_signal.csv",
        "text/csv"
    )

    report = "\n".join(
        [
            "SMART SIGNAL ANALYZER REPORT",
            "============================",
            f"Input: {input_name}",
            f"Sampling frequency: {fs:g} Hz",
            f"Samples: {len(y)}",
            f"Duration: {len(y) / fs:.3f} seconds",
            f"Filter: {filter_type}",
            f"Mean: {metrics['mean']:.6f}",
            f"RMS: {metrics['rms']:.6f}",
            f"Peak: {metrics['peak']:.6f}",
            f"Peak-to-Peak: {metrics['peak_to_peak']:.6f}",
            f"Standard deviation: {metrics['std']:.6f}",
            f"Dominant frequency: {metrics['dominant_frequency']:.6f} Hz",
            f"Crest factor: {metrics['crest_factor']:.6f}",
        ]
    )

    report_data = report.encode(
        "utf-8"
    )

    st.download_button(
        "Download analysis report",
        report_data,
        "signal_report.txt",
        "text/plain"
    )