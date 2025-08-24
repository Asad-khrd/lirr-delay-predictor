# 🧠 Live LIRR Delay Cause Predictor

![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)
![Libraries](https://img.shields.io/badge/Libraries-Streamlit%2C%20Pandas%2C%20Scikit--learn-orange)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

A real-time dashboard that uses a machine learning model to predict the likely causes of Long Island Rail Road (LIRR) delays based on live transit data.

---

## Key Features

* **Live Data Integration:** Connects directly to the official MTA GTFS-RT feed to fetch the real-time status of active LIRR trains.
* **ML-Powered Predictions:** Uses a trained Random Forest model to predict the top 3 most likely causes of a delay for any given train, based on its branch, time of day, and other engineered features.
* **In-Depth Historical Analysis:** The model was trained on over 248,000 historical delay records from 2010-2022, with extensive Exploratory Data Analysis (EDA) to validate features.
* **Interactive Dashboard:** Built with Streamlit to provide a clean, user-friendly interface that updates with live predictions.

---

## 📸 Dashboard Screenshot


*(Add a screenshot of your running Streamlit app here!)*

---

## 🛠️ Technology Stack

* **Language:** Python 3.9+
* **Data Analysis:** Pandas, NumPy
* **Machine Learning:** Scikit-learn (RandomForestClassifier)
* **Dashboard:** Streamlit
* **Data Fetching:** Requests, Protobuf, GTFS-realtime-bindings
* **Utilities:** Joblib, Holidays

---

## 🚀 Installation and Setup

To run this project locally, follow these steps:

**1. Clone the repository:**
```bash
git clone [https://github.com/Asad-khrd/lirr-delay-predictor.git](https://github.com/Asad-khrd/lirr-delay-predictor.git)
cd lirr-delay-predictor
