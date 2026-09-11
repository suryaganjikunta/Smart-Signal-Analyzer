# 📡 Smart Signal Analyzer

A practical digital signal processing dashboard built with Python, NumPy, SciPy, Matplotlib, Pandas, and Streamlit.

## ✨ Features

- Generate sine, square, triangle, chirp, and mixed noisy signals
- Upload a CSV signal for analysis
- Time-domain waveform visualization
- FFT-based frequency spectrum
- Dominant-frequency detection
- Mean, RMS, peak, peak-to-peak, standard deviation, and crest factor
- Low-pass, high-pass, and band-pass filtering
- Original/analyzed signal export
- Downloadable text analysis report
- Clean browser-based interface

# 📡 Smart Signal Analyzer

A practical digital signal processing dashboard built with Python, NumPy, SciPy, Matplotlib, Pandas, and Streamlit.

## 🚀 Live Demo

👉 [Open Smart Signal Analyzer](https://cphmxedznzrcoljebzvyv4.streamlit.app/)

## ✨ Features

- Generate sine, square, triangle, chirp, and mixed noisy signals

- Upload a CSV signal for analysis

- Time-domain waveform visualization

- FFT-based frequency spectrum

- Dominant-frequency detection

- Mean, RMS, peak, peak-to-peak, standard deviation, and crest factor

- Low-pass, high-pass, and band-pass filtering

- Original/analyzed signal export

- Downloadable text analysis report

- Clean browser-based interface

## 🧰 Tech Stack

Python • NumPy • SciPy • Pandas • Matplotlib • Streamlit

## 🚀 Run locally

```bash
git clone https://github.com/suryaganjikunta/Smart-Signal-Analyzer.git
cd Smart-Signal-Analyzer

python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Start the application:
```bash
streamlit run app.py
```

The app will open in your browser.

## 📂 Project Structure

```text
Smart-Signal-Analyzer/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   ├── signal_generator.py
│   ├── signal_analysis.py
│   └── filters.py
├── assets/
│   └── screenshots/
└── sample_data/
```

## 🎓 ECE Concepts Used

- Sampling
- Time-domain representation
- Frequency-domain representation
- Fast Fourier Transform (FFT)
- Noise analysis
- Digital filtering
- Frequency response concepts
- Signal statistics

## 🔮 Future Scope

- Real-time microphone/ADC input
- Audio signal analysis
- Spectrogram/STFT
- SNR estimation
- IIR/FIR filter comparison
- ESP32/Arduino data streaming
- AI-assisted signal classification

## 👨‍💻 Author

**Ganjikunta Venkata Surya Prakash Reddy**

GitHub: https://github.com/suryaganjikunta

## 📄 License

MIT License
