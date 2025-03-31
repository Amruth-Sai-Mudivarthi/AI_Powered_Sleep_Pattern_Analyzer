# 🌙 AI-Powered Sleep Pattern Analyzer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-powered-sleep-pattern-analyzer.streamlit.app/)
![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/sleep-pattern-analyzer)
![GitHub license](https://img.shields.io/github/license/yourusername/sleep-pattern-analyzer)

An intelligent web application that analyzes your lifestyle factors to predict sleep quality and provide personalized recommendations for better rest.

![App Screenshot](https://ysm-res.cloudinary.com/image/upload/c_limit,f_auto,h_630,q_auto,w_1200/v1/yms/prod/5d491542-079c-4d25-bfeb-2364229534f7)

## ✨ Features

- **Sleep Quality Prediction**: Machine learning model predicts your sleep duration
- **Personalized Recommendations**: Tailored suggestions for sleep improvement  
- **Progress Tracking**: Monitor sleep patterns over time
- **Educational Resources**: Sleep science knowledge base
- **Interactive UI**: Beautiful visualizations and intuitive interface

## 🛠️ How It Works

The app analyzes:

```mermaid
graph TD
    A[User Input] --> B[Lifestyle Factors]
    A --> C[Sleep Environment]
    A --> D[Personal Metrics]
    B --> E[Screen Time, Exercise]
    C --> F[Bed Orientation, Lighting]
    D --> G[Age, Gender, Health]
    E & F & G --> H[ML Model]
    H --> I[Sleep Prediction]
    H --> J[Recommendations]
