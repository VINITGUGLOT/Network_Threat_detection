# AI-Based Network Threat Detection using Wavelet Transform

An AI-powered system for detecting network threats — **DDoS**, **Port Scan**, and **Benign** traffic — using Discrete Wavelet Transform (DWT) feature extraction combined with an XGBoost classifier. Built as a Semester VI mini-project (Group 8).

## Overview

Network intrusion detection systems (NIDS) need to tell malicious traffic apart from normal traffic in real time. This project applies **Discrete Wavelet Transform (db4, level 2)** to network flow features to capture time-frequency patterns that traditional statistical features miss, then classifies the resulting feature vector using **XGBoost**.

The system detects three traffic classes:
- **Benign** – normal network traffic
- **DDoS** – Distributed Denial of Service attacks
- **Port Scan** – reconnaissance/scanning attacks

## Features

- Wavelet-based feature extraction (DWT, db4 wavelet, level 2 decomposition) producing a 22-dimensional feature vector
- XGBoost classifier trained on real-world intrusion detection data
- Flask backend serving the trained model
- Simple HTML dashboard frontend for live predictions
- Pre-trained model artifacts included (`model.pkl`, `scaler.pkl`, `label_mapping.pkl`)

## Dataset

- **CICIDS2017** – Canadian Institute for Cybersecurity Intrusion Detection Evaluation dataset, containing labeled benign and attack (DDoS, Port Scan, etc.) network traffic.

> Note: Raw dataset files are not included in this repository due to size. Download them from the official CICIDS2017 source and place them as described in the setup steps below.

## Tech Stack

| Component | Technology |
|---|---|
| Feature extraction | Python, PyWavelets (DWT) |
| Model | XGBoost |
| Backend | Flask |
| Frontend | HTML/CSS (Jinja templates) |
| Data processing | Pandas, NumPy, Scikit-learn |

## Project Structure

```
Network/
├── CICIDS2017/
│   ├── app.py                  # Flask app entry point
│   ├── data_preprocessing.py   # Data cleaning and preprocessing
│   ├── feature_extraction.py   # DWT-based feature extraction
│   ├── model_training.py       # XGBoost model training script
│   ├── model.pkl               # Trained model
│   ├── scaler.pkl              # Feature scaler
│   └── templates/
│       └── index.html          # Dashboard UI
├── model.pkl
├── scaler.pkl
├── label_mapping.pkl
└── README.md
```

## Setup & Installation

1. Clone the repository
   ```bash
   git clone https://github.com/VINITGUGLOT/Network_Threat_detection.git
   cd Network_Threat_detection
   ```

2. Create a virtual environment and install dependencies
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   pip install flask xgboost scikit-learn pandas numpy pywavelets
   ```

3. Run the Flask app
   ```bash
   cd CICIDS2017
   python app.py
   ```

4. Open your browser at `http://127.0.0.1:5000` to access the dashboard.

## How It Works

1. Network flow data is passed through preprocessing to clean and normalize features.
2. Discrete Wavelet Transform (db4, level 2) is applied to extract a 22-dimensional feature vector capturing time-frequency characteristics of the traffic.
3. Features are scaled using the saved `scaler.pkl`.
4. The XGBoost model (`model.pkl`) classifies the traffic as **Benign**, **DDoS**, or **Port Scan**.
5. The result is displayed on the Flask-served dashboard.

## Model Performance

_Add your accuracy, precision, recall, and F1-score results here from your evaluation on the CICIDS2017 test split._

## Future Improvements

- Real-time packet capture integration
- Support for additional attack categories
- Model comparison with deep learning approaches (LSTM/CNN)

## Authors

Group 8 — Semester VI Mini Project
Rajiv Gandhi College of Engineering Research and Technology (RGCERT), Chandrapur

- Vinit Venkanna Guglot
- Yash Anand Ghotekar
- Sarang Vinod Channe
- Dikshant Vilas Fulzele
- Gourav Pramod Kumbhare

## License

This project is for academic purposes.
