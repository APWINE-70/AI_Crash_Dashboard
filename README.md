# AI Crash & Incident Dashboard

A real-time telemetry and analytics dashboard for tracking, diagnosing, and mitigating AI/ML model crashes, latency spikes, GPU memory leaks, and guardrail breaches.

---

## 🚀 Overview

Production AI systems face unique reliability challenges: rate limiting, token window overflows, GPU out-of-memory errors, latency degradation, and hallucination/guardrail breaches. **AI Crash Dashboard** provides a centralized observability interface for engineering and operations teams.

---

## 🛠️ Tech Stack

- **Dashboard Framework**: [Streamlit](https://streamlit.io/)
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Interactive Visualizations**: [Plotly](https://plotly.com/)
- **Language**: Python 3.10+

---

## 📦 Getting Started

### 1. Clone & Setup Workspace
```bash
git clone https://github.com/APWINE-70/AI_Crash_Dashboard.git
cd AI_Crash_Dashboard
```

### 2. Create Virtual Environment
```bash
python -m venv .venv

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Linux / macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Dashboard
```bash
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`.

---

## 📁 Repository Structure

```text
├── AGENTS.md           # Instructions, architecture, and conventions for AI Agents
├── README.md           # Project documentation and getting started guide
├── requirements.txt    # Python package dependencies
├── .gitignore          # Ignored files (virtualenvs, cache, secrets)
└── app.py              # Main Streamlit application
```

---

## 🤖 AI Agent Guidelines
For autonomous agents developing features, debugging issues, or modifying code in this repository, please review [AGENTS.md](AGENTS.md) before making changes.
